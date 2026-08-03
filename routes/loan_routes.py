from datetime import datetime

from flask import Blueprint, jsonify, request

from extensions import db
from models.book import Book
from models.loan import Loan
from utils.decorators import token_required

loan_bp = Blueprint("loans", __name__, url_prefix="/api/loans")


@loan_bp.route("/borrow", methods=["POST"])
@token_required
def borrow_book():
    data = request.get_json(silent=True) or {}
    book_id = data.get("book_id")

    if not book_id:
        return jsonify({"error": "book_id is required"}), 400

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if book.available_copies <= 0:
        return jsonify({"error": "No copies available to borrow"}), 409

    user_id = request.current_user["id"]

    already_borrowed = Loan.query.filter_by(
        book_id=book_id, user_id=user_id, status="borrowed"
    ).first()
    if already_borrowed:
        return jsonify({"error": "You already have this book borrowed"}), 409

    loan = Loan(book_id=book_id, user_id=user_id)
    book.available_copies -= 1

    db.session.add(loan)
    db.session.commit()

    return jsonify(loan.to_dict()), 201


@loan_bp.route("/<int:loan_id>/return", methods=["POST"])
@token_required
def return_book(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404

    if loan.user_id != request.current_user["id"] and request.current_user["role"] != "admin":
        return jsonify({"error": "You can only return your own loans"}), 403

    if loan.status == "returned":
        return jsonify({"error": "This loan has already been returned"}), 409

    loan.status = "returned"
    loan.returned_at = datetime.utcnow()

    book = Book.query.get(loan.book_id)
    if book:
        book.available_copies = min(book.available_copies + 1, book.total_copies)

    db.session.commit()

    return jsonify(loan.to_dict()), 200


@loan_bp.route("", methods=["GET"])
@token_required
def list_loans():
    if request.current_user["role"] == "admin":
        loans = Loan.query.all()
    else:
        loans = Loan.query.filter_by(user_id=request.current_user["id"]).all()

    return jsonify([loan.to_dict() for loan in loans]), 200


@loan_bp.route("/<int:loan_id>", methods=["GET"])
@token_required
def get_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404

    if loan.user_id != request.current_user["id"] and request.current_user["role"] != "admin":
        return jsonify({"error": "You can only view your own loans"}), 403

    return jsonify(loan.to_dict()), 200

from datetime import datetime

from flask import Blueprint, jsonify, request

from extensions import db
from models.book import Book
from models.loan import Loan
from schemas import borrow_schema
from utils.decorators import token_required
from utils.errors import APIError
from utils.validation import validate_payload

loan_bp = Blueprint("loans", __name__, url_prefix="/api/loans")


def get_loan_or_404(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        raise APIError("Loan not found", status_code=404)
    return loan


def ensure_owner_or_admin(loan):
    if loan.user_id != request.current_user["id"] and request.current_user["role"] != "admin":
        raise APIError("You can only access your own loans", status_code=403)


@loan_bp.route("/borrow", methods=["POST"])
@token_required
def borrow_book():
    data = validate_payload(borrow_schema, request.get_json(silent=True))
    book_id = data["book_id"]

    book = Book.query.get(book_id)
    if not book:
        raise APIError("Book not found", status_code=404)

    if book.available_copies <= 0:
        raise APIError("No copies available to borrow", status_code=409)

    user_id = request.current_user["id"]

    already_borrowed = Loan.query.filter_by(
        book_id=book_id, user_id=user_id, status="borrowed"
    ).first()
    if already_borrowed:
        raise APIError("You already have this book borrowed", status_code=409)

    loan = Loan(book_id=book_id, user_id=user_id)
    book.available_copies -= 1

    db.session.add(loan)
    db.session.commit()

    return jsonify(loan.to_dict()), 201


@loan_bp.route("/<int:loan_id>/return", methods=["POST"])
@token_required
def return_book(loan_id):
    loan = get_loan_or_404(loan_id)
    ensure_owner_or_admin(loan)

    if loan.status == "returned":
        raise APIError("This loan has already been returned", status_code=409)

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
    loan = get_loan_or_404(loan_id)
    ensure_owner_or_admin(loan)
    return jsonify(loan.to_dict()), 200

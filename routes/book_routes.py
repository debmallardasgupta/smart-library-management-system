from flask import Blueprint, jsonify, request

from extensions import db
from models.book import Book
from schemas import book_create_schema, book_update_schema
from utils.decorators import token_required
from utils.errors import APIError
from utils.validation import validate_payload

book_bp = Blueprint("books", __name__, url_prefix="/api/books")


def get_book_or_404(book_id):
    book = Book.query.get(book_id)
    if not book:
        raise APIError("Book not found", status_code=404)
    return book


@book_bp.route("", methods=["POST"])
@token_required
def create_book():
    data = validate_payload(book_create_schema, request.get_json(silent=True))

    if data.get("isbn") and Book.query.filter_by(isbn=data["isbn"]).first():
        raise APIError("A book with this ISBN already exists", status_code=409)

    total_copies = data["total_copies"]

    book = Book(
        title=data["title"],
        author=data["author"],
        isbn=data.get("isbn"),
        genre=data.get("genre"),
        total_copies=total_copies,
        available_copies=total_copies,
    )

    db.session.add(book)
    db.session.commit()

    return jsonify(book.to_dict()), 201


@book_bp.route("", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify([b.to_dict() for b in books]), 200


@book_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = get_book_or_404(book_id)
    return jsonify(book.to_dict()), 200


@book_bp.route("/<int:book_id>", methods=["PUT"])
@token_required
def update_book(book_id):
    book = get_book_or_404(book_id)
    data = validate_payload(book_update_schema, request.get_json(silent=True))

    if "available_copies" in data and "total_copies" in data:
        if data["available_copies"] > data["total_copies"]:
            raise APIError("available_copies cannot exceed total_copies", status_code=400)
    elif "available_copies" in data and data["available_copies"] > book.total_copies:
        raise APIError("available_copies cannot exceed total_copies", status_code=400)

    for field, value in data.items():
        setattr(book, field, value)

    db.session.commit()

    return jsonify(book.to_dict()), 200


@book_bp.route("/<int:book_id>", methods=["DELETE"])
@token_required
def delete_book(book_id):
    book = get_book_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": f"Book {book_id} deleted"}), 200

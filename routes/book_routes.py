from flask import Blueprint, jsonify, request

from extensions import db
from models.book import Book

book_bp = Blueprint("books", __name__, url_prefix="/api/books")


@book_bp.route("", methods=["POST"])
def create_book():
    data = request.get_json(silent=True) or {}

    title = data.get("title")
    author = data.get("author")

    if not title or not author:
        return jsonify({"error": "title and author are required"}), 400

    total_copies = data.get("total_copies", 1)

    book = Book(
        title=title,
        author=author,
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
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict()), 200


@book_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json(silent=True) or {}

    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.isbn = data.get("isbn", book.isbn)
    book.genre = data.get("genre", book.genre)
    book.total_copies = data.get("total_copies", book.total_copies)
    book.available_copies = data.get("available_copies", book.available_copies)

    db.session.commit()

    return jsonify(book.to_dict()), 200


@book_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": f"Book {book_id} deleted"}), 200

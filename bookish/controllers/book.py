from flask import request
from bookish.models import db
from bookish.models.copybook import CopyBook
from bookish.models.book import Book

def register_book_routes(app):
    @app.route('/books', methods=['POST', 'GET'])
    def handle_book():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                new_book = Book(title=data['title'], author=data['author'], isbn=data['isbn'])

                db.session.add(new_book)
                db.session.flush()

                number_of__copies=data['number_of_copies']
                copies = [
                    CopyBook(book_id=new_book.id, available=True)
                    for _ in range(number_of__copies)
                ]
                
                db.session.add_all(copies)
                db.session.commit()
                return {"message": "New book has been created successfully."}
            else:
                return {"error": "The request payload is not in JSON format"}

        elif request.method == 'GET':
            books = Book.query.all()
            results = [
                {
                    'id': b.id,
                    'isbn': b.isbn, 
                    'author': b.author,
                    'title' : b.title,
                    'number of copies': b.copies.count()
                } for b in books]
            return {"books": results}
from flask import jsonify, request
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
            title_query = request.args.get('title')
            author_query = request.args.get('author')
            page_query = int(request.args.get('page', 0))
            limit_query = int(request.args.get('limit', 10))

            query = Book.query

            if title_query:
                query = query.filter(Book.title.ilike(f"%{title_query}%"))

            if author_query:
                query = query.filter(Book.author.ilike(f"%{author_query}%"))
                
            query = query.order_by(Book.title)
            
            if page_query > 0:
                query = query.offset((page_query - 1) * limit_query).limit(limit_query)
            
            results = [
                {
                    'id': b.id,
                    'isbn': b.isbn, 
                    'author': b.author,
                    'title' : b.title,
                    'number of copies': b.copies.count()
                } for b in query.all()]
            return jsonify({"books": results})
        
    @app.route('/books/<int:book_id>', methods=['GET'])
    def get_book_by_id(book_id):
        book = Book.query.get(book_id)
        if book is not None:
            result = {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "isbn": book.isbn,
                "total_copies": book.copies.count(),
                "available_copies": book.copies.filter_by(available=True).count(),
                "borrowed_copies" : [
                    {
                        "borrowed_by" : b.borrowed_by,
                        "due_date" : b.due_date
                    } for b in book.copies.filter_by(available=False)
                ]
            }

            return jsonify({"books": result})
        else:
            return {"error": "The requested book cannot be found"}
    
    @app.route('/users/<username>/books', methods=['GET'])
    def get_user_book(username):
        borrowed_books = CopyBook.query.filter(CopyBook.borrowed_by.ilike(f"{username}"))
        result = [
            {
                "book_name": b.book.title,
                "due_date" : b.due_date
            } for b in borrowed_books
        ]

        return jsonify({"books" : result})
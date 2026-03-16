from bookish.controllers.book import register_book_routes
from bookish.controllers.bookish import bookish_routes

def register_controllers(app):
    bookish_routes(app)
    register_book_routes(app)
    

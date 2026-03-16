from bookish.app import db

class Book(db.Model):

    __tablename__ = 'books'


    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)

    copies = db.relationship("CopyBook", backref="book", lazy="dynamic")

    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def __repr__(self):
        return '<Book id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'Isbn' : self.isbn,
            'title': self.title,
            'author': self.author
        }
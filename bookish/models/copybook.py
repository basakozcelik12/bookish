from bookish.app import db

class CopyBook(db.Model):

    __tablename__ = 'copy_books'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
    due_date = db.Column(db.DateTime)
    borrowed_by = db.Column(db.String())

    def __repr__(self):
        return '<CopyBook id {}>'.format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "available": self.available,
            "due_date": self.due_date,
            "borrowed_by": self.borrowed_by
        }
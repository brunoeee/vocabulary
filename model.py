from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120), nullable=False)
    language = db.Column(db.String(80), default="English")
    parse_limitation = db.Column(db.String(80), default=".*")
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    vocabularies = db.relationship("Vocabulary", back_populates='book', cascade="all, delete-orphan")

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'language': self.language,
            'parse_limitation': self.parse_limitation
            }
            
class Vocabulary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship("Book", back_populates='vocabularies')
    words = db.relationship("Word", back_populates='vocabulary', cascade="all, delete-orphan")

    def to_json(self):
        return {
            'id': self.id,
            'book': self.book.to_json(),
            'words': [word.to_json() for word in self.words]
            }

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(80), unique=True, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    createAt = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    vocabulary_id = db.Column(db.Integer, db.ForeignKey('vocabulary.id'),
                              nullable=False)
    vocabulary = db.relationship("Vocabulary",  back_populates="words")

    def to_json(self):
        return {
            'id': self.id,
            'value': self.value,
            'frequency': self.frequency,
            'createAt': self.createAt.strftime("%H:%M:%S.%f - %b %d %Y"),
            'vocabulary_id': self.vocabulary_id
        }
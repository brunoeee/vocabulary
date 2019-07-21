from flask_restful import Resource, reqparse, abort
from model import Book, Vocabulary, db

parser = reqparse.RequestParser()
parser.add_argument('book_id', required=True)

class VocabularyControler(Resource):
    def get(self, vocabulary_id):
        vocabulary = Vocabulary.query.filter_by(id=vocabulary_id).first()
        if not vocabulary:
            abort(404, message=f"vocabulary {vocabulary_id} doesn't exist")
        return vocabulary.to_json()

    def delete(self, vocabulary_id):
        vocabulary = Vocabulary.query.filter_by(id=vocabulary_id).first()
        if not vocabulary:
            abort(404, message=f"vocabulary {vocabulary_id} doesn't exist")
        db.session.delete(vocabulary)
        db.session.commit()
        return '', 204

class VocabularyListControler(Resource):
    def get(self):
        vocabularies = [voc.to_json() for voc in Vocabulary.query.all()]
        return vocabularies

    def post(self):
        args = parser.parse_args()
        book_id = args['book_id']
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            abort(404, message=f"book {book_id} doesn't exist")
        vocabulary = Vocabulary()
        book.vocabularies.append(vocabulary)
        db.session.commit()
        return vocabulary.to_json(), 201          

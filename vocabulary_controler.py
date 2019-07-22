from flask_restful import Resource, reqparse, abort
from model import Book, Vocabulary, Word, db

parser = reqparse.RequestParser()
parser.add_argument('book_id', required=True)

parser_book_title = reqparse.RequestParser()
parser_book_title.add_argument('book_title', required=True)

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

class VocabularybyTitleControler(Resource):
    def get(self):
        args = parser_book_title.parse_args()
        book_title = args['book_title']
        result_query = Vocabulary.query.join(Book).filter(Book.title == book_title).all()
        vocabularies = [voc.to_json() for voc in result_query]
        return vocabularies

class The10MostAnd10LeastFrequentWordsControler(Resource):
    def get(self, vocabulary_id):
        result_10_most_query = Word.query.join(Vocabulary)\
            .filter(Vocabulary.id == vocabulary_id)\
            .order_by(Word.frequency.desc()).limit(10).all()
        result_10_least_query = Word.query.join(Vocabulary)\
            .filter(Vocabulary.id == vocabulary_id)\
            .order_by(Word.frequency.asc()).limit(10).all()
        result_10_most_words = []
        result_10_least_words = []
        for i in range(0,10):
            result_10_most_words.append(result_10_most_query[i].to_json())
            result_10_least_words.append(result_10_least_query[i].to_json())
        return {'most': result_10_most_words, 'least': result_10_least_words}

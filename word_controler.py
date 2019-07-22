from flask_restful import Resource, reqparse, abort
from model import Book, Vocabulary, Word, db
from sqlalchemy.exc import IntegrityError

parser_vocabulary = reqparse.RequestParser()
parser_vocabulary.add_argument('vocabulary_id', required=True, type=int)

parser_all = reqparse.RequestParser()
parser_all.add_argument('vocabulary_id', required=True, type=int)
parser_all.add_argument('value', required=True)
parser_all.add_argument('frequency', required=True, type=int)

class WordControler(Resource):
    def get(self, word_id):
        word = Word.query.filter_by(id=word_id).first()
        if not word:
            abort(404, message=f"word {word_id} doesn't exist")
        return word.to_json()

    def delete(self, word_id):
        word = Word.query.filter_by(id=word_id).first()
        if not word:
            abort(404, message=f"word {word_id} doesn't exist")
        db.session.delete(word)
        db.session.commit()
        return '', 204

class WordListControler(Resource):
    def get(self):
        words = [word.to_json() for word in Word.query.all()]
        return words

    def post(self):
        args = parser_all.parse_args()
        try:
            vocabulary_id = args['vocabulary_id']
            vocabulary = Vocabulary.query.filter_by(id=vocabulary_id).first()
            if not vocabulary:
                abort(404, message=f"vocabulary {vocabulary_id} doesn't exist")
            word = Word(
                value = args['value'],
                frequency = args['frequency']
            )
            vocabulary.words.append(word)
            db.session.commit()
            return word.to_json(), 201          
        except IntegrityError as error:
            db.session.rollback()
            if 'already exists' in repr(error._sql_message):
                abort(409, message=f"{args['value']} already exists")
            abort(400)
        return ''

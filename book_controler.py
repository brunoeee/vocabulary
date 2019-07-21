import re
from flask_restful import Resource, reqparse, abort
from model import Book, db, Vocabulary, Word

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('author', required=True)
parser.add_argument('isbn', type=int, required=True)
parser.add_argument('language', required=True)
parser.add_argument('parse_limitation', required=False)

parser_abstract = reqparse.RequestParser()
parser_abstract.add_argument('book_id', required=True)
parser_abstract.add_argument('abstract', required=True)

class BookControler(Resource):
    def get(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            abort(404, message=f"book {book_id} doesn't exist")
        return book.to_json()

    def delete(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            abort(404, message=f"book {book_id} doesn't exist")
        db.session.delete(book)
        db.session.commit()
        return '', 204

    def put(self, book_id):
        args = parser.parse_args()
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            abort(404, message=f"book {book_id} doesn't exist")
        book.title = args['title']
        book.author = args['author']
        book.language = args['language']
        book.isbn = args['isbn']
        if args['parse_limitation']:
            book.parse_limitation = args['parse_limitation']
        db.session.commit()
        return book.to_json(), 201

class BookListControler(Resource):
    def get(self):
        books = [book.to_json() for book in Book.query.all()]
        return books

    def post(self):
        args = parser.parse_args()
        book = Book(
            title = args['title'],
            author = args['author'],
            language = args['language'],
            isbn = args['isbn']
        )
        if args['parse_limitation']:
            book.parse_limitation = args['parse_limitation']
        db.session.add(book)
        db.session.commit()
        return book.to_json(), 201          

class GenerateVocabularyControler(Resource):
    def post(self):
        args = parser_abstract.parse_args()
        book_id = args['book_id']
        abstract = args['abstract']
        
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            abort(404, message=f"book {book_id} doesn't exist")
        if not book.parse_limitation:
            abort(404, message=f"book {book_id} haven't parse_limitation")
        
        words_list = {}
        parse_limitation = book.parse_limitation
        for w in re.split(r'\W+', abstract):
            if re.match(parse_limitation, w):
                count = words_list.get(w, 0)
                count = count + 1
                words_list[w] = count

        vocabulary = Vocabulary()
        for w, count in words_list.items():
            word = Word(
                value = w,
                frequency = count
            )
            vocabulary.words.append(word)

        book.vocabularies.append(vocabulary)
        db.session.commit()
        return vocabulary.to_json(), 201          

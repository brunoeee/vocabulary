#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from model import db

# config
app = Flask(__name__)

# Data Base 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:postgres@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def init_db():
     with app.app_context():
        with db.engine.connect() as con:
            rs = con.execute("""SELECT table_name FROM information_schema.tables
                                WHERE table_type='BASE TABLE' AND table_schema='public'""").fetchall()
            if( len(rs) == 0 ):
                db.create_all()

# controlers
api = Api(app)
from book_controler import BookControler, BookListControler, GenerateVocabularyControler
from vocabulary_controler import VocabularyControler, VocabularyListControler
from word_controler import WordControler, WordListControler
api.add_resource(BookControler, '/books/<int:book_id>')
api.add_resource(BookListControler, '/books')
api.add_resource(GenerateVocabularyControler, '/books/generate-vocabulary')
api.add_resource(VocabularyControler, '/vocabulary/<int:vocabulary_id>')
api.add_resource(VocabularyListControler, '/vocabularies')
api.add_resource(WordControler, '/words/<int:word_id>')
api.add_resource(WordListControler, '/words')

if __name__ == '__main__':
    app.run(debug=True)


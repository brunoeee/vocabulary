#!/usr/bin/env python3
import os
from requests import put, get, post, delete

SERVER_URI = os.environ.get('SERVER_URI', "http://localhost:5000")

insert_books = [
    ('John Galsworthy', 'Forsyte Saga', 1, 'English', "^[\w]{3,}$"),
    ('John Kenneth Galbraith', 'China Passage', 2, 'English', None),
    ('John Milton', 'Paradise lost', 3, 'English', None),
    ('John Ruskin', 'Unto The Last', 4, 'English', None)
]

if __name__ == '__main__':
    for book in insert_books:
        rs = post(f'{SERVER_URI}/books', 
        data={'author': book[0], 
              'title': book[1], 
              'isbn': book[2],
              'language': book[3],
              'parse_limitation': book[4]
              })
        print(rs.json())

    print('--- Books ---')
    books = get(f'{SERVER_URI}/books').json()
    book_id = books[0]['id']
    book_title = books[0]['title']
    print(books)

    print('--- Vocabularies ---')
    # create
    post(f'{SERVER_URI}/vocabularies', 
        data={'book_id': book_id})
    # get
    vocabularies = get(f'{SERVER_URI}/vocabularies').json()
    print(vocabularies)

    print('--- words ---')
    vocabulary_id = vocabularies[0]['id']
    word = post(f'{SERVER_URI}/words', 
        data={'vocabulary_id': vocabulary_id,
              'value': 'word3',
              'frequency': 10}).json()
    print(word)

    words = get(f'{SERVER_URI}/words').json()
    print(words)

    abstract = """Lorem ipsum dolor sit amet, utroque adolescens pri cu, ne qui zril graecis.
                  Errem doctus tritani ius ne, ex salutatus expetendis usu. Ut falli voluptua
                  cum. Vel mutat regione menandri at, pro libris accumsan id, ex eligendi singulis
                  forensibus pro. Pri nisl illud minim an, qui ad aeque fabulas delectus. An ignota
                  ponderum has.
                  Etiam phaedrum cu pro, ad vix atqui eripuit accommodare. Sit eu purto putent inimicus.
                  Id singulis conclusionemque his, sint ubique minimum ad cum, duo harum discere ei. Aeque
                  tollit eirmod mei ut. No usu inani exerci oporteat, discere scripserit eam ex, mel ei 
                  malis oratio liberavisse. Ut sed dicant veniam viderer, usu ex affert delicata voluptatibus.
                  Posse primis mei ne. Luptatum indoctum no his, ei mel omittam officiis abhorreant, autem
                  noluisse deterruisset pro id. Ne hinc aeterno perpetua usu, ad autem erant mundi mel, vel
                  ludus accusam percipit ut. Nec audire regione fabulas ei. Tantas graece prodesset pri no."""

    print('--- abstract to vocabulary ---')
    generated_vocabulary = post(f'{SERVER_URI}/books/generate-vocabulary', 
        data={'book_id': book_id, 'abstract': abstract}).json()          
    print(generated_vocabulary)

    print('--- Vocabularies by book title ---')
    vocabularies_by_title = get(f'{SERVER_URI}/vocabularies/by-title', 
        data={'book_title': book_title}).json()
    print(vocabularies_by_title)

    print('--- The 10 most frequent words and 10 least frequent words in the vocabulary ---')
    vocabulary_id = vocabularies_by_title[1]['id']
    words_most_and_least = get(f'{SERVER_URI}/vocabularies/{vocabulary_id}/most-and-least').json()
    print(words_most_and_least)
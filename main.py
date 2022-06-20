
from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from Schema import movie_schema, movies_schema, director_schema, directors_schema, genres_schema, genre_schema


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}
db = SQLAlchemy(app)

api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


@movie_ns.route('/')
class MoviesViews(Resource):
    def get(self):
        all_category = db.session.query(Movie.id, Movie.title, Movie.description, Movie.trailer, Movie.year,
                                        Movie.rating, Genre.name.label('genre'), Director.name.label('director')).join(
            Genre).join(Director)
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if 'director_id' and 'genre_id':
            all_category = all_category.filter(Movie.director_id == director_id, Movie.genre_id == genre_id)


        all_movie = all_category.all()
        return movies_schema.dump(all_movie), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return f"Новый объект с id {new_movie.id} добавлен!!", 201


@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid):
        one_movie = db.session.query(Movie).get(uid)
        return jsonify(movie_schema.dump(one_movie))

    def delete(self, uid: int):
        del_movie = db.session.query(Movie).get(uid)
        if not del_movie:
            return 'Такого фильма нет'
        db.session.delete(del_movie)
        db.session.commit()
        return f'Фильм с id {del_movie.id} удален!'


@director_ns.route('/')
class DirectorsViews(Resource):
    def get(self):
        directors = db.session.query(Director).all()
        return directors_schema.dump(directors), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        db.session.commit()
        return f"Пост с id {new_director.id} добавлен!!"


@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    def get(self, uid: int):
        directors = db.session.query(Director).get(uid)
        return director_schema.dump(directors)

    def put(self, uid: int):
        directors = db.session.query(Director).get(uid)
        req_json = request.json
        directors.name = req_json.get("name")
        db.session.add(directors)
        db.session.commit()
        return f"Файл с id {directors.id} изменен!!"

    def delete(self, uid: int):
        directors = db.session.query(Director).get(uid)
        db.session.delete(directors)
        db.session.commit()
        return f"Файл с id {directors.id} удален!!"


@genre_ns.route('/')
class GenresViews(Resource):
    def get(self):
        all_genres = db.session.query(Genre).all()
        return genres_schema.dump(all_genres), 200

    def post(self):
        req_json = request.json
        new_post = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_post)
        db.session.commit()
        return f"Пост с id {new_post.id} добавлен!!"


@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    def get(self, uid: int):
        one_genre = db.session.query(Genre).get(uid)
        return genre_schema.dump(one_genre),200

    def put(self, uid: int):
        gen = db.session.query(Genre).get(uid)
        req_json = request.json
        gen.name = req_json.get("name")
        db.session.add(gen)
        db.session.commit()
        return f"Файл с id {gen.id} изменен!!",200

    def delete(self, uid: int):
        gen = db.session.query(Genre).get(uid)
        db.session.delete(gen)
        db.session.commit()
        return f"Файл с id {gen.id} удален!!",200


if __name__ == '__main__':
    app.run(debug=True)

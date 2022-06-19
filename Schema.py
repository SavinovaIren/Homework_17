from marshmallow import Schema, fields


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()

class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()
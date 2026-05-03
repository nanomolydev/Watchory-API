from enum import Enum
from marshmallow import fields, Schema, validate

class StatusOfViewing(str, Enum):
    watching = 'watching',
    watched = 'watched',
    planned = 'planned',
    dropped = 'dropped'

class TypeOfViewing(str, Enum):
    book = 'book',
    film = 'film',
    anime = 'anime',
    course = 'course'
class TMDBViewingSchema(Schema):
    id = fields.Int(dump_only=True, required=False)
    img = fields.Str(required=True,dump_only=True)
    overview = fields.Str(required=False, dump_only=True)
class PlainCollectionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
class PlainViewingSchema(Schema):
    id = fields.Int(dump_only=True, required=False)
    name = fields.Str(required=True)
    img = fields.Str(required=False)
    overview = fields.Str(required=False)
    type = fields.Enum(TypeOfViewing, required=True)
    status = fields.Enum(StatusOfViewing, required=True)
    range = fields.Int(required=False, validate=validate.Range(min=0, max=10))
    note = fields.Str(required=False)

class PlainEditViewingSchema(Schema):
    id = fields.Int(dump_only=True, required=False)
    name = fields.Str(required=False)
    type = fields.Enum(TypeOfViewing, required=False)
    status = fields.Enum(StatusOfViewing, required=False)
    range = fields.Int(required=False, validate=validate.Range(min=0, max=10))
    note = fields.Str(required=False)
class CollectionSchema(PlainCollectionSchema):
    viewings = fields.List(fields.Nested(PlainViewingSchema(), dump_only=True))
class ViewingSchema(PlainViewingSchema):
    collection_id = fields.Int(required=False, load_only=True)
    collection = fields.Nested(PlainCollectionSchema(), dump_only=True, required=False)
    tmdb_searched = fields.List(fields.Nested(TMDBViewingSchema(), dump_only=True))
class EditViewingSchema(PlainEditViewingSchema):
    collection_id = fields.Int(required=False, load_only=True)
    collection = fields.Nested(PlainCollectionSchema(), dump_only=True, required=False)

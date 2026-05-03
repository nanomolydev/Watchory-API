from flask_smorest import Blueprint
from flask.views import MethodView
from schemas import PlainCollectionSchema, CollectionSchema, ViewingSchema
from models import CollectionModel
from db import db
blp = Blueprint("collection", __name__, description="Collection object operations")

@blp.route("/collections")
class CollectionListOperation(MethodView):
    @blp.arguments(PlainCollectionSchema)
    @blp.response(201, CollectionSchema)
    def post(self, collection_data):
        new_collection = CollectionModel(**collection_data)
        db.session.add(new_collection)
        db.session.commit()
        return new_collection

    @blp.response(200, CollectionSchema(many=True))
    def get(self):
        all_collections = CollectionModel.query.all()
        return all_collections


@blp.route("/collections/<int:collection_id>")
class CollectionOperation(MethodView):


    @blp.response(200, CollectionSchema)
    def get(self, collection_id):
        collection = CollectionModel.query.get_or_404(collection_id)
        return collection

    def delete(self, collection_id):
        collection = CollectionModel.query.get_or_404(collection_id)
        db.session.delete(collection)
        db.session.commit()
        return {"message": "Delete success"}, 200

@blp.route("/collections/<int:collection_id>/viewings")
class GetViewings(MethodView):
    @blp.response(200, ViewingSchema)
    def get(self, collection_id):
        collection = CollectionModel.query.get_or_404(collection_id)
        return collection.viewings
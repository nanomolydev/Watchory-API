from flask_smorest import Blueprint
from flask.views import MethodView
from schemas import PlainCollectionSchema, CollectionSchema, ViewingSchema,PlainViewingSchema
from models import CollectionModel, ViewingModel
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
    @blp.arguments(PlainCollectionSchema)
    @blp.response(200, CollectionSchema)
    def patch(self, collection_data,collection_id):
        old_data = CollectionModel.query.get_or_404(collection_id)
        for key, item in collection_data.items():
            setattr(old_data, key,item)
        db.session.commit()
        return old_data

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
    @blp.arguments(PlainViewingSchema)
    def post(self, viewing_data, collection_id):
        viewing_data['collection_id'] = collection_id
        new_viewing = ViewingModel(**viewing_data)
        db.session.add(new_viewing)
        db.session.commit()
        return {"message": "Viewing created"}, 201
    @blp.response(200, ViewingSchema(many=True))
    def get(self, collection_id):
        collection = CollectionModel.query.get_or_404(collection_id)
        return collection.viewings
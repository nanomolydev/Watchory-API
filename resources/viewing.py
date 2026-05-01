from flask_smorest import Blueprint
from flask.views import MethodView
from db import db
from models.viewing import ViewingModel
from schemas import PlainViewingSchema, ViewingSchema, EditViewingSchema

blp = Blueprint("viewing", __name__, description="Операции с обьектом просмотра")

@blp.route("/viewings")
class ViewingsListOperation(MethodView):
    @blp.arguments(PlainViewingSchema)
    def post(self, viewing_data):
        new_viewing = ViewingModel(**viewing_data)
        db.session.add(new_viewing)
        db.session.commit()
        return {"message": "Viewing created"}, 201
    @blp.response(200, ViewingSchema(many=True))
    def get(self):
        all_viewings = ViewingModel.query.all()
        return all_viewings
    def delete(self):
        all_viewings = ViewingModel.query.all()
        for i in all_viewings:
            db.session.delete(i)
        db.session.commit()
        return  {"message": "All viewings deleted"}, 200

@blp.route("/viewings/<int:viewing_id>")
class ViewingOperation(MethodView):
    @blp.arguments(EditViewingSchema)
    @blp.response(200, ViewingSchema)
    def patch(self, viewing_data,viewing_id):

        old_data = ViewingModel.query.get_or_404(viewing_id)
        for key, item in viewing_data.items():
            setattr(old_data, key,item)
        db.session.commit()
        return old_data
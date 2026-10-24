import os
import requests
from flask_smorest import Blueprint
from flask.views import MethodView
from db import db
from models.viewing import ViewingModel
from models import TMDBModel
from sqlalchemy import and_
from schemas import PlainViewingSchema, ViewingSchema, EditViewingSchema, TMDBViewingSchema
headers = {
    "Authorization": f"Bearer {os.getenv('TMDB_API_READ_ACCESS_TOKEN')}",
    "accept": "application/json"
}

blp = Blueprint("viewing", __name__, description="Viewing object operations")

@blp.route("/viewings")
class ViewingsListOperation(MethodView):
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

    @blp.response(200, ViewingSchema)
    def get(self, viewing_id):
        find_el = ViewingModel.query.get_or_404(viewing_id)
        return find_el

    def delete(self, viewing_id):
        find_el = ViewingModel.query.get_or_404(viewing_id)
        db.session.delete(find_el)
        db.session.commit()
        return {"message": "Delete success"}, 200

@blp.route("/viewings/<int:viewing_id>/search")
class ViewingSearchOperation(MethodView):

    @blp.response(200, TMDBViewingSchema(many=True))
    def patch(self, viewing_id):
        find_viewing = ViewingModel.query.get_or_404(viewing_id)
        data = {
            "query": find_viewing.name,
            "language": "ru-RU",
            "page": 1,
            "include_adult": False
        }
        response = requests.get(
            "https://api.themoviedb.org/3/search/multi",
            headers=headers,
            params=data
        )
        data = response.json()
        if(data.get('status_code', 200) == 200):

            results = data.get('results', [])
            all_tmdb_el = []
            for i in results:
                new_viewing = TMDBModel(
                    img=f"https://image.tmdb.org/t/p/w500{i['poster_path']}",
                    overview=i.get("overview", None)
                )
                all_tmdb_el.append(new_viewing)
            find_viewing.tmdb_searched = all_tmdb_el
            db.session.add(find_viewing)
            db.session.commit()
            return all_tmdb_el
        else:
            return [{"message": data.get("status_message", None)}], 400

@blp.route("/viewings/<int:viewing_id>/tmdb-search-results/<int:tmdb_id>/select")
class ViewingTmdbOperation(MethodView):
    @blp.response(200, ViewingSchema)
    def patch(self, viewing_id, tmdb_id):
        find_viewing = ViewingModel.query.get_or_404(viewing_id)
        for i in find_viewing.tmdb_searched:
            if(i.id==tmdb_id):
                find_viewing.img = i.img
                find_viewing.overview = i.overview
                db.session.add(find_viewing)
                db.session.commit()
        return find_viewing
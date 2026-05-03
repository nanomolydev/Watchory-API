from db import db

class TMDBModel(db.Model):
    __tablename__ = 'TMDBViewings'

    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(80), nullable=False)
    overview = db.Column(db.String(200),nullable=True)
    viewing_id = db.Column(db.Integer, db.ForeignKey("viewings.id"), nullable=True)
    viewing = db.relationship("ViewingModel", back_populates="tmdb_searched")
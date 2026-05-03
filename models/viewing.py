from db import db
from schemas import StatusOfViewing, TypeOfViewing


class ViewingModel(db.Model):
    __tablename__ = "viewings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    img = db.Column(db.String(80), nullable=True)
    overview = db.Column(db.String(200), nullable=True)
    type = db.Column(db.Enum(TypeOfViewing), nullable=False)
    status = db.Column(db.Enum(StatusOfViewing), nullable=False)
    range = db.Column(db.Integer, default=0,nullable=False)
    note = db.Column(db.String(500), nullable=True)
    collection_id = db.Column(db.Integer, db.ForeignKey("collections.id"), nullable=True)
    collection = db.relationship("CollectionModel", back_populates="viewings")
    tmdb_searched = db.relationship("TMDBModel", back_populates="viewing")
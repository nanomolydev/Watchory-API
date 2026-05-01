from db import db
from schemas import StatusOfViewing, TypeOfViewing


class ViewingModel(db.Model):
    __tablename___ = "viewing"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.Enum(TypeOfViewing), nullable=False)
    status = db.Column(db.Enum(StatusOfViewing), nullable=False)
    range = db.Column(db.Integer, default=0,nullable=False)
    note = db.Column(db.String(500), nullable=True)
    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"), nullable=True)
    collection = db.relationship("CollectionModel", back_populates="viewings")
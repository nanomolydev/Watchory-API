from db import db

class CollectionModel(db.Model):
    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    viewings = db.relationship("ViewingModel", back_populates="collection")
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    items = relationship("ClothingItem", back_populates="owner")


class ClothingItem(Base):
    __tablename__ = "clothing_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    color = Column(String)
    style = Column(String)
    image_path = Column(String)
    embedding_path = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class OutfitRecommendation(Base):
    __tablename__ = "outfit_recommendations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    top_id = Column(Integer, ForeignKey("clothing_items.id"))
    bottom_id = Column(Integer, ForeignKey("clothing_items.id"))
    score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

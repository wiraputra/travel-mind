from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
import bcrypt

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    profile_picture_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    itineraries = db.relationship(
        "Itinerary", back_populates="user", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode(
            "utf-8"
        )

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    def __repr__(self):
        return f"<User {self.username}>"


class Destination(db.Model):
    __tablename__ = "destinations"

    destination_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    tags = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    avg_rating = db.Column(db.Numeric(3, 2), nullable=True)
    opening_hours = db.Column(db.JSON, nullable=True)
    typical_visit_duration_minutes = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Destination {self.name}>"


class Itinerary(db.Model):
    __tablename__ = "itineraries"

    itinerary_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    itinerary_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    number_of_days = db.Column(db.Integer, nullable=True)
    preferences = db.Column(db.JSON, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user = db.relationship("User", back_populates="itineraries")
    items = db.relationship(
        "ItineraryItem",
        back_populates="itinerary",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="ItineraryItem.day_number, ItineraryItem.order_in_day",
    )

    def __repr__(self):
        return f"<Itinerary {self.itinerary_name}>"


class ItineraryItem(db.Model):
    __tablename__ = "itinerary_items"

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    itinerary_id = db.Column(
        db.Integer, db.ForeignKey("itineraries.itinerary_id"), nullable=False
    )
    destination_id = db.Column(
        db.Integer, db.ForeignKey("destinations.destination_id"), nullable=False
    )
    day_number = db.Column(db.Integer, nullable=False)
    order_in_day = db.Column(db.Integer, nullable=False)
    visit_time = db.Column(db.Time, nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    itinerary = db.relationship("Itinerary", back_populates="items")
    destination = db.relationship("Destination")

    def __repr__(self):
        return f"<ItineraryItem day {self.day_number} order {self.order_in_day}>"

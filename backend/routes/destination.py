from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Destination

destination_bp = Blueprint('destination_bp', __name__)

@destination_bp.route('', methods=['GET'])
def get_destinations():
    param = request.args

    city = param.get('city')
    country = param.get('country')
    category = param.get('category')
    search_term = param.get('q')

    query = Destination.query

    if city:
        query =  query.filter(Destination.city.ilike(f"%{city}%"))
    if country:
        query =  query.filter(Destination.country.ilike(f"%{country}%"))
    if category:
        query =  query.filter(Destination.category.ilike(f"%{category}%"))
    if search_term:
        query =  query.filter(Destination.name.ilike(f"%{search_term}%"))

    # Pagination
    page = param.get('page', 1, type=int)
    per_page = param.get('per_page', 10, type=int)
    paginated_destinations = query.paginate(page=page, per_page=per_page, error_out=False)

    destinations_data = []
    for dest in paginated_destinations.items:
        destinations_data.append({
            "destination_id": dest.destination_id,
            "name": dest.name,
            "city": dest.city,
            "country": dest.country,
            "category": dest.category,
            "image_url": dest.image_url,
            "latitude": float(dest.latitude) if dest.latitude else None,
            "longitude": float(dest.longitude) if dest.longitude else None,
            "avg_rating": float(dest.avg_rating) if dest.avg_rating else None,
        })

    return jsonify({
        "destinations": destinations_data,
        "total": paginated_destinations.total,
        "pages": paginated_destinations.pages,
        "current_page": paginated_destinations.page,
    }), 200

@destination_bp.route('/<int:destination_id>', methods=['GET'])
def get_destination_detail(destination_id):
    destination = Destination.query.get(destination_id)

    if not destination:
        return jsonify({"msg": "Destinasi tidak ditemukan"}), 404
    
    return jsonify({
        "destination_id": destination.destination_id,
        "name": destination.name,
        "description": destination.description,
        "latitude": float(destination.latitude) if destination.latitude else None,
        "longitude": float(destination.longitude) if destination.longitude else None,
        "address": destination.address,
        "city": destination.city,
        "country": destination.country,
        "category": destination.category,
        "tags": destination.tags.split(',') if destination.tags else [],
        "image_url": destination.image_url,
        "avg_rating": float(destination.avg_rating) if destination.avg_rating else None,
        "opening_hours": destination.opening_hours,
        "typical_visit_duration_minutes": destination.typical_visit_duration_minutes,
    }), 200

@destination_bp.route('', methods=['POST'])
@jwt_required()
def create_destination():
    # current_user_id = get_jwt_identity()
    # user = User.query.get(current_user_id)
    # if not user.is_admin: # Asumsi ada field is_admin di model User
    #     return jsonify({"msg": "Akses ditolak"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"msg": "Data tidak ditemukan"}), 400
    
    name = data.get('name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not all([name, latitude, longitude]):
        return jsonify({"msg": "Nama, latitude, dan longitude dibutuhkan"}), 400
    
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return jsonify({
            "msg": "Latitude dan longitude harus berupa angka"
        }), 400
    
    new_destination = Destination(
        name=name,
        description=data.get('description'),
        latitude=latitude,
        longitude=longitude,
        address=data.get('address'),
        city=data.get('city'),
        country=data.get('country'),
        category=data.get('category'),
        tags=data.get('tags'),
        image_url=data.get('image_url'),
        avg_rating=data.get('avg_rating'),
        opening_hours=data.get('opening_hours'),
        typical_visit_duration_minutes=data.get('typical_visit_duration_minutes'),
    )

    try:
        db.session.add(new_destination)
        db.session.commit()
        return jsonify({
            "msg": "Destinasi berhasil dibuat",
            "destination_id": new_destination.destination_id
        }), 201
    except Exception as e:
        db.session.rollback()
        if "Duplicate entry" in str(e).lower() or "unique constraint" in str(e).lower():
            return jsonify({
                "msg": "Gagal membuat destinasi. Data mungkin sudah ada atau melanggar constraint unik.",
                "error_detail": str(e)
            }), 409
        return jsonify({
            "msg": "Gagal membuat destinasi",
            "error": str(e)
        }), 500
    
# Endpoint lain seperti PUT (update) dan DELETE (delete) untuk destinasi bisa ditambahkan
# dengan logika yang mirip, biasanya juga memerlukan otorisasi (misalnya admin).
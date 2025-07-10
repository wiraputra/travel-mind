from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Itinerary, ItineraryItem, Destination, User
from datetime import datetime, timedelta
from sqlalchemy import func, or_
import requests

itinerary_bp = Blueprint("itinerary_bp", __name__)


# --- CRUD untuk Itinerary ---


@itinerary_bp.route("", methods=["POST"])
@jwt_required()
def create_itinerary():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    itinerary_name = data.get("itinerary_name")
    start_date_str = data.get("start_date")  # YYYY-MM-DD
    end_date_str = data.get("end_date")  # YYYY-MM-DD
    number_of_days = data.get("number_of_days")
    preferences = data.get("preferences")  # JSON Object
    notes = data.get("notes")

    if not itinerary_name:
        return jsonify({"msg": "Nama itinerary dibutuhkan"}), 400

    start_date_obj = None
    if start_date_str:
        try:
            start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"msg": "Format start_date salah, gunakan YYYY-MM-DD"}), 400

    end_date_obj = None
    if end_date_str:
        try:
            end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"msg": "Format start_date salah, gunakan YYYY-MM-DD"}), 400

    # Hitung number_of_days jika start_date dan end_date ada, dan number_of_days tidak disediakan
    if start_date_obj and end_date_obj and number_of_days is None:
        if end_date_obj < start_date_obj:
            return (
                jsonify({"msg": "Tanggal selesai tidak boleh sebelum tanggal mulai"}),
                400,
            )
        number_of_days = (end_date_obj - start_date_obj).days + 1
    elif number_of_days is not None and number_of_days <= 0:
        return jsonify({"msg": "Jumlah hari harus positif"}), 400

    new_itinerary = Itinerary(
        user_id=current_user_id,
        itinerary_name=itinerary_name,
        start_date=start_date_obj,
        end_date=end_date_obj,
        number_of_days=number_of_days,
        preferences=preferences,
        notes=notes,
    )

    try:
        db.session.add(new_itinerary)
        db.session.commit()
        return (
            jsonify(
                {
                    "msg": "Itinerary berhasil dibuat",
                    "itinerary_id": new_itinerary.itinerary_id,
                    "itinerary_name": new_itinerary.itinerary_name,
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Gagal membuat itinerary", "error": str(e)}), 500


@itinerary_bp.route("", methods=["GET"])
@jwt_required()
def get_user_itineraries():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User tidak ditemukan"}), 404

    itineraries = []
    for itinerary in user.itineraries:
        itineraries.append(
            {
                "itinerary_id": itinerary.itinerary_id,
                "itinerary_name": itinerary.itinerary_name,
                "start_date": (
                    itinerary.start_date.strftime("%Y-%m-%d")
                    if itinerary.start_date
                    else None
                ),
                "end_date": (
                    itinerary.end_date.strftime("%Y-%m-%d")
                    if itinerary.end_date
                    else None
                ),
                "number_of_days": itinerary.number_of_days,
                "created_at": itinerary.created_at.isoformat(),
            }
        )
    return jsonify(itineraries), 200


@itinerary_bp.route("/<int:itinerary_id>", methods=["GET"])
@jwt_required()
def get_itinerary_detail(itinerary_id):
    current_user_id = get_jwt_identity()
    itinerary = Itinerary.query.filter_by(
        itinerary_id=itinerary_id, user_id=current_user_id
    ).first()

    if not itinerary:
        return (
            jsonify(
                {"msg": "Itinerary tidak ditemukan atau anda tidak memiliki aksess"}
            ),
            404,
        )

    items_data = []
    for item in itinerary.items:
        destination_data = None
        if item.destination:
            destination_data = {
                "destination_id": item.destination.destination_id,
                "name": item.destination.name,
                "latitude": (
                    float(item.destination.latitude)
                    if item.destination.latitude
                    else None
                ),
                "longitude": (
                    float(item.destination.longitude)
                    if item.destination.longitude
                    else None
                ),
                "image_url": item.destination.image_url,
                "category": item.destination.category,
                "city": item.destination.city,
                "country": item.destination.country,
                "avg_rating": float(item.destination.avg_rating)
                if item.destination.avg_rating
                else None,
                "opening_hours": item.destination.opening_hours,
                "typical_visit_duration_minutes": item.destination.typical_visit_duration_minutes,
            }
        items_data.append(
            {
                "item_id": item.item_id,
                "destination": destination_data,
                "day_number": item.day_number,
                "order_in_day": item.order_in_day,
                "visit_time": (
                    item.visit_time.strftime("%H-%M-%S") if item.visit_time else None
                ),
                "duration_minute": item.duration_minutes,
                "notes": item.notes,
            }
        )

    return (
        jsonify(
            {
                "itinerary_id": itinerary.itinerary_id,
                "itinerary_name": itinerary.itinerary_name,
                "start_date": (
                    itinerary.start_date.strftime("%Y-%m-%d")
                    if itinerary.start_date
                    else None
                ),
                "end_date": (
                    itinerary.end_date.strftime("%Y-%m-%d")
                    if itinerary.end_date
                    else None
                ),
                "number_of_days": itinerary.number_of_days,
                "preferences": itinerary.preferences,
                "notes": itinerary.notes,
                "created_at": itinerary.created_at.isoformat(),
                "updated_at": itinerary.updated_at.isoformat(),
                "items": items_data,
            }
        ),
        200,
    )


@itinerary_bp.route("/<int:itinerary_id>", methods=["PUT"])
@jwt_required()
def update_itinerary(itinerary_id):
    current_user_id = get_jwt_identity()
    itinerary = Itinerary.query.filter_by(
        itinerary_id=itinerary_id, user_id=current_user_id
    ).first()

    if not itinerary:
        return (
            jsonify(
                {"msg": "Itinerary tidak ditemukan atau Anda tidak memiliki akses"}
            ),
            404,
        )

    data = request.get_json()

    has_changes = False

    if "itinerary_name" in data:
        itinerary.itinerary_name = data["itinerary_name"]
        has_changes = True

    new_start_date_str = data.get("start_date")
    new_end_date_str = data.get("end_date")
    new_number_of_days = data.get("number_of_days")

    if new_start_date_str and new_end_date_str:
        try:
            start_date_obj = datetime.strptime(new_start_date_str, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(new_end_date_str, "%Y-%m-%d").date()
            if end_date_obj < start_date_obj:
                return jsonify(
                    {"msg": "Tanggal selesai tidak boleh sebelum tanggal mulai"}
                ), 400

            calculated_days = (end_date_obj - start_date_obj).days + 1

            if itinerary.start_date != start_date_obj:
                itinerary.start_date = start_date_obj
                has_changes = True
            if itinerary.end_date != end_date_obj:
                itinerary.end_date = end_date_obj
                has_changes = True
            if itinerary.number_of_days != calculated_days:
                itinerary.number_of_days = calculated_days
                has_changes = True
        except ValueError:
            return jsonify({"msg": "Format tanggal salah, gunakan YYYY-MM-DD"}), 400
    elif new_number_of_days is not None:
        try:
            num_days = int(new_number_of_days)
            if num_days <= 0:
                return jsonify({"msg": "Jumlah hari harus positif"}), 400
            if itinerary.start_date is not None:
                itinerary.start_date = None
                has_changes = True
            if itinerary.end_date is not None:
                itinerary.end_date = None
                has_changes = True
            if itinerary.number_of_days != num_days:
                itinerary.number_of_days = num_days
                has_changes = True
        except ValueError:
            return jsonify({"msg": "Jumlah hari harus angka"}), 400
    elif (
        "start_date" in data
        and data["start_date"] is None
        and "end_date" in data
        and data["end_date"] is None
        and "number_of_days" in data
        and data["number_of_days"] is None
    ):
        if itinerary.start_date is not None:
            itinerary.start_date = None
            has_changes = True
        if itinerary.end_date is not None:
            itinerary.end_date = None
            has_changes = True
        if itinerary.number_of_days is not None:
            itinerary.number_of_days = None
            has_changes = True

    if "notes" in data:
        if itinerary.notes != data["notes"]:
            itinerary.notes = data["notes"]
            has_changes = True

    # if 'preferences' in data:
    #     itinerary.preferences = data['preferences']
    #     has_changes = True

    if not has_changes:
        return jsonify({"msg": "Tidak ada perubahan data yang dikirim."}), 304

    itinerary.updated_at = datetime.now()

    try:
        db.session.commit()
        return jsonify(
            {
                "msg": "Itinerary berhasil diupdate",
                "itinerary_id": itinerary.itinerary_id,
                "itinerary_name": itinerary.itinerary_name,
                "start_date": itinerary.start_date.isoformat()
                if itinerary.start_date
                else None,
                "end_date": itinerary.end_date.isoformat()
                if itinerary.end_date
                else None,
                "number_of_days": itinerary.number_of_days,
                "notes": itinerary.notes,
                "preferences": itinerary.preferences,
                "created_at": itinerary.created_at.isoformat(),
                "updated_at": itinerary.updated_at.isoformat(),
            }
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Gagal mengupdate itinerary", "error": str(e)}), 500


@itinerary_bp.route("/<int:itinerary_id>", methods=["DELETE"])
@jwt_required()
def delete_itinerary(itinerary_id):
    current_user_id = get_jwt_identity()
    itinerary = Itinerary.query.filter_by(
        itinerary_id=itinerary_id, user_id=current_user_id
    ).first()

    if not itinerary:
        return (
            jsonify(
                {"msg": "Itinerary tidak ditemukan atau Anda tidak memiliki akses"}
            ),
            404,
        )

    try:
        db.session.delete(
            itinerary
        )  # Cascade delete untuk ItineraryItems akan bekerja di sini
        db.session.commit()
        return jsonify({"msg": "Itinerary berhasil dihapus"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Gagal menghapus itinerary", "error": str(e)}), 500


INTEREST_KEYWORDS_MAP = {
    "alam": [
        "alam",
        "pemandangan",
        "gunung",
        "pantai",
        "danau",
        "air terjun",
        "taman nasional",
        "outdoor",
    ],
    "sejarah": [
        "sejarah",
        "budaya",
        "arkeologi",
        "museum sejarah",
        "candi",
        "benteng",
        "kerajaan",
        "peninggalan",
    ],
    "kuliner": [
        "kuliner",
        "makanan",
        "restoran",
        "kafe",
        "pasar tradisional",
        "jajanan",
        "makanan khas",
    ],
    "belanja": [
        "belanja",
        "pasar",
        "mal",
        "toko",
        "oleh-oleh",
        "butik",
        "pusat perbelanjaan",
    ],
    "seni": [
        "seni",
        "museum seni",
        "galeri",
        "lukisan",
        "patung",
        "pameran seni",
        "budaya",
    ],
    "hiburan": [
        "hiburan",
        "relaksasi",
        "spa",
        "taman hiburan",
        "bioskop",
        "konser",
        "nightlife",
        "karaoke",
    ],
    "petualangan": [
        "petualangan",
        "hiking",
        "trekking",
        "rafting",
        "diving",
        "snorkeling",
        "mendaki",
        "outdoor",
    ],
}


def generate_simple_ai_schedule(
    destination_city, preferences, num_days, start_date_obj=None
):
    schedule_items_per_day = {}

    base_query = Destination.query.filter(
        Destination.city.ilike(f"%{destination_city}%")
    )

    user_interests_values = preferences.get("interests", [])
    all_interest_conditions = []
    if user_interests_values:
        for interest_value in user_interests_values:
            keyword_for_interest = INTEREST_KEYWORDS_MAP.get(
                interest_value.lower(), [interest_value.lower()]
            )

            single_interest_conditions = []
            for keyword in keyword_for_interest:
                single_interest_conditions.append(
                    Destination.category.ilike(f"%{keyword}%")
                )
                single_interest_conditions.append(
                    Destination.tags.ilike(f"%{keyword}%")
                )

            if single_interest_conditions:
                all_interest_conditions.append(or_(*single_interest_conditions))

    if all_interest_conditions:
        base_query = base_query.filter(or_(*all_interest_conditions))

    trip_type = preferences.get("trip_type")
    if trip_type == "keluarga":
        family_tags = ["%ramah keluarga%", "%anak-anak%", "%hiburan keluarga%"]
        family_conditions = [Destination.tags.ilike(tag) for tag in family_tags]
        base_query = base_query.filter(or_(*family_conditions))
    elif trip_type == "pasangan":
        base_query = base_query.filter(Destination.tags.ilike("%romantis%"))

    destinations_per_day_map = {"santai": 2, "sedang": 3, "padat": 4}
    target_dest_per_day = destinations_per_day_map.get(
        preferences.get("pace", "sedang"), 3
    )

    candidate_destinations_all = (
        base_query.order_by(Destination.avg_rating.desc(), func.random())
        .limit(num_days * target_dest_per_day * 5)
        .all()
    )

    if not candidate_destinations_all:
        return {}

    used_destination_ids = set()

    estimated_daily_duration = {day: 0 for day in range(1, num_days + 1)}

    for day_num in range(1, num_days + 1):
        schedule_items_per_day[day_num] = []
        dest_count_for_day = 0
        categories_in_day = set()

        available_candidates = [
            d
            for d in candidate_destinations_all
            if d.destination_id not in used_destination_ids
        ]

        for dest in available_candidates:
            if dest_count_for_day >= target_dest_per_day:
                break

            can_add_by_category_diversity = True
            if (
                len(user_interests_values) > 1
                and dest.category
                and dest.category.lower() in categories_in_day
            ):
                pass

            if can_add_by_category_diversity:
                schedule_items_per_day[day_num].append(
                    {
                        "destination_id": dest.destination_id,
                        "order_in_day": dest_count_for_day + 1,
                    }
                )
                used_destination_ids.add(dest.destination_id)
                if dest.category:
                    categories_in_day.add(dest.category.lower())

                # if dest.typical_visit_duration_minutes:
                #     estimated_daily_duration[day_num] += (
                #         dest.typical_visit_duration_minutes
                #     )

                dest_count_for_day += 1

        if not schedule_items_per_day[day_num] and len(used_destination_ids) < len(
            candidate_destinations_all
        ):
            remaining_candidates_for_empty_day = [
                d
                for d in candidate_destinations_all
                if d.destination_id not in used_destination_ids
            ]
            if remaining_candidates_for_empty_day:
                chosen_remaining = remaining_candidates_for_empty_day[0]
                schedule_items_per_day[day_num].append(
                    {
                        "destination_id": chosen_remaining.destination_id,
                        "order_in_day": 1,
                    }
                )
                used_destination_ids.add(chosen_remaining.destination_id)
                if chosen_remaining.typical_visit_duration_minutes:
                    estimated_daily_duration[day_num] += (
                        chosen_remaining.typical_visit_duration_minutes
                    )

    final_schedule_for_db = {}
    for day, items_with_details in schedule_items_per_day.items():
        final_schedule_for_db[day] = [
            item_detail["destination_id"] for item_detail in items_with_details
        ]

    return final_schedule_for_db


@itinerary_bp.route("/generate-ai", methods=["POST"])
@jwt_required()
def create_itinerary_with_ai():
    current_user_id = get_jwt_identity()
    user_id = int(current_user_id)
    data = request.get_json()
    itinerary_name = data.get("itinerary_name")
    start_date_str = data.get("start_date")
    end_date_str = data.get("end_date")
    number_of_days_input = data.get("number_of_days")
    notes = data.get("notes")
    preferences = data.get("preferences", {})

    if not itinerary_name:
        return jsonify({"msg": "Nama itinerary dibutuhkan"}), 400
    if not preferences.get("destination_city"):
        return jsonify({"msg": "Kota/Wilayah Tujuan dibutuhkan"}), 400
    if not preferences.get("interests") or len(preferences["interests"]) == 0:
        return jsonify({"msg": "Minimal satu minat dibutuhkan"}), 400

    start_date_obj, end_date_obj, num_days = None, None, 0
    if start_date_str and end_date_str:
        try:
            start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            if end_date_obj < start_date_obj:
                return jsonify({"msg": "Tanggal selesai sebelum tanggal mulai"}), 400
            num_days = (end_date_obj - start_date_obj).days + 1
        except ValueError:
            return jsonify({"msg": "Format tanggal salah"}), 400
    elif number_of_days_input:
        try:
            num_days = int(number_of_days_input)
            if num_days <= 0:
                return jsonify({"msg": "Jumlah hari harus positif"}), 400
            if start_date_str:
                try:
                    start_date_obj = datetime.strptime(
                        start_date_str, "%Y-%m-%d"
                    ).date()
                    if start_date_obj:
                        end_date_obj = start_date_obj + timedelta(days=num_days - 1)
                except ValueError:
                    pass
        except ValueError:
            return jsonify({"msg": "Jumlah hari harus angka"}), 400
    else:
        return jsonify({"msg": "Isi Tanggal Mulai & Selesai atau Jumlah Hari"}), 400
    if num_days == 0:
        return jsonify({"msg": "Durasi itinerary tidak bisa nol."}), 400

    destination_city = preferences.get("destination_city")
    ai_schedule_dest_ids_per_day = generate_simple_ai_schedule(
        destination_city, preferences, num_days, start_date_obj
    )

    if not ai_schedule_dest_ids_per_day or all(
        not items for items in ai_schedule_dest_ids_per_day.values()
    ):
        return jsonify(
            {
                "msg": f"Maaf, tidak dapat menemukan destinasi yang cocok untuk preferensi Anda di {destination_city}."
            }
        ), 404

    new_itinerary = Itinerary(
        user_id=user_id,
        itinerary_name=itinerary_name,
        start_date=start_date_obj,
        end_date=end_date_obj,
        number_of_days=num_days,
        preferences=preferences,
        notes=notes,
    )
    db.session.add(new_itinerary)

    try:
        db.session.flush()

        items_to_add = []
        for day_num, dest_ids_for_day_list in ai_schedule_dest_ids_per_day.items():
            for order_in_day_idx, dest_id in enumerate(dest_ids_for_day_list):
                item = ItineraryItem(
                    itinerary_id=new_itinerary.itinerary_id,
                    destination_id=dest_id,
                    day_number=day_num,
                    order_in_day=order_in_day_idx + 1,
                )
                items_to_add.append(item)

        if items_to_add:
            db.session.bulk_save_objects(items_to_add)
        db.session.commit()

        return jsonify(
            {
                "msg": "Itinerary AI berhasil dibuat!",
                "itinerary_id": new_itinerary.itinerary_id,
                "itinerary_name": new_itinerary.itinerary_name,
            }
        ), 201
    except Exception:
        db.session.rollback()
        # current_app.logger.error(f"Error saving AI itinerary: {str(e)}")
        return jsonify(
            {
                "msg": "Gagal menyimpan itinerary AI",
                "error": "Terjadi kesalahan internal.",
            }
        ), 500


# --- CRUD untuk Itinerary Items --


@itinerary_bp.route("/<int:itinerary_id>/items", methods=["POST"])
@jwt_required()
def add_item_to_itinerary(itinerary_id):
    current_user_id = get_jwt_identity()
    itinerary = Itinerary.query.filter_by(
        itinerary_id=itinerary_id, user_id=current_user_id
    ).first()

    if not itinerary:
        return (
            jsonify(
                {"msg": "Itinerary tidak ditemukan atau Anda tidak memiliki akses"}
            ),
            404,
        )

    data = request.get_json()
    destination_id = data.get("destination_id")
    day_number = data.get("day_number")
    order_in_day = data.get("order_in_day")
    visit_time_str = data.get("visit_time")
    duration_minutes = data.get("duration_minutes")
    notes = data.get("notes")

    if not destination_id or not day_number:
        return jsonify({"msg": "destination_id dan day_number dibutuhkan"}), 400

    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({"msg": "Destinasi tidak ditemukan"}), 404

    if itinerary.number_of_days and day_number > itinerary.number_of_days:
        return (
            jsonify(
                {
                    "msg": f"Day number ({day_number}) melebihi jumlah hari itinerary ({itinerary.number_of_days})"
                }
            ),
            400,
        )
    if day_number <= 0:
        return jsonify({"msg": "Day number harus positif"}), 400

    if order_in_day is None:
        last_item_in_day = (
            ItineraryItem.query.filter_by(
                itinerary_id=itinerary_id, day_number=day_number
            )
            .order_by(ItineraryItem.order_in_day.desc())
            .first()
        )
        order_in_day = (last_item_in_day.order_in_day + 1) if last_item_in_day else 1
    elif order_in_day <= 0:
        return jsonify({"msg": "Order in day harus positif"}), 400

    visit_time_obj = None
    if visit_time_str:
        try:
            visit_time_obj = datetime.strptime(visit_time_str, "%H:%M:%S").time()
        except ValueError:
            try:
                visit_time_obj = datetime.strptime(visit_time_str, "%H:%M").time()
            except ValueError:
                return (
                    jsonify(
                        {"msg": "Format visit_time salah, gunakan HH:MM:SS atau HH:MM"}
                    ),
                    400,
                )

    new_item = ItineraryItem(
        itinerary_id=itinerary_id,
        destination_id=destination_id,
        day_number=day_number,
        order_in_day=order_in_day,
        visit_time=visit_time_obj,
        duration_minutes=duration_minutes,
        notes=notes,
    )

    try:
        db.session.add(new_item)
        db.session.commit()
        return (
            jsonify(
                {
                    "msg": "Item berhasil ditambahkan ke itinerary",
                    "item_id": new_item.item_id,
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Gagal menambahkan item", "error": str(e)}), 500


@itinerary_bp.route("/<int:itinerary_id>/items/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_itinerary_item(itinerary_id, item_id):
    current_user_id = get_jwt_identity()
    item = (
        ItineraryItem.query.join(Itinerary)
        .filter(
            ItineraryItem.item_id == item_id,
            Itinerary.itinerary_id == itinerary_id,
            Itinerary.user_id == current_user_id,
        )
        .first()
    )

    if not item:
        return (
            jsonify(
                {"msg": "Item itinerary tidak ditemukan atau Anda tidak memiliki akses"}
            ),
            404,
        )

    data = request.get_json()

    if "day_number" in data:
        new_day_number = data["day_number"]
        if (
            item.itinerary.number_of_days
            and new_day_number > item.itinerary.number_of_days
        ):
            return (
                jsonify(
                    {
                        "msg": f"Day number ({new_day_number}) melebihi jumlah hari itinerary ({item.itinerary.number_of_days})"
                    }
                ),
                400,
            )
        if new_day_number <= 0:
            return jsonify({"msg": "Day number harus positif"}), 400
        item.day_number = new_day_number

    if "order_in_day" in data:
        new_order_in_day = data["order_in_day"]
        if new_order_in_day <= 0:
            return jsonify({"msg": "Order in day harus positif"}), 400
        item.order_in_day = new_order_in_day

    if "visit_time" in data:
        visit_time_str = data["visit_time"]
        if visit_time_str is None:
            item.visit_time = None
        else:
            try:
                item.visit_time = datetime.strptime(visit_time_str, "%H:%M:%S").time()
            except ValueError:
                try:
                    item.visit_time = datetime.strptime(visit_time_str, "%H:%M").time()
                except ValueError:
                    return (
                        jsonify(
                            {
                                "msg": "Format visit_time salah, gunakan HH:MM:SS atau HH:MM"
                            }
                        ),
                        400,
                    )

    if "duration_minutes" in data:
        item.duration_minutes = data["duration_minutes"]
    if "notes" in data:
        item.notes = data["notes"]

    try:
        db.session.commit()
        return (
            jsonify(
                {
                    "msg": "Item itinerary berhasil diupdate",
                    "item_id": item.item_id,
                    "day_number": item.day_number,
                    "order_in_day": item.order_in_day,
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Gagal mengupdate item itinerary", "error": str(e)}), 500


@itinerary_bp.route("/<int:itinerary_id>/items/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_itinerary_item(itinerary_id, item_id):
    current_user_id = get_jwt_identity()
    item = (
        ItineraryItem.query.join(Itinerary)
        .filter(
            ItineraryItem.item_id == item_id,
            Itinerary.itinerary_id == itinerary_id,
            Itinerary.user_id == current_user_id,
        )
        .first()
    )

    if not item:
        return (
            jsonify(
                {"msg": "Item itinerary tidak ditemukan atau Anda tidak memiliki akses"}
            ),
            404,
        )

    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"msg": "Item itinerary berhasil dihapus"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Gagal menghapus item itinerary", "error": str(e)}), 500


# Endpoint untuk mengupdate urutan semua item dalam itinerary (untuk drag & drop)
@itinerary_bp.route("/<int:itinerary_id>/items/reorder", methods=["PUT"])
@jwt_required()
def reorder_itinerary_items(itinerary_id):
    current_user_id = get_jwt_identity()
    itinerary = Itinerary.query.filter_by(
        itinerary_id=itinerary_id, user_id=current_user_id
    ).first()

    if not itinerary:
        return (
            jsonify(
                {"msg": "Itinerary tidak ditemukan atau Anda tidak memiliki akses"}
            ),
            404,
        )

    # Data yang diharapkan adalah list of objects, dimana setiap object memiliki 'item_id', 'day_number', 'order_in_day'
    # Contoh: [{"item_id": 1, "day_number": 1, "order_in_day": 1}, {"item_id": 3, "day_number": 1, "order_in_day": 2}, ...]
    ordered_items_data = request.get_json()
    if not isinstance(ordered_items_data, list):
        return jsonify({"msg": "Data harus berupa list item yang diurutkan"}), 400

    try:
        existing_item_ids = {item.item_id for item in itinerary.items}

        for item_data in ordered_items_data:
            item_id = item_data.get("item_id")
            new_day = item_data.get("day_number")
            new_order = item_data.get("order_in_day")

            if not all(
                [
                    isinstance(item_id, int),
                    isinstance(new_day, int),
                    isinstance(new_order, int),
                ]
            ):
                db.session.rollback()
                return (
                    jsonify(
                        {
                            "msg": "Setiap item harus memiliki item_id, day_number, dan order_in_day (integer)"
                        }
                    ),
                    400,
                )

            if item_id not in existing_item_ids:
                db.session.rollback()
                return (
                    jsonify(
                        {
                            "msg": f"Item dengan id {item_id} tidak ditemukan dalam itinerary ini."
                        }
                    ),
                    404,
                )

            item_to_update = ItineraryItem.query.get(item_id)
            if item_to_update:  # Seharusnya selalu ada karena cek existing_item_ids
                item_to_update.day_number = new_day
                item_to_update.order_in_day = new_order
            else:  # Double check, seharusnya tidak terjadi
                db.session.rollback()
                return (
                    jsonify(
                        {
                            "msg": f"Gagal menemukan item dengan id {item_id} untuk diupdate."
                        }
                    ),
                    500,
                )

        db.session.commit()
        return jsonify({"msg": "Urutan item itinerary berhasil diupdate"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Gagal mengupdate urutan item", "error": str(e)}), 500


@itinerary_bp.route(
    "/<int:itinerary_id>/days/<int:day_number>/optimize-route", methods=["POST"]
)
@jwt_required()
def get_optimized_route_for_day(itinerary_id, day_number):
    current_user_id = int(get_jwt_identity())
    itinerary = Itinerary.query.filter_by(
        itinerary_id=itinerary_id, user_id=current_user_id
    ).first_or_404()

    data = request.get_json()
    start_coords = data.get("start_coords")
    if not start_coords or len(start_coords) != 2:
        return jsonify({"msg": "Koordinat awal dibutuhkan."}), 400

    items_for_day = (
        ItineraryItem.query.filter_by(itinerary_id=itinerary_id, day_number=day_number)
        .join(Destination)
        .order_by(ItineraryItem.order_in_day)
        .all()
    )

    if len(items_for_day) < 1:
        return jsonify(
            {"msg": "Tidak ada destinasi untuk dioptimalkan pada hari ini."}
        ), 400

    # Siapkan daftar koordinat untuk ORS API
    # Format ORS: [longitude, latitude]
    coordinates = [start_coords]
    item_id_map = {0: "start_location"}  # Map index ke item_id
    for i, item in enumerate(items_for_day):
        if (
            item.destination
            and item.destination.longitude is not None
            and item.destination.latitude is not None
        ):
            coordinates.append(
                [float(item.destination.longitude), float(item.destination.latitude)]
            )
            item_id_map[i + 1] = item.item_id

    coordinates.append(start_coords)

    if len(coordinates) < 2:
        return jsonify({"msg": "Tidak cukup destinasi dengan koordinat valid."}), 400

    api_key = current_app.config.get("ORS_API_KEY")
    if not api_key:
        return jsonify({"msg": "ORS API Key tidak dikonfigurasi di server."}), 500

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json; charset=utf-8",
    }
    # Gunakan 'optimize_waypoints=true' untuk membiarkan ORS menemukan urutan terbaik
    # (Fitur ini mungkin terbatas pada profil tertentu atau memerlukan panggilan ke endpoint optimasi)
    # Untuk Directions API standar, ia akan mengikuti urutan yang kita berikan.
    # Kita bisa panggil Optimization API jika diperlukan, atau urutkan manual dengan matriks jarak.
    # Untuk sekarang, kita hitung rute berdasarkan urutan yang ada.

    body = {"coordinates": coordinates}

    try:
        response = requests.post(
            "https://api.openrouteservice.org/v2/directions/driving-car/geojson",
            json=body,
            headers=headers,
        )
        response.raise_for_status()

        route_data = response.json()

        geometry = route_data["features"][0]["geometry"]  # Koordinat untuk polyline
        summary = route_data["features"][0]["properties"][
            "summary"
        ]  # { distance, duration }

        # Karena Directions API standar mengikuti urutan, urutan item tidak berubah
        # Jika ingin optimasi, kita perlu langkah tambahan (misalnya, panggil ORS Matrix API)

        return jsonify(
            {
                "route_geometry": geometry,
                "distance_meters": summary.get("distance"),
                "duration_seconds": summary.get("duration"),
                "optimized_order": [
                    item.item_id for item in items_for_day
                ],  # Urutan saat ini
            }
        ), 200

    except requests.exceptions.RequestException as e:
        return jsonify(
            {"msg": "Gagal menghubungi OpenRouteService.", "error": str(e)}
        ), 503
    except Exception as e:
        current_app.logger.error(f"Error processing ORS response: {e}")
        return jsonify({"msg": "Gagal memproses respons dari ORS."}), 500

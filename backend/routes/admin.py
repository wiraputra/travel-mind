import csv
import io
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
import json

from sqlalchemy import func
from models import ItineraryItem, db, User, Destination, Itinerary
from admin_forms import UserAdminForm, UserAdminEditForm, DestinationForm

admin_bp = Blueprint(
    "admin_bp", __name__, url_prefix="/admin", template_folder="../templates/admin"
)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in") or not session.get("is_admin_user"):
            flash("Silakan login sebagai admin untuk mengakses halaman ini.", "warning")
            return redirect(url_for("admin_auth.admin_login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@admin_bp.route("/")
@admin_required
def index():
    user_count = User.query.count()
    destination_count = Destination.query.count()
    itinerary_count = Itinerary.query.count()
    return render_template(
        "dashboard.html",
        user_count=user_count,
        destination_count=destination_count,
        itinerary_count=itinerary_count,
    )


# ===============
# CRUD untuk USER
# ===============
@admin_bp.route("/users")
@admin_required
def users_list():
    page = request.args.get("page", 1, type=int)
    users = User.query.order_by(User.user_id).paginate(page=page, per_page=15)
    return render_template("user_list.html", users=users)


@admin_bp.route("/users/new", methods=["GET", "POST"])
@admin_required
def add_user():
    form = UserAdminForm()
    if form.validate_on_submit():
        existing_user_email = User.query.filter(
            func.lower(User.email) == func.lower(form.email.data)
        ).first()
        existing_user_username = User.query.filter(
            func.lower(User.username) == func.lower(form.username.data)
        ).first()
        if existing_user_email:
            flash("Email sudah terdaftar.", "danger")
        elif existing_user_username:
            flash("Username sudah digunakan.", "danger")
        elif not form.password.data:
            flash("Password wajib diisi untuk user baru.", "danger")
        else:
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                full_name=form.full_name.data,
                is_admin=form.is_admin.data,
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash(f'User "{new_user.username}" berhasil dibuat.', "success")
            return redirect(url_for(".users_list"))
    return render_template("user_form.html", form=form, form_title="Buat User Baru")


@admin_bp.route("/users/edit/<int:user_id>", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserAdminEditForm(obj=user)
    if form.validate_on_submit():
        if (
            user.email.lower() != form.email.data.lower()
            and User.query.filter(
                User.user_id != user_id,
                func.lower(User.email) == func.lower(form.email.data),
            ).first()
        ):
            flash("Email tersebut sudah digunakan oleh user lain.", "danger")
        elif (
            user.username.lower() != form.username.data.lower()
            and User.query.filter(
                User.user_id != user_id,
                func.lower(User.username) == func.lower(form.username.data),
            ).first()
        ):
            flash("Username tersebut sudah digunakan oleh user lain.", "danger")
        else:
            user.username = form.username.data
            user.email = form.email.data
            user.full_name = form.full_name.data
            user.is_admin = form.is_admin.data
            if form.password.data:
                user.set_password(form.password.data)
            db.session.commit()
            flash(f'User "{user.username}" berhasil diperbarui.', "success")
            return redirect(url_for(".users_list"))

    # Isi ulang data saat GET request (penting jika validasi gagal)
    form.username.data = user.username
    form.email.data = user.email
    form.full_name.data = user.full_name
    form.is_admin.data = user.is_admin
    return render_template(
        "user_form.html", form=form, form_title=f"Edit User: {user.username}"
    )


@admin_bp.route("/users/delete/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if session.get("admin_user_id") == user.user_id:
        flash("Tidak dapat menghapus akun Anda sendiri.", "danger")
        return redirect(url_for(".users_list"))
    db.session.delete(user)
    db.session.commit()
    flash(f'User "{user.username}" berhasil dihapus.', "success")
    return redirect(url_for(".users_list"))


# ==================================
# CRUD untuk DESTINASI (DESTINATION)
# ==================================
@admin_bp.route("/destinations")
@admin_required
def destinations_list():
    page = request.args.get("page", 1, type=int)
    search_term = request.args.get("q", "")
    query = Destination.query.order_by(Destination.name)
    if search_term:
        query = query.filter(Destination.name.ilike(f"%{search_term}%"))
    destinations = query.paginate(page=page, per_page=15)
    return render_template(
        "destination_list.html", destinations=destinations, search_term=search_term
    )


@admin_bp.route("/destinations/new", methods=["GET", "POST"])
@admin_required
def add_destination():
    form = DestinationForm()
    if form.validate_on_submit():
        opening_hours_obj = None
        if form.opening_hours.data:
            try:
                opening_hours_obj = json.loads(form.opening_hours.data)
            except json.JSONDecodeError:
                flash("Format JSON untuk Jam Buka tidak valid.", "danger")
                return render_template(
                    "destination_form.html", form=form, form_title="Buat Destinasi Baru"
                )

        new_destination = Destination(
            name=form.name.data,
            description=form.description.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            address=form.address.data,
            city=form.city.data,
            country=form.country.data,
            category=form.category.data,
            tags=form.tags.data,
            image_url=form.image_url.data,
            avg_rating=form.avg_rating.data,
            opening_hours=opening_hours_obj,
            typical_visit_duration_minutes=form.typical_visit_duration_minutes.data,
        )
        db.session.add(new_destination)
        db.session.commit()
        flash(f'Destinasi "{new_destination.name}" berhasil dibuat.', "success")
        return redirect(url_for(".destinations_list"))

    return render_template(
        "destination_form.html", form=form, form_title="Buat Destinasi Baru"
    )


@admin_bp.route("/destinations/edit/<int:destination_id>", methods=["GET", "POST"])
@admin_required
def edit_destination(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    form = DestinationForm(obj=destination)

    if form.validate_on_submit():
        opening_hours_obj = None
        if form.opening_hours.data:
            try:
                opening_hours_obj = json.loads(form.opening_hours.data)
            except json.JSONDecodeError:
                flash("Format JSON untuk Jam Buka tidak valid.", "danger")
                return render_template(
                    "destination_form.html",
                    form=form,
                    form_title=f"Edit Destinasi: {destination.name}",
                )

        destination.name = form.name.data
        destination.description = form.description.data
        destination.latitude = form.latitude.data
        destination.longitude = form.longitude.data
        destination.address = form.address.data
        destination.city = form.city.data
        destination.country = form.country.data
        destination.category = form.category.data
        destination.tags = form.tags.data
        destination.image_url = form.image_url.data
        destination.avg_rating = form.avg_rating.data
        destination.opening_hours = opening_hours_obj
        destination.typical_visit_duration_minutes = (
            form.typical_visit_duration_minutes.data
        )

        db.session.commit()
        flash(f'Destinasi "{destination.name}" berhasil diperbarui.', "success")
        return redirect(url_for(".destinations_list"))

    if destination.opening_hours:
        form.opening_hours.data = json.dumps(destination.opening_hours, indent=4)

    return render_template(
        "destination_form.html",
        form=form,
        form_title=f"Edit Destinasi: {destination.name}",
    )


@admin_bp.route("/destinations/delete/<int:destination_id>", methods=["POST"])
@admin_required
def delete_destination(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    # Tambahkan pengecekan jika destinasi masih dipakai di itinerary (opsional)
    if ItineraryItem.query.filter_by(destination_id=destination_id).first():
        flash(
            f'Destinasi "{destination.name}" tidak dapat dihapus karena masih digunakan dalam itinerary.',
            "danger",
        )
        return redirect(url_for(".destinations_list"))

    db.session.delete(destination)
    db.session.commit()
    flash(f'Destinasi "{destination.name}" berhasil dihapus.', "success")
    return redirect(url_for(".destinations_list"))


@admin_bp.route("/destinations/import", methods=["POST"])
@admin_required
def import_destinations():
    if "file" not in request.files:
        flash("Tidak ada file yang dipilih.", "danger")
        return redirect(url_for(".destinations_list"))

    file = request.files["file"]

    if file.filename == "":
        flash("Tidak ada file yang dipilih.", "danger")
        return redirect(url_for(".destinations_list"))

    # Validasi tipe file
    allowed_extensions = {"csv", "txt"}
    if (
        "." not in file.filename
        or file.filename.rsplit(".", 1)[1].lower() not in allowed_extensions
    ):
        flash("Tipe file tidak diizinkan. Harap unggah file .csv atau .txt.", "danger")
        return redirect(url_for(".destinations_list"))

    # Membaca file
    # Kita gunakan io.TextIOWrapper untuk membaca stream byte sebagai teks
    try:
        stream = io.TextIOWrapper(file.stream._file, "UTF-8", newline=None)
        # Gunakan DictReader untuk membaca baris sebagai dictionary berdasarkan header
        csv_reader = csv.DictReader(stream)

        destinations_to_add = []
        errors = []
        line_num = 1

        # Kolom yang wajib ada di header file
        required_headers = {"name", "latitude", "longitude"}

        # Cek header
        if not required_headers.issubset(set(csv_reader.fieldnames)):
            missing = required_headers - set(csv_reader.fieldnames)
            flash(
                f"Header file tidak lengkap. Kolom berikut tidak ditemukan: {', '.join(missing)}",
                "danger",
            )
            return redirect(url_for(".destinations_list"))

        for row in csv_reader:
            line_num += 1
            # Validasi data per baris
            if (
                not row.get("name")
                or not row.get("latitude")
                or not row.get("longitude")
            ):
                errors.append(
                    f"Baris {line_num}: data 'name', 'latitude', dan 'longitude' wajib diisi."
                )
                continue

            # Konversi tipe data dan handle nilai kosong
            try:
                # Untuk field opsional, gunakan .get() dengan default None
                destination_data = {
                    "name": row.get("name"),
                    "description": row.get("description") or None,
                    "latitude": float(row.get("latitude")),
                    "longitude": float(row.get("longitude")),
                    "address": row.get("address") or None,
                    "city": row.get("city") or None,
                    "country": row.get("country") or None,
                    "category": row.get("category") or None,
                    "tags": row.get("tags") or None,
                    "image_url": row.get("image_url") or None,
                    "avg_rating": float(row.get("avg_rating"))
                    if row.get("avg_rating")
                    else None,
                    "opening_hours": json.loads(row.get("opening_hours"))
                    if row.get("opening_hours")
                    else None,
                    "typical_visit_duration_minutes": int(
                        row.get("typical_visit_duration_minutes")
                    )
                    if row.get("typical_visit_duration_minutes")
                    else None,
                }
                destinations_to_add.append(Destination(**destination_data))
            except (ValueError, TypeError, json.JSONDecodeError) as e:
                errors.append(f"Baris {line_num}: Format data salah. Error: {e}")
                continue

        if errors:
            # Jika ada error, jangan simpan apa pun dan tampilkan error
            for error in errors:
                flash(error, "danger")
        else:
            # Jika tidak ada error, coba simpan ke database
            try:
                db.session.bulk_save_objects(destinations_to_add)
                db.session.commit()
                flash(
                    f"{len(destinations_to_add)} destinasi berhasil diimpor.", "success"
                )
            except IntegrityError as e:
                db.session.rollback()
                flash(
                    f"Gagal menyimpan data karena ada data duplikat atau error database. Error: {e.orig}",
                    "danger",
                )
            except Exception as e:
                db.session.rollback()
                flash(
                    f"Terjadi kesalahan tak terduga saat menyimpan data. Error: {e}",
                    "danger",
                )

    except Exception as e:
        flash(f"Gagal memproses file. Error: {e}", "danger")

    return redirect(url_for(".destinations_list"))


@admin_bp.route("/itineraries")
@admin_required
def itineraries_list():
    page = request.args.get("page", 1, type=int)
    itineraries = Itinerary.query.order_by(Itinerary.created_at.desc()).paginate(
        page=page, per_page=15
    )
    return render_template("itinerary_list.html", itineraries=itineraries)

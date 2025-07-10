from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")

    if not username or not email or not password:
        return jsonify({"msg": "Username, email, dan password dibutuhkan"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username sudah digunakan"}), 409  # 409 Conflic

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email sudah terdaftar"}), 409

    new_user = User(username=username, email=email, full_name=full_name)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return (
            jsonify({"msg": "User berhasil dibuat", "user_id": new_user.user_id}),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Gagal membuat user", "error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Email dan password dibutuhkan"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.user_id))
        return (
            jsonify(
                access_token=access_token, user_id=user.user_id, username=user.username
            ),
            200,
        )
    else:
        return jsonify({"msg": "Email atau password salah"}), 401


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(logged_in_as=user.username, user_id=user.user_id), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_user_profile():
    current_user_id_str = get_jwt_identity()
    try:
        curren_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"msg": "Invalid User ID format in token"}), 422

    user = User.query.get(curren_user_id)

    if not user:
        return jsonify({"msg": "User tidak ditemukan"}), 404

    return jsonify(
        {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "profile_picture_url": user.profile_picture_url,
            "created_at": user.created_at.isoformat(),
        }
    )


@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_user_profile():
    current_user_id_str = get_jwt_identity()
    try:
        current_user_id = int(current_user_id_str)
    except ValueError:
        return jsonify({"msg": "Invalid user ID format in token"}), 422

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User tidak ditemukan"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"msg": "Tidak ada data yang dikirim"}), 400

    updated_fields = []

    if "full_name" in data:
        user.full_name = data["full_name"]
        updated_fields.append("Nama lengkap")

    if "new_password" in data and data["new_password"]:
        current_password_input = data.get("current_password")
        new_password = data["new_password"]

        if not current_password_input:
            return (
                jsonify(
                    {"msg": "Password saat ini dibutuhkan untuk mengubah password"}
                ),
                400,
            )

        if not user.check_password(
            current_password_input
        ): 
            return jsonify({"msg": "Password saat ini salah"}), 400

        # Validasi panjang password baru, dll. bisa ditambahkan di sini
        if len(new_password) < 6:
            return jsonify({"msg": "Password baru minimal 6 karakter"}), 400

        user.set_password(new_password)
        updated_fields.append("Password")
    elif ("current_password" in data and data["current_password"]) and not (
        "new_password" in data and data["new_password"]
    ):
        # Jika current_password diisi tapi new_password tidak
        return (
            jsonify(
                {"msg": "Password baru juga harus diisi jika ingin mengubah password."}
            ),
            400,
        )

    if not updated_fields:
        return (
            jsonify(
                {
                    "msg": "Tidak ada field yang diupdate. Kirim 'full_name' atau ('current_password' dan 'new_password')."
                }
            ),
            400,
        )

    try:
        db.session.commit()
        updated_user_data = {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "profile_picture_url": user.profile_picture_url,
            "created_at": user.created_at.isoformat(),
        }
        return (
            jsonify(
                {
                    "msg": f"{', '.join(updated_fields)} berhasil diperbarui.",
                    "user": updated_user_data,
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Gagal memperbarui profil", "error": str(e)}), 500

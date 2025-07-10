import json
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    DecimalField,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Optional,
    URL,
    NumberRange,
    ValidationError,
)


class UserAdminForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    full_name = StringField("Nama Lengkap")
    is_admin = BooleanField("Jadikan Admin?")

    password = PasswordField(
        "Password",
        validators=[
            Optional(),
            EqualTo("confirm_password", message="Password must mastch"),
        ],
    )
    confirm_password = PasswordField("Konfirmasi Password")

    submit = SubmitField("Simpan")


class UserAdminEditForm(UserAdminForm):
    pass


def OptionalJson(form, field):
    if field.data:
        try:
            json.loads(field.data)
        except json.JSONDecodeError:
            raise ValidationError("Format JSON tidak valid.")


class DestinationForm(FlaskForm):
    name = StringField(
        "Nama Destinasi",
        validators=[DataRequired(message="Nama destinasi tidak boleh kosong.")],
    )

    description = TextAreaField("Deskripsi")

    latitude = DecimalField(
        "Latitude",
        validators=[
            DataRequired(message="Latitude tidak boleh kosong."),
            NumberRange(min=-90, max=90),
        ],
        places=8,
    )
    longitude = DecimalField(
        "Longitude",
        validators=[
            DataRequired(message="Longitude tidak boleh kosong."),
            NumberRange(min=-180, max=180),
        ],
        places=8,
    )

    address = TextAreaField("Alamat")
    city = StringField("Kota")
    country = StringField("Negara")
    category = StringField("Kategori", description="Contoh: Alam, Sejarah, Kuliner")
    tags = StringField(
        "Tags",
        description="Pisahkan dengan koma, contoh: pantai, sunset, ramah keluarga",
    )

    image_url = StringField(
        "URL Gambar", validators=[Optional(), URL(message="URL gambar tidak valid.")]
    )

    avg_rating = DecimalField(
        "Rating Rata-rata",
        validators=[
            Optional(),
            NumberRange(min=0, max=5, message="Rating harus antara 0 dan 5."),
        ],
        places=2,
    )

    opening_hours = TextAreaField(
        "Jam Buka (JSON)",
        validators=[OptionalJson],
        description='Gunakan format JSON, contoh: {"default": "09:00-17:00", "sunday": "Tutup"}',
    )

    typical_visit_duration_minutes = IntegerField(
        "Estimasi Durasi Kunjungan (menit)",
        validators=[
            Optional(),
            NumberRange(min=0, message="Durasi harus angka positif."),
        ],
    )

    submit = SubmitField("Simpan Destinasi")

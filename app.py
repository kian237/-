

import os
import sqlite3
import uuid
from datetime import datetime

from flask import (
    Flask, request, redirect, url_for,
    render_template_string, flash
)
from werkzeug.utils import secure_filename


# ==========================================
# تنظیمات اصلی
# ==========================================

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "amlakan-iran-secret-key")

DATABASE = "amlakan.db"
UPLOAD_FOLDER = os.path.join("static", "uploads")

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# دیتابیس
# ==========================================

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            city TEXT,
            price TEXT,
            area TEXT,
            rooms TEXT,
            kind TEXT,
            image TEXT,
            description TEXT,
            created_at TEXT
        )
    """)

    # اضافه کردن ستون‌های جدید به دیتابیس قدیمی
    new_columns = {
        "property_type": "TEXT DEFAULT 'آپارتمان'",
        "address": "TEXT DEFAULT ''",
        "floor": "TEXT DEFAULT ''",
        "building_age": "TEXT DEFAULT ''",
        "parking": "TEXT DEFAULT 'ندارد'",
        "elevator": "TEXT DEFAULT 'ندارد'",
        "warehouse": "TEXT DEFAULT 'ندارد'"
    }

    existing_columns = [
        row["name"]
        for row in db.execute(
            "PRAGMA table_info(properties)"
        ).fetchall()
    ]

    for column, definition in new_columns.items():
        if column not in existing_columns:
            db.execute(
                f"ALTER TABLE properties ADD COLUMN {column} {definition}"
            )

    db.commit()

    # آگهی‌های نمونه، فقط در اولین اجرای دیتابیس
    count = db.execute(
        "SELECT COUNT(*) FROM properties"
    ).fetchone()[0]

    if count == 0:
        samples = [
            (
                "آپارتمان لوکس و نورگیر",
                "تهران",
                "۸,۵۰۰,۰۰۰,۰۰۰ تومان",
                "۱۲۰",
                "۳",
                "فروش",
                "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=900",
                "آپارتمان زیبا با طراحی مدرن و نورگیری عالی",
                "۱۴۰۵/۰۸/۲۶",
                "آپارتمان",
                "تهران، منطقه ۲",
                "۳",
                "۵",
                "دارد",
                "دارد",
                "دارد"
            ),
            (
                "خانه ویلایی با حیاط بزرگ",
                "کرج",
                "۶,۰۰۰,۰۰۰,۰۰۰ تومان",
                "۲۰۰",
                "۴",
                "فروش",
                "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=900",
                "خانه ویلایی با حیاط زیبا و پارکینگ",
                "۱۴۰۵/۰۸/۲۶",
                "خانه ویلایی",
                "کرج، مهرشهر",
                "همکف",
                "۸",
                "دارد",
                "ندارد",
                "دارد"
            )
        ]

        db.executemany("""
            INSERT INTO properties (
                title, city, price, area, rooms, kind,
                image, description, created_at,
                property_type, address, floor, building_age,
                parking, elevator, warehouse
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, samples)

        db.commit()

    db.close()


init_db()


# ==========================================
# ابزارهای کمکی
# ==========================================

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def image_src(property_item):
    image = property_item["image"] or ""

    if image.startswith("http://") or image.startswith("https://"):
        return image

    return url_for("static", filename=image)


def get_properties():
    db = get_db()
    properties = db.execute(
        "SELECT * FROM properties ORDER BY id DESC"
    ).fetchall()
    db.close()
    return properties


# ==========================================
# طراحی و استایل سایت
# ==========================================

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #101827;
    --card: #1b293b;
    --gold: #f5b942;
    --text: #f8fafc;
    --muted: #aab7c8;
    --header-bg: #142033;
    --input-bg: #111d2d;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: 'Vazirmatn', Tahoma, sans-serif;
    direction: rtl;
    transition: background .4s, color .4s;
}

a {
    color: inherit;
    text-decoration: none;
}

button, input, select, textarea {
    font-family: inherit;
}

header {
    background: var(--header-bg);
    padding: 16px 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
    border-bottom: 1px solid #ffffff12;
    position: sticky;
    top: 0;
    z-index: 20;
}

.logo {
    font-size: 25px;
    font-weight: 900;
    background: linear-gradient(90deg,#f5b942,#ff6b6b,#5eead4,#f5b942);
    background-size: 300%;
    -webkit-background-clip: text;
    color: transparent;
    animation: logoColor 5s linear infinite;
}

@keyframes logoColor {
    0% { background-position: 0%; }
    100% { background-position: 300%; }
}

.nav-links {
    display: flex;
    gap: 22px;
    flex-wrap: wrap;
    align-items: center;
}

.nav-links a {
    color: var(--muted);
    font-size: 14px;
}

.nav-links a:hover {
    color: var(--gold);
}

.btn {
    background: var(--gold);
    color: #172033;
    border: 0;
    padding: 11px 20px;
    border-radius: 12px;
    font-weight: 800;
    cursor: pointer;
    display: inline-block;
    text-align: center;
}

.btn:hover {
    filter: brightness(1.08);
    transform: translateY(-1px);
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: auto;
}

.hero {
    padding: 75px 25px;
    text-align: center;
    background:
        linear-gradient(120deg,#172b45ee,#182a3eee),
        url("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1500") center/cover;
    border-radius: 0 0 30px 30px;
}

.hero h1 {
    font-size: clamp(28px,5vw,45px);
    margin: 0 0 15px;
}

.hero p {
    color: #d0d9e7;
    margin-bottom: 25px;
}

.search-box {
    max-width: 750px;
    margin: 30px auto 0;
    display: flex;
    gap: 10px;
    background: #ffffff12;
    padding: 12px;
    border-radius: 15px;
}

.search-box input {
    flex: 1;
    min-width: 0;
    background: white;
    color: #172033;
    border: none;
    padding: 13px;
    border-radius: 10px;
    outline: none;
}

.section-title {
    margin: 45px 0 22px;
    font-size: 25px;
}

.property-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit,minmax(250px,1fr));
    gap: 22px;
    padding-bottom: 45px;
}

.property-card {
    background: var(--card);
    border: 1px solid #ffffff12;
    border-radius: 18px;
    overflow: hidden;
    transition: .25s;
}

.property-card:hover {
    transform: translateY(-5px);
    border-color: var(--gold);
}

.property-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    background: #26374b;
}

.card-content {
    padding: 17px;
}

.card-content h3 {
    margin: 0 0 12px;
    font-size: 18px;
}

.muted {
    color: var(--muted);
    font-size: 13px;
}

.price {
    color: var(--gold);
    font-size: 17px;
    font-weight: 900;
    margin: 15px 0;
}

.tag {
    display: inline-block;
    background: #f5b94220;
    color: var(--gold);
    border-radius: 8px;
    padding: 5px 10px;
    font-size: 12px;
}

.form-card, .detail-card {
    background: var(--card);
    border: 1px solid #ffffff12;
    padding: 25px;
    border-radius: 20px;
    margin: 35px auto;
    max-width: 900px;
}

.form-grid, .info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit,minmax(210px,1fr));
    gap: 17px;
}

.field {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.field label {
    color: var(--muted);
    font-size: 13px;
}

.field input, .field select, .field textarea {
    background: var(--input-bg);
    border: 1px solid #ffffff20;
    border-radius: 10px;
    padding: 13px;
    color: var(--text);
    outline: none;
    width: 100%;
}

.field input:focus, .field select:focus, .field textarea:focus {
    border-color: var(--gold);
}

.field textarea {
    min-height: 120px;
    resize: vertical;
}

.full {
    grid-column: 1 / -1;
}

.preview {
    width: 100%;
    max-height: 260px;
    object-fit: cover;
    border-radius: 12px;
    display: none;
    margin-top: 12px;
}

.detail-image {
    width: 100%;
    max-height: 450px;
    object-fit: cover;
    border-radius: 15px;
}

.info-item {
    background: var(--input-bg);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #ffffff10;
}

.info-item span {
    display: block;
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 7px;
}

.info-item strong {
    font-size: 15px;
}

.notice {
    background: #f5b94218;
    color: var(--gold);
    padding: 13px;
    border-radius: 10px;
    margin: 15px 0;
}

footer {
    text-align: center;
    padding: 30px;
    color: var(--muted);
    border-top: 1px solid #ffffff12;
    margin-top: 40px;
}

.theme-panel {
    position: fixed;
    left: 15px;
    bottom: 15px;
    z-index: 50;
}

.theme-toggle {
    border: none;
    border-radius: 50%;
    width: 52px;
    height: 52px;
    background: var(--gold);
    font-size: 23px;
    cursor: pointer;
}

.theme-content {
    display: none;
    background: var(--card);
    border: 1px solid #ffffff30;
    border-radius: 15px;
    padding: 16px;
    width: 240px;
    margin-bottom: 10px;
    box-shadow: 0 10px 40px #0005;
}

.theme-content.show {
    display: block;
}

.theme-content button {
    border: 0;
    padding: 8px;
    border-radius: 8px;
    margin: 4px;
    cursor: pointer;
}

.theme-content input[type=color] {
    width: 100%;
    height: 38px;
    margin: 7px 0;
}

.flash {
    background: #1d8055;
    padding: 12px;
    border-radius: 10px;
    margin: 15px 0;
}

@media(max-width:650px) {
    header {
        justify-content: center;
    }
    .nav-links {
        justify-content: center;
    }
    .hero {
        padding: 50px 15px;
    }
    .search-box {
        flex-direction: column;
    }
    .form-card, .detail-card {
        padding: 17px;
    }
}
</style>
"""


# ==========================================
# هدر و پنل رنگ
# ==========================================

HEADER = """
<header>
    <a href="/" class="logo">املاکان ایران</a>

    <nav class="nav-links">
        <a href="/">🏠 صفحه اصلی</a>
        <a href="/#properties">🏢 مشاهده املاک</a>
        <a href="/add">➕ ثبت آگهی</a>
    </nav>

    <a href="/add" class="btn">+ ثبت آگهی رایگان</a>
</header>

<div class="theme-panel">
    <div class="theme-content" id="themeContent">
        <strong>🎨 تنظیم رنگ سایت</strong>
        <p class="muted">رنگ دلخواه خودت را انتخاب کن</p>

        <label>پس زمینه</label>
        <input type="color" id="bgColor" value="#101827">

        <label>رنگ کارت‌ها</label>
        <input type="color" id="cardColor" value="#1b293b">

        <label>رنگ اصلی</label>
        <input type="color" id="goldColor" value="#f5b942">

        <button onclick="saveTheme()">ذخیره رنگ‌ها</button>
        <button onclick="resetTheme()">بازنشانی</button>
    </div>

    <button class="theme-toggle" onclick="toggleTheme()">🎨</button>
</div>

<script>
function toggleTheme() {
    document.getElementById("themeContent").classList.toggle("show");
}

function saveTheme() {
    const theme = {
        bg: document.getElementById("bgColor").value,
        card: document.getElementById("cardColor").value,
        gold: document.getElementById("goldColor").value
    };

    localStorage.setItem("amlakan_personal_theme", JSON.stringify(theme));
    applyTheme(theme);
}

function applyTheme(theme) {
    document.documentElement.style.setProperty("--bg", theme.bg);
    document.documentElement.style.setProperty("--card", theme.card);
    document.documentElement.style.setProperty("--gold", theme.gold);
}

function resetTheme() {
    localStorage.removeItem("amlakan_personal_theme");
    applyTheme({
        bg: "#101827",
        card: "#1b293b",
        gold: "#f5b942"
    });
}

try {
    const saved = localStorage.getItem("amlakan_personal_theme");
    if (saved) applyTheme(JSON.parse(saved));
} catch (e) {
    console.log("Theme settings unavailable");
}
</script>
"""


# ==========================================
# قالب پایه
# ==========================================

BASE_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page_title }} | املاکان ایران</title>
    {{ style|safe }}
</head>
<body>
    {{ header|safe }}

    <main class="container">
        {% with messages = get_flashed_messages() %}
            {% for message in messages %}
                <div class="flash">{{ message }}</div>
            {% endfor %}
        {% endwith %}

        {{ content|safe }}
    </main>

    <footer>
        © املاکان ایران - سامانه خرید، فروش و اجاره ملک
    </footer>
</body>
</html>
"""


def render_page(template, page_title="صفحه اصلی", **context):
    rendered = render_template_string(template, **context)

    return render_template_string(
        BASE_HTML,
        page_title=page_title,
        style=STYLE,
        header=HEADER,
        content=rendered
    )


# ==========================================
# صفحه اصلی
# ==========================================

HOME_HTML = """
<section class="hero">
    <h1>خانه رویایی‌ات را پیدا کن 🏡</h1>
    <p>خرید، فروش و اجاره ملک در سراسر ایران</p>

    <a href="/add" class="btn">➕ همین حالا آگهی ثبت کن</a>

    <form action="/" method="GET" class="search-box">
        <input
            type="text"
            name="q"
            placeholder="نام ملک یا شهر را وارد کن..."
            value="{{ search }}"
        >
        <button class="btn" type="submit">جست‌وجو 🔍</button>
    </form>
</section>

<div id="properties">
    <h2 class="section-title">🏢 جدیدترین آگهی‌های املاک</h2>

    {% if properties %}
    <div class="property-grid">
        {% for p in properties %}
        <a href="/property/{{ p['id'] }}" class="property-card">
            <img src="{{ image_src(p) }}" alt="{{ p['title'] }}">

            <div class="card-content">
                <span class="tag">{{ p['kind'] }}</span>
                <h3>{{ p['title'] }}</h3>

                <div class="muted">
                    📍 {{ p['city'] }} |
                    🏠 {{ p['property_type'] or 'ملک' }}
                </div>

                <div class="muted">
                    📐 {{ p['area'] }} متر |
                    🛏️ {{ p['rooms'] }} اتاق
                </div>

                <div class="price">{{ p['price'] }}</div>
                <span class="btn">مشاهده جزئیات</span>
            </div>
        </a>
        {% endfor %}
    </div>
    {% else %}
        <div class="notice">آگهی‌ای پیدا نشد. عبارت دیگری را جست‌وجو کن.</div>
    {% endif %}
</div>

<div style="text-align:center;margin:30px 0 60px">
    <h2>ملک خودت را برای هزاران نفر معرفی کن!</h2>
    <p class="muted">ثبت آگهی در املاکان ایران را شروع کن.</p>
    <a href="/add" class="btn">➕ ثبت آگهی رایگان</a>
</div>
"""


@app.route("/")
def home():
    search = request.args.get("q", "").strip()

    db = get_db()

    if search:
        properties = db.execute("""
            SELECT * FROM properties
            WHERE title LIKE ?
               OR city LIKE ?
               OR property_type LIKE ?
            ORDER BY id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        )).fetchall()
    else:
        properties = db.execute(
            "SELECT * FROM properties ORDER BY id DESC"
        ).fetchall()

    db.close()

    return render_page(
        HOME_HTML,
        page_title="صفحه اصلی",
        properties=properties,
        search=search,
        image_src=image_src
    )


# ==========================================
# فرم کامل ثبت آگهی
# ==========================================

ADD_HTML = """
<div class="form-card">
    <h1>➕ ثبت آگهی ملک</h1>

    <p class="muted">
        اطلاعات ملک خود را با دقت وارد کن تا آگهی در سایت نمایش داده شود.
    </p>

    <div class="notice">
        همه اطلاعات را درست وارد کن. عکس ملک باید حداکثر ۵ مگابایت باشد.
    </div>

    <form action="/add" method="POST" enctype="multipart/form-data">

        <div class="form-grid">

            <div class="field full">
                <label>عنوان آگهی *</label>
                <input name="title" required
                       placeholder="مثلاً آپارتمان ۱۲۰ متری در تهران">
            </div>

            <div class="field">
                <label>نوع ملک *</label>
                <select name="property_type" required>
                    <option value="آپارتمان">آپارتمان</option>
                    <option value="خانه ویلایی">خانه ویلایی</option>
                    <option value="زمین">زمین</option>
                    <option value="مغازه">مغازه</option>
                    <option value="دفتر کار">دفتر کار</option>
                    <option value="باغ">باغ</option>
                    <option value="سایر">سایر</option>
                </select>
            </div>

            <div class="field">
                <label>نوع معامله *</label>
                <select name="kind" required>
                    <option value="فروش">فروش</option>
                    <option value="اجاره">اجاره</option>
                    <option value="رهن">رهن</option>
                </select>
            </div>

            <div class="field">
                <label>استان و شهر *</label>
                <input name="city" required placeholder="مثلاً تهران">
            </div>

            <div class="field">
                <label>آدرس ملک</label>
                <input name="address" placeholder="محله، خیابان و ...">
            </div>

            <div class="field">
                <label>متراژ (متر مربع) *</label>
                <input name="area" type="number" min="1" required>
            </div>

            <div class="field">
                <label>تعداد اتاق</label>
                <input name="rooms" type="number" min="0" value="0">
            </div>

            <div class="field">
                <label>طبقه</label>
                <input name="floor" placeholder="مثلاً طبقه سوم">
            </div>

            <div class="field">
                <label>سن بنا (سال)</label>
                <input name="building_age" type="number" min="0" value="0">
            </div>

            <div class="field">
                <label>پارکینگ</label>
                <select name="parking">
                    <option value="دارد">دارد</option>
                    <option value="ندارد">ندارد</option>
                </select>
            </div>

            <div class="field">
                <label>آسانسور</label>
                <select name="elevator">
                    <option value="دارد">دارد</option>
                    <option value="ندارد">ندارد</option>
                </select>
            </div>

            <div class="field">
                <label>انباری</label>
                <select name="warehouse">
                    <option value="دارد">دارد</option>
                    <option value="ندارد">ندارد</option>
                </select>
            </div>

            <div class="field full">
                <label>قیمت یا مبلغ معامله *</label>
                <input name="price" required
                       placeholder="مثلاً ۵ میلیارد تومان">
            </div>

            <div class="field full">
                <label>عکس ملک</label>
                <input
                    type="file"
                    name="image"
                    id="imageInput"
                    accept=".jpg,.jpeg,.png,.webp"
                >
                <img id="imagePreview" class="preview" alt="پیش‌نمایش عکس">
                <small class="muted">
                    فرمت‌های مجاز: JPG، JPEG، PNG و WEBP
                </small>
            </div>

            <div class="field full">
                <label>توضیحات کامل ملک</label>
                <textarea name="description"
                          placeholder="توضیحات ملک، امکانات، شرایط معامله و ..."></textarea>
            </div>

            <div class="field full">
                <button class="btn" type="submit">
                    ثبت نهایی آگهی
                </button>
            </div>

        </div>
    </form>
</div>

<script>
const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");

imageInput.addEventListener("change", function() {
    const file = this.files[0];

    if (!file) {
        imagePreview.style.display = "none";
        return;
    }

    if (file.size > 5 * 1024 * 1024) {
        alert("حجم عکس باید کمتر از ۵ مگابایت باشد.");
        this.value = "";
        imagePreview.style.display = "none";
        return;
    }

    imagePreview.src = URL.createObjectURL(file);
    imagePreview.style.display = "block";
});
</script>
"""


# ==========================================
# ثبت آگهی در دیتابیس
# ==========================================

@app.route("/add", methods=["GET", "POST"])
def add_property():

    if request.method == "GET":
        return render_page(
            ADD_HTML,
            page_title="ثبت آگهی"
        )

    title = request.form.get("title", "").strip()
    city = request.form.get("city", "").strip()
    price = request.form.get("price", "").strip()
    area = request.form.get("area", "").strip()
    rooms = request.form.get("rooms", "0").strip()
    kind = request.form.get("kind", "فروش")
    description = request.form.get("description", "").strip()

    property_type = request.form.get("property_type", "آپارتمان")
    address = request.form.get("address", "").strip()
    floor = request.form.get("floor", "").strip()
    building_age = request.form.get("building_age", "").strip()
    parking = request.form.get("parking", "ندارد")
    elevator = request.form.get("elevator", "ندارد")
    warehouse = request.form.get("warehouse", "ندارد")

    if not title or not city or not price or not area:
        flash("لطفاً فیلدهای ضروری را تکمیل کن.")
        return redirect(url_for("add_property"))

    try:
        if int(area) < 1 or int(rooms) < 0 or int(building_age or 0) < 0:
            raise ValueError
    except ValueError:
        flash("متراژ، تعداد اتاق و سن بنا باید عدد معتبر باشند.")
        return redirect(url_for("add_property"))

    image = ""

    uploaded_file = request.files.get("image")

    if uploaded_file and uploaded_file.filename:
        if not allowed_file(uploaded_file.filename):
            flash("فرمت عکس مجاز نیست.")
            return redirect(url_for("add_property"))

        extension = uploaded_file.filename.rsplit(".", 1)[1].lower()
        filename = secure_filename(str(uuid.uuid4()) + "." + extension)

        uploaded_file.save(
            os.path.join(app.config["UPLOAD_FOLDER"], filename)
        )

        image = "uploads/" + filename

    db = get_db()

    db.execute("""
        INSERT INTO properties (
            title, city, price, area, rooms, kind,
            image, description, created_at,
            property_type, address, floor, building_age,
            parking, elevator, warehouse
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title, city, price, area, rooms, kind,
        image, description,
        datetime.now().strftime("%Y-%m-%d"),
        property_type, address, floor, building_age,
        parking, elevator, warehouse
    ))

    db.commit()
    db.close()

    flash("آگهی با موفقیت ثبت شد.")
    return redirect(url_for("home"))


# ==========================================
# صفحه جزئیات ملک
# ==========================================

DETAIL_HTML = """
<div class="detail-card">

    <img class="detail-image"
         src="{{ image_src(property) }}"
         alt="{{ property['title'] }}">

    <h1>{{ property['title'] }}</h1>

    <span class="tag">{{ property['kind'] }}</span>

    <div class="price">{{ property['price'] }}</div>

    <div class="info-grid">

        <div class="info-item">
            <span>نوع ملک</span>
            <strong>{{ property['property_type'] or 'ثبت نشده' }}</strong>
        </div>

        <div class="info-item">
            <span>شهر</span>
            <strong>{{ property['city'] }}</strong>
        </div>

        <div class="info-item">
            <span>آدرس</span>
            <strong>{{ property['address'] or 'ثبت نشده' }}</strong>
        </div>

        <div class="info-item">
            <span>متراژ</span>
            <strong>{{ property['area'] }} متر</strong>
        </div>

        <div class="info-item">
            <span>تعداد اتاق</span>
            <strong>{{ property['rooms'] }}</strong>
        </div>

        <div class="info-item">
            <span>طبقه</span>
            <strong>{{ property['floor'] or 'ثبت نشده' }}</strong>
        </div>

        <div class="info-item">
            <span>سن بنا</span>
            <strong>{{ property['building_age'] or 'ثبت نشده' }} سال</strong>
        </div>

        <div class="info-item">
            <span>پارکینگ</span>
            <strong>{{ property['parking'] or 'ثبت نشده' }}</strong>
        </div>

        <div class="info-item">
            <span>آسانسور</span>
            <strong>{{ property['elevator'] or 'ثبت نشده' }}</strong>
        </div>

        <div class="info-item">
            <span>انباری</span>
            <strong>{{ property['warehouse'] or 'ثبت نشده' }}</strong>
        </div>

        <div class="info-item">
            <span>تاریخ ثبت</span>
            <strong>{{ property['created_at'] }}</strong>
        </div>

    </div>

    <h2>توضیحات ملک</h2>

    <p style="line-height:2;color:var(--muted)">
        {{ property['description'] or 'توضیحی ثبت نشده است.' }}
    </p>

    <a href="/" class="btn">بازگشت به صفحه اصلی</a>

</div>
"""


@app.route("/property/<int:property_id>")
def property_detail(property_id):

    db = get_db()

    property_item = db.execute(
        "SELECT * FROM properties WHERE id = ?",
        (property_id,)
    ).fetchone()

    db.close()

    if property_item is None:
        return "ملک موردنظر پیدا نشد.", 404

    return render_page(
        DETAIL_HTML,
        page_title=property_item["title"],
        property=property_item,
        image_src=image_src
    )


# ==========================================
# مدیریت خطای حجم فایل
# ==========================================

@app.errorhandler(413)
def file_too_large(error):
    return render_page(
        """
        <div class="form-card">
            <h2>حجم فایل بیش از حد مجاز است!</h2>
            <p>لطفاً عکسی با حجم کمتر از ۵ مگابایت انتخاب کن.</p>
            <a href="/add" class="btn">بازگشت به ثبت آگهی</a>
        </div>
        """,
        page_title="حجم فایل زیاد است"
    ), 413


# ==========================================
# اجرای برنامه
# ==========================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )

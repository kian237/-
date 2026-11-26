


from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = "amlakan.db"


# =====================================
# DATABASE
# =====================================

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            city TEXT NOT NULL,
            price TEXT NOT NULL,
            area INTEGER NOT NULL,
            rooms INTEGER NOT NULL,
            kind TEXT NOT NULL,
            image TEXT NOT NULL,
            description TEXT,
            created_at TEXT
        )
    """)

    count = db.execute(
        "SELECT COUNT(*) FROM properties"
    ).fetchone()[0]

    if count == 0:
        samples = [
            (
                "آپارتمان لوکس و مدرن",
                "تهران",
                "۱۲ میلیارد تومان",
                500, 3, "فروش",
                "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1000",
                "آپارتمان زیبا با طراحی مدرن، نورگیری عالی و امکانات کامل.",
                datetime.now().strftime("%Y-%m-%d")
            ),
            (
                "ویلای مدرن با استخر",
                "شمال",
                "۱۸ میلیارد تومان",
                300, 4, "فروش",
                "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=1000",
                "ویلای مدرن با محوطه سرسبز، استخر و فضای آرام.",
                datetime.now().strftime("%Y-%m-%d")
            ),
            (
                "خانه شیک و دلباز",
                "اصفهان",
                "۶۰ میلیون تومان",
                120, 2, "اجاره",
                "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=1000",
                "خانه‌ای دلباز با دسترسی مناسب به امکانات شهری.",
                datetime.now().strftime("%Y-%m-%d")
            )
        ]

        db.executemany("""
            INSERT INTO properties
            (title, city, price, area, rooms, kind, image,
             description, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, samples)

    db.commit()
    db.close()


init_db()


# =====================================
# CSS
# =====================================

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #0b0e13;
    --card: #151b25;
    --gold: #e8bd63;
    --text: #ffffff;
    --muted: #a7afbd;
    --header-bg: #080b10ee;
    --input-bg: #0c111a;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: 'Vazirmatn', sans-serif;
    background: var(--bg);
    color: var(--text);
    direction: rtl;
    transition: background .25s, color .25s;
}

a {
    text-decoration: none;
    color: inherit;
}

.container {
    width: 92%;
    max-width: 1250px;
    margin: auto;
}

header {
    padding: 15px 0;
    border-bottom: 1px solid #ffffff14;
    background: var(--header-bg);
    position: sticky;
    top: 0;
    z-index: 10;
    backdrop-filter: blur(15px);
}

.nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 21px;
    font-weight: 900;
}

.logo svg {
    width: 45px;
    height: 45px;
}

.logo-text span {
    color: var(--gold);
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 23px;
    color: #d4d8df;
    font-size: 13px;
}

.nav-links a:hover {
    color: var(--gold);
}

.btn, button, a.button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    border: none;
    border-radius: 9px;
    padding: 8px 14px;
    background: linear-gradient(135deg, var(--gold), #bd8c37);
    color: #17120a;
    font-family: inherit;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    transition: .2s;
}

.btn:hover, button:hover, a.button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 16px #0004;
}

.hero {
    padding: 75px 0 55px;
    text-align: center;
    background:
        linear-gradient(#0b0e13d9, #0b0e13f2),
        url('https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=1600')
        center/cover;
}

.hero h1 {
    font-size: clamp(30px, 5vw, 55px);
    margin: 0 0 15px;
    font-weight: 900;
}

.hero h1 span {
    color: var(--gold);
}

.hero p {
    color: #d1d5dc;
    font-size: 15px;
    margin-bottom: 28px;
}

.search-box {
    max-width: 750px;
    margin: auto;
    background: #ffffff12;
    border: 1px solid #ffffff25;
    border-radius: 14px;
    padding: 9px;
    display: flex;
    gap: 9px;
    backdrop-filter: blur(12px);
}

.search-box input {
    flex: 1;
    min-width: 0;
    background: transparent;
    border: none;
    outline: none;
    color: white;
    padding: 10px;
    font-family: inherit;
    font-size: 14px;
}

.search-box input::placeholder {
    color: #c2c6ce;
}

.section-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 42px 0 23px;
    gap: 15px;
}

.section-title h2 {
    font-size: 23px;
    margin: 0;
}

.gold {
    color: var(--gold);
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 21px;
    padding-bottom: 50px;
}

.card {
    background: var(--card);
    border: 1px solid #ffffff12;
    border-radius: 16px;
    overflow: hidden;
    transition: .3s;
    display: block;
}

.card:hover {
    transform: translateY(-5px);
    border-color: var(--gold);
    box-shadow: 0 15px 35px #0005;
}

.card img {
    width: 100%;
    height: 215px;
    object-fit: cover;
    display: block;
}

.card-content {
    padding: 17px;
}

.card h3 {
    margin: 0 0 12px;
    font-size: 17px;
}

.muted {
    color: var(--muted);
    font-size: 12px;
}

.price {
    color: var(--gold);
    font-size: 17px;
    font-weight: 900;
    margin: 13px 0;
}

.card-footer {
    border-top: 1px solid #ffffff12;
    padding-top: 12px;
    display: flex;
    justify-content: space-between;
    color: #c6cbd3;
    font-size: 12px;
}

.form-box {
    max-width: 700px;
    margin: 45px auto;
    padding: 28px;
    background: var(--card);
    border: 1px solid #ffffff18;
    border-radius: 18px;
}

.form-box h2 {
    margin-top: 0;
    color: var(--gold);
}

.form-box input,
.form-box textarea,
.form-box select {
    width: 100%;
    margin: 8px 0 15px;
    padding: 11px;
    border-radius: 9px;
    border: 1px solid #ffffff20;
    background: var(--input-bg);
    color: var(--text);
    font-family: inherit;
    font-size: 13px;
    outline: none;
}

.form-box label {
    font-size: 13px;
    color: var(--text);
}

.form-box textarea {
    min-height: 120px;
    resize: vertical;
}

.detail {
    margin: 40px auto;
    max-width: 1000px;
    background: var(--card);
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid #ffffff18;
}

.detail img {
    width: 100%;
    max-height: 500px;
    object-fit: cover;
    display: block;
}

.detail-content {
    padding: 28px;
}

.detail-content h1 {
    font-size: 28px;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 14px;
    margin: 23px 0;
}

.info-item {
    background: #ffffff09;
    padding: 16px;
    border-radius: 11px;
}

.info-item small {
    color: var(--muted);
    display: block;
    margin-bottom: 8px;
}

.info-item strong {
    color: var(--gold);
}

.description {
    line-height: 2.2;
    color: var(--text);
}

footer {
    text-align: center;
    padding: 35px 10px;
    color: var(--muted);
    border-top: 1px solid #ffffff15;
    margin-top: 30px;
}

.empty {
    text-align: center;
    color: var(--muted);
    padding: 50px 10px;
}

/* Personal theme panel */

.theme-toggle {
    white-space: nowrap;
}

.theme-panel {
    position: fixed;
    top: 82px;
    left: 4%;
    z-index: 30;
    width: min(340px, 92vw);
    padding: 20px;
    background: var(--card);
    color: var(--text);
    border: 1px solid #ffffff25;
    border-radius: 16px;
    box-shadow: 0 18px 50px #0008;
    display: none;
}

.theme-panel.open {
    display: block;
}

.theme-panel h3 {
    margin: 0 0 14px;
    color: var(--gold);
}

.theme-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin: 12px 0;
    font-size: 13px;
}

.theme-panel input[type="color"] {
    width: 52px;
    height: 36px;
    padding: 2px;
    border: 1px solid #ffffff30;
    border-radius: 8px;
    background: transparent;
    cursor: pointer;
}

.theme-presets {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin: 14px 0;
}

.theme-preset {
    min-height: 36px;
    border: 1px solid #ffffff30;
    border-radius: 8px;
    padding: 6px;
    color: white;
    font-family: inherit;
    font-size: 11px;
    cursor: pointer;
}

.theme-actions {
    display: flex;
    gap: 8px;
    margin-top: 14px;
}

.theme-actions button {
    flex: 1;
}

@media(max-width: 650px) {
    .nav-links {
        display: none;
    }

    .hero {
        padding: 50px 0;
    }

    .search-box {
        flex-direction: column;
    }

    .detail-content {
        padding: 19px;
    }

    .btn, button, a.button {
        padding: 7px 12px;
        font-size: 12px;
    }
}
</style>
"""


# =====================================
# HEADER
# =====================================

HEADER = """
<header>
    <div class="container nav">

        <a href="/" class="logo">

            <svg viewBox="0 0 100 100" fill="none"
                 xmlns="http://www.w3.org/2000/svg">

                <defs>
                    <linearGradient id="logoGradient"
                        x1="0" y1="0" x2="100" y2="100">

                        <stop id="logoStop1" offset="0%"
                              stop-color="#f5d58c"/>

                        <stop id="logoStop2" offset="100%"
                              stop-color="#b47d29"/>

                    </linearGradient>
                </defs>

                <path d="M12 48 L50 15 L88 48"
                    stroke="url(#logoGradient)"
                    stroke-width="8"
                    stroke-linecap="round"
                    stroke-linejoin="round"/>

                <path d="M23 44 V85 H77 V44"
                    stroke="url(#logoGradient)"
                    stroke-width="7"
                    stroke-linejoin="round"/>

                <path d="M43 85 V58 H58 V85"
                    stroke="url(#logoGradient)"
                    stroke-width="6"/>

                <circle cx="50" cy="39" r="5"
                    fill="url(#logoGradient)"/>

            </svg>

            <div class="logo-text">
                املاکان <span>ایران</span>
            </div>

        </a>

        <nav class="nav-links">
            <a href="/">صفحه اصلی</a>
            <a href="/#properties">آگهی املاک</a>
            <a href="/add">ثبت آگهی</a>
        </nav>

        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">

            <button type="button"
                    class="btn theme-toggle"
                    id="themeToggle">
                🎨 رنگ سایت
            </button>

            <a href="/add" class="btn">
                ثبت آگهی جدید
            </a>

        </div>

    </div>
</header>

<div class="theme-panel" id="themePanel">

    <h3>تنظیمات ظاهر سایت 🎨</h3>

    <div class="theme-row">
        <label for="themeBg">رنگ پس‌زمینه</label>
        <input type="color" id="themeBg" value="#0b0e13">
    </div>

    <div class="theme-row">
        <label for="themeCard">رنگ کارت‌ها</label>
        <input type="color" id="themeCard" value="#151b25">
    </div>

    <div class="theme-row">
        <label for="themeAccent">رنگ اصلی و دکمه‌ها</label>
        <input type="color" id="themeAccent" value="#e8bd63">
    </div>

    <div class="theme-row">
        <label for="themeText">رنگ نوشته‌ها</label>
        <input type="color" id="themeText" value="#ffffff">
    </div>

    <div class="theme-presets">

        <button class="theme-preset" data-theme="gold"
                style="background:#a77a2c">طلایی</button>

        <button class="theme-preset" data-theme="blue"
                style="background:#2468c5">آبی</button>

        <button class="theme-preset" data-theme="green"
                style="background:#21845a">سبز</button>

        <button class="theme-preset" data-theme="purple"
                style="background:#7042c7">بنفش</button>

        <button class="theme-preset" data-theme="pink"
                style="background:#bd315e">صورتی</button>

        <button class="theme-preset" data-theme="orange"
                style="background:#d35a25">نارنجی</button>

    </div>

    <div class="theme-actions">

        <button type="button" class="btn" id="themeReset">
            رنگ پیش‌فرض
        </button>

        <button type="button" class="btn" id="themeClose">
            بستن
        </button>

    </div>

    <p class="muted">
        تنظیمات فقط در مرورگر شما ذخیره می‌شود.
    </p>

</div>
"""


# =====================================
# JAVASCRIPT
# =====================================

SCRIPTS = """
<script>

// تغییر رنگ لوگو

const logoColors = [
    ["#f5d58c", "#b47d29"],
    ["#76d7ff", "#2468c5"],
    ["#ff8caa", "#bd315e"],
    ["#8de5b0", "#21845a"],
    ["#c6a0ff", "#7042c7"],
    ["#ffb16b", "#d35a25"],
    ["#f7e875", "#b99b19"]
];

let logoIndex = 0;

setInterval(() => {

    logoIndex = (logoIndex + 1) % logoColors.length;

    const stop1 = document.getElementById("logoStop1");
    const stop2 = document.getElementById("logoStop2");

    if (stop1 && stop2) {
        stop1.setAttribute("stop-color", logoColors[logoIndex][0]);
        stop2.setAttribute("stop-color", logoColors[logoIndex][1]);
    }

}, 5000);


// رنگ‌های پیش‌فرض

const defaultTheme = {
    bg: "#0b0e13",
    card: "#151b25",
    accent: "#e8bd63",
    text: "#ffffff"
};


// قالب‌های آماده

const themePresets = {

    gold: {
        bg: "#0b0e13",
        card: "#151b25",
        accent: "#e8bd63",
        text: "#ffffff"
    },

    blue: {
        bg: "#0b1422",
        card: "#14243a",
        accent: "#58a6ff",
        text: "#f4f8ff"
    },

    green: {
        bg: "#0d1b16",
        card: "#183027",
        accent: "#63d69a",
        text: "#f1fff7"
    },

    purple: {
        bg: "#171126",
        card: "#251a3b",
        accent: "#bd9aff",
        text: "#fbf7ff"
    },

    pink: {
        bg: "#21121a",
        card: "#351d2a",
        accent: "#ff8eb5",
        text: "#fff5f8"
    },

    orange: {
        bg: "#21170f",
        card: "#352519",
        accent: "#ffb36b",
        text: "#fff8f0"
    }

};


// عناصر پنل

const themePanel = document.getElementById("themePanel");
const themeToggle = document.getElementById("themeToggle");

const themeInputs = {
    bg: document.getElementById("themeBg"),
    card: document.getElementById("themeCard"),
    accent: document.getElementById("themeAccent"),
    text: document.getElementById("themeText")
};


// اعمال رنگ‌ها

function applyTheme(theme, save = true) {

    const root = document.documentElement;

    root.style.setProperty("--bg", theme.bg);
    root.style.setProperty("--card", theme.card);
    root.style.setProperty("--gold", theme.accent);
    root.style.setProperty("--text", theme.text);

    root.style.setProperty(
        "--muted",
        theme.text === "#ffffff" ? "#a7afbd" : theme.text + "bb"
    );

    root.style.setProperty("--header-bg", theme.bg + "ee");
    root.style.setProperty("--input-bg", theme.bg);

    Object.keys(themeInputs).forEach(key => {
        if (themeInputs[key]) {
            themeInputs[key].value = theme[key];
        }
    });

    if (save) {
        try {
            localStorage.setItem(
                "amlakan_personal_theme",
                JSON.stringify(theme)
            );
        } catch (error) {
            console.warn("ذخیره تنظیمات ممکن نشد.", error);
        }
    }

}


// بارگذاری رنگ ذخیره‌شده

let savedTheme = defaultTheme;

try {

    const storedTheme = JSON.parse(
        localStorage.getItem("amlakan_personal_theme") || "null"
    );

    if (
        storedTheme &&
        ["bg", "card", "accent", "text"].every(key =>
            typeof storedTheme[key] === "string" &&
            /^#[0-9a-fA-F]{6}$/.test(storedTheme[key])
        )
    ) {
        savedTheme = storedTheme;
    }

} catch (error) {
    console.log("تنظیمات قبلی پیدا نشد.");
}

applyTheme(savedTheme, false);


// باز و بسته کردن پنل

if (themeToggle && themePanel) {

    themeToggle.addEventListener("click", () => {

        const opened = themePanel.classList.toggle("open");

        themeToggle.setAttribute(
            "aria-expanded",
            String(opened)
        );

    });

}


// تغییر دستی رنگ

Object.keys(themeInputs).forEach(key => {

    if (!themeInputs[key]) return;

    themeInputs[key].addEventListener("input", () => {

        const current = {};

        Object.keys(themeInputs).forEach(k => {
            current[k] = themeInputs[k].value;
        });

        applyTheme(current);

    });

});


// قالب‌های آماده

document.querySelectorAll(".theme-preset").forEach(button => {

    button.addEventListener("click", () => {

        const preset = themePresets[button.dataset.theme];

        if (preset) {
            applyTheme(preset);
        }

    });

});


// بازگشت به رنگ پیش‌فرض

document.getElementById("themeReset")?.addEventListener(
    "click",
    () => {
        applyTheme(defaultTheme);
    }
);


// بستن پنل

document.getElementById("themeClose")?.addEventListener(
    "click",
    () => {

        themePanel?.classList.remove("open");

        themeToggle?.setAttribute("aria-expanded", "false");

    }
);


// بستن پنل با کلیک بیرون آن

document.addEventListener("click", event => {

    if (
        themePanel &&
        themeToggle &&
        !themePanel.contains(event.target) &&
        !themeToggle.contains(event.target)
    ) {

        themePanel.classList.remove("open");

        themeToggle.setAttribute("aria-expanded", "false");

    }

});

</script>
"""


# =====================================
# HOME PAGE
# =====================================

HOME_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>املاکان ایران | خرید، فروش و اجاره ملک</title>
""" + STYLE + """
</head>

<body>

""" + HEADER + """

<section class="hero">
    <div class="container">

        <h1>خانه رویایی خود را <span>پیدا کنید</span></h1>

        <p>خرید، فروش و اجاره ملک در سراسر ایران</p>

        <form class="search-box" method="GET" action="/">

            <input
                type="text"
                name="q"
                placeholder="نام ملک یا شهر موردنظر را وارد کنید..."
                value="{{ query }}"
            >

            <button class="btn" type="submit">
                جست وجوی ملک
            </button>

        </form>

    </div>
</section>

<main class="container" id="properties">

    <div class="section-title">
        <h2>جدیدترین <span class="gold">آگهی‌های املاک</span></h2>
        <a href="/add" class="gold">ثبت آگهی ←</a>
    </div>

    {% if properties %}

    <div class="grid">

        {% for p in properties %}

        <a class="card" href="{{ url_for('property_detail', property_id=p.id) }}">

            <img src="{{ p.image }}" alt="{{ p.title }}"
                 onerror="this.src='https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1000'">

            <div class="card-content">

                <h3>{{ p.title }}</h3>

                <p class="muted">{{ p.city }}</p>

                <div class="price">{{ p.price }}</div>

                <div class="card-footer">
                    <span>{{ p.area }} متر</span>
                    <span>{{ p.rooms }} اتاق</span>
                    <span>{{ p.kind }}</span>
                </div>

                <p class="gold">مشاهده جزئیات ملک ←</p>

            </div>

        </a>

        {% endfor %}

    </div>

    {% else %}

    <div class="empty">
        <h3>ملکی پیدا نشد!</h3>
        <p>عبارت دیگری را جست وجو کنید یا آگهی جدید ثبت کنید.</p>
        <a href="/add" class="btn">ثبت آگهی</a>
    </div>

    {% endif %}

</main>

<footer>
    <div class="logo" style="justify-content:center">
        املاکان <span class="gold">ایران</span>
    </div>
    <p>سامانه خرید، فروش و اجاره املاک در ایران</p>
    <p>تمام حقوق محفوظ است.</p>
</footer>

""" + SCRIPTS + """

</body>
</html>
"""


# =====================================
# ADD PROPERTY PAGE
# =====================================

ADD_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ثبت آگهی | املاکان ایران</title>
""" + STYLE + """
</head>

<body>

""" + HEADER + """

<div class="container">

    <form class="form-box" method="POST" action="/add">

        <h2>ثبت آگهی ملک جدید</h2>

        <p class="muted">
            اطلاعات ملک خود را وارد کنید تا آگهی در سایت نمایش داده شود.
        </p>

        <label>عنوان آگهی</label>
        <input name="title" required
               placeholder="مثلاً آپارتمان لوکس در تهران">

        <label>شهر</label>
        <input name="city" required placeholder="مثلاً تهران">

        <label>قیمت</label>
        <input name="price" required placeholder="مثلاً ۸ میلیارد تومان">

        <label>متراژ</label>
        <input name="area" type="number" min="1"
               required placeholder="مثلاً ۱۵۰">

        <label>تعداد اتاق</label>
        <input name="rooms" type="number" min="0"
               required placeholder="مثلاً ۳">

        <label>نوع معامله</label>
        <select name="kind" required>
            <option value="فروش">فروش</option>
            <option value="اجاره">اجاره</option>
            <option value="رهن">رهن</option>
        </select>

        <label>لینک عکس ملک</label>
        <input name="image" type="url" required
               placeholder="https://example.com/image.jpg">

        <label>توضیحات ملک</label>
        <textarea name="description"
                  placeholder="توضیحات کامل ملک را بنویسید..."></textarea>

        <button class="btn" type="submit">ثبت آگهی</button>

    </form>

</div>

""" + SCRIPTS + """

</body>
</html>
"""


# =====================================
# PROPERTY DETAILS
# =====================================

DETAIL_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ p.title }} | املاکان ایران</title>
""" + STYLE + """
</head>

<body>

""" + HEADER + """

<div class="container">

    <div class="detail">

        <img src="{{ p.image }}" alt="{{ p.title }}"
             onerror="this.src='https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=1000'">

        <div class="detail-content">

            <p class="gold">{{ p.kind }} ملک</p>

            <h1>{{ p.title }}</h1>

            <p class="muted">شهر: {{ p.city }}</p>

            <div class="price">{{ p.price }}</div>

            <div class="info-grid">

                <div class="info-item">
                    <small>متراژ</small>
                    <strong>{{ p.area }} متر مربع</strong>
                </div>

                <div class="info-item">
                    <small>تعداد اتاق</small>
                    <strong>{{ p.rooms }} اتاق</strong>
                </div>

                <div class="info-item">
                    <small>نوع معامله</small>
                    <strong>{{ p.kind }}</strong>
                </div>

                <div class="info-item">
                    <small>شناسه آگهی</small>
                    <strong>{{ p.id }}</strong>
                </div>

            </div>

            <h3 class="gold">توضیحات ملک</h3>

            <p class="description">
                {{ p.description or "برای این ملک توضیحاتی ثبت نشده است." }}
            </p>

            <a href="/" class="btn">بازگشت به صفحه اصلی</a>

        </div>

    </div>

</div>

""" + SCRIPTS + """

</body>
</html>
"""


# =====================================
# HOME ROUTE
# =====================================

@app.route("/")
def home():

    query = request.args.get("q", "").strip()

    db = get_db()

    if query:

        properties = db.execute("""
            SELECT * FROM properties
            WHERE title LIKE ? OR city LIKE ?
            ORDER BY id DESC
        """, (f"%{query}%", f"%{query}%")).fetchall()

    else:

        properties = db.execute("""
            SELECT * FROM properties
            ORDER BY id DESC
        """).fetchall()

    db.close()

    return render_template_string(
        HOME_HTML,
        properties=properties,
        query=query
    )


# =====================================
# ADD PROPERTY ROUTE
# =====================================

@app.route("/add", methods=["GET", "POST"])
def add_property():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        city = request.form.get("city", "").strip()
        price = request.form.get("price", "").strip()
        image = request.form.get("image", "").strip()
        description = request.form.get("description", "").strip()
        kind = request.form.get("kind", "").strip()

        try:
            area = int(request.form.get("area", "0"))
            rooms = int(request.form.get("rooms", "0"))

        except ValueError:
            return "متراژ و تعداد اتاق باید عدد باشند.", 400

        if not title or not city or not price or not image:
            return "لطفاً تمام اطلاعات ضروری را وارد کنید.", 400

        if area < 1 or rooms < 0:
            return "متراژ یا تعداد اتاق نامعتبر است.", 400

        if kind not in ["فروش", "اجاره", "رهن"]:
            return "نوع معامله نامعتبر است.", 400

        if not image.startswith(("https://", "http://")):
            return "لینک عکس معتبر نیست.", 400

        db = get_db()

        db.execute("""
            INSERT INTO properties
            (title, city, price, area, rooms, kind, image,
             description, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title, city, price, area, rooms, kind,
            image, description,
            datetime.now().strftime("%Y-%m-%d")
        ))

        db.commit()
        db.close()

        return redirect(url_for("home"))

    return render_template_string(ADD_HTML)


# =====================================
# PROPERTY DETAILS ROUTE
# =====================================

@app.route("/property/<int:property_id>")
def property_detail(property_id):

    db = get_db()

    property_item = db.execute("""
        SELECT * FROM properties
        WHERE id = ?
    """, (property_id,)).fetchone()

    db.close()

    if property_item is None:
        return "ملک موردنظر پیدا نشد!", 404

    return render_template_string(
        DETAIL_HTML,
        p=property_item
    )


# =====================================
# RUN APPLICATION
# =====================================

if __name__ == "__main__":
    app.run(debug=False)

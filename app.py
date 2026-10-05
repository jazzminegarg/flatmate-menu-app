import streamlit as st
import pandas as pd
import requests
from io import StringIO
from datetime import date, timedelta

# ============================================================
# CONFIGURATION
# ============================================================

SHEET_ID = "1XCwQ23-1RlkqKcHo6ECj6WDGMa3TUKxHc5AoB48CoBI"

# IMPORTANT:
# Replace this with your deployed Google Apps Script Web App URL.
API_URL = "PASTE_YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL_HERE"

USERS = ["Jasmine", "Aashi", "Meera"]
MEAL_TYPES = [
    ("☕", "Breakfast"),
    ("☀", "Lunch"),
    ("🌙", "Dinner"),
]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="our table ♡",
    page_icon="♡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
/* ---------- APP ---------- */

.stApp {
    background: #F8F5F6;
    color: #332E30;
}

.main .block-container {
    max-width: 1500px;
    padding: 1.4rem 1.5rem 2rem;
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* ---------- TYPOGRAPHY ---------- */

h1, h2, h3, p, div, span, label {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
                 "SF Pro Text", Inter, Arial, sans-serif;
}

.app-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -1.5px;
    color: #332E30;
    margin-top: 0.2rem;
}

.app-subtitle {
    text-align: center;
    color: #8A7F83;
    font-size: 0.92rem;
    margin-top: -3px;
}

/* ---------- TOP BAR ---------- */

.topbar {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    margin: 15px 0 14px;
    flex-wrap: wrap;
}

.user-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #FFFFFF;
    border: 1px solid #E8DDE0;
    border-radius: 999px;
    padding: 7px 11px;
    color: #6D6266;
    font-size: 0.78rem;
}

.user-pill.active {
    background: #F4E2E6;
    border-color: #E4B8C0;
    color: #A85F6C;
    font-weight: 700;
}

.progress {
    text-align: center;
    color: #8A7F83;
    font-size: 0.8rem;
    margin-bottom: 14px;
}

/* ---------- CALENDAR ---------- */

.calendar {
    width: 100%;
    overflow-x: auto;
    padding-bottom: 5px;
}

.calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, minmax(135px, 1fr));
    min-width: 980px;
    border: 1px solid #E5DADD;
    border-radius: 20px;
    overflow: hidden;
    background: #FFFFFF;
    box-shadow: 0 8px 28px rgba(70, 45, 52, 0.07);
}

.day-column {
    min-width: 0;
    border-right: 1px solid #EEE6E8;
}

.day-column:last-child {
    border-right: none;
}

.day-header {
    min-height: 67px;
    padding: 11px 8px 9px;
    text-align: center;
    background: #FFFBFC;
    border-bottom: 1px solid #EEE6E8;
}

.day-header.today {
    background: #F8E7EB;
}

.day-name {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1.1px;
    color: #9A8C91;
    font-weight: 700;
}

.day-number {
    font-size: 1.42rem;
    line-height: 1.25;
    font-weight: 700;
    color: #3B3437;
}

.today-pill {
    display: inline-block;
    font-size: 0.55rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #A85F6C;
    background: #FFFFFF;
    border-radius: 999px;
    padding: 2px 6px;
    margin-top: 2px;
}

/* ---------- MEAL SLOT ---------- */

.slot {
    min-height: 125px;
    padding: 9px 8px 10px;
    border-bottom: 1px solid #EEE6E8;
}

.slot:last-child {
    border-bottom: none;
}

.slot-label {
    color: #9A8C91;
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.9px;
    font-weight: 700;
    margin-bottom: 6px;
}

.meal-card {
    min-height: 72px;
    background: #FCFAFB;
    border: 1px solid #EAE1E4;
    border-radius: 12px;
    padding: 9px 8px;
}

.meal-card.confirmed {
    background: #F5F9F3;
    border-color: #D8E4D4;
}

.meal-card.waiting {
    background: #FFF9FA;
    border-color: #F0D9DE;
}

.meal-name {
    font-size: 0.77rem;
    line-height: 1.2;
    font-weight: 700;
    color: #40383B;
    word-break: break-word;
}

.vote-line {
    margin-top: 7px;
    color: #9A8C91;
    font-size: 0.61rem;
    line-height: 1.2;
}

.vote-line.confirmed {
    color: #708568;
    font-weight: 700;
}

.avatar-row {
    margin-top: 6px;
    color: #B17A84;
    font-size: 0.62rem;
    letter-spacing: 1px;
}

.empty-card {
    min-height: 72px;
    border: 1px dashed #DCCED2;
    border-radius: 12px;
    background: #FFFDFD;
    padding: 9px 8px;
}

.empty-plus {
    font-size: 1.15rem;
    color: #D18D99;
    line-height: 1;
}

.empty-title {
    color: #7E7176;
    font-size: 0.72rem;
    font-weight: 600;
    margin-top: 4px;
}

.empty-subtitle {
    color: #B0A4A8;
    font-size: 0.59rem;
    margin-top: 3px;
}

/* ---------- STREAMLIT BUTTONS ---------- */

.stButton > button {
    border-radius: 11px !important;
    border: 1px solid #E8DDE0 !important;
    background: #FFFFFF !important;
    color: #51484B !important;
    font-size: 0.68rem !important;
    min-height: 34px !important;
    padding: 3px 6px !important;
    box-shadow: none !important;
}

.stButton > button:hover {
    border-color: #D99AA5 !important;
    color: #A85F6C !important;
    background: #FFF8FA !important;
}

/* Slot buttons are deliberately compact */
.slot-button {
    margin-top: 5px;
}

/* ---------- BOTTOM / PICKER ---------- */

.picker {
    max-width: 650px;
    margin: 18px auto 0;
    padding: 18px;
    background: #FFFFFF;
    border: 1px solid #E8DDE0;
    border-radius: 18px;
    box-shadow: 0 8px 28px rgba(70, 45, 52, 0.08);
}

.picker-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #40383B;
}

.picker-subtitle {
    color: #9A8C91;
    font-size: 0.75rem;
    margin-top: 3px;
    margin-bottom: 12px;
}

/* ---------- RESPONSIVE ---------- */

@media (max-width: 900px) {
    .main .block-container {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }

    .app-title {
        font-size: 2rem;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DATA
# ============================================================

@st.cache_data(ttl=20)
def load_sheet():
    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/export?format=csv"
    )

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=15,
    )
    response.raise_for_status()

    text = response.text

    if "<html" in text[:500].lower():
        raise RuntimeError(
            "Google returned an HTML page instead of CSV. "
            "Make sure the Google Sheet is shared as 'Anyone with the link → Viewer'."
        )

    df = pd.read_csv(StringIO(text))
    df.columns = df.columns.astype(str).str.strip()

    required = {"Meal_ID", "Meal_Name"}
    missing = required - set(df.columns)

    if missing:
        raise RuntimeError(
            f"Missing required columns: {', '.join(sorted(missing))}. "
            f"Your sheet must contain Meal_ID and Meal_Name."
        )

    for user in USERS:
        if user not in df.columns:
            df[user] = ""

        df[user] = (
            df[user]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    return df


try:
    df = load_sheet()
except Exception as exc:
    st.error("Couldn't load the kitchen sheet.")
    st.code(str(exc))
    st.stop()


# ============================================================
# HELPERS
# ============================================================

def week_start(today=None):
    today = today or date.today()
    return today - timedelta(days=today.weekday())


def display_date_for_day(day_name):
    start = week_start()
    index = DAYS.index(day_name)
    return start + timedelta(days=index)


def get_votes_for_slot(day, meal_type):
    """
    Reads the existing sheet format:
    Aashi / Meera / Jasmine cells contain values such as:
    Monday_Breakfast, Tuesday_Lunch, Wednesday_Dinner
    """
    target = f"{day}_{meal_type}"

    result = {}

    for user in USERS:
        rows = df[df[user].str.contains(target, regex=False, na=False)]

        if not rows.empty:
            result[user] = str(rows.iloc[0]["Meal_ID"])

    return result


def meal_name(meal_id):
    rows = df[df["Meal_ID"].astype(str) == str(meal_id)]

    if rows.empty:
        return "Unknown meal"

    return str(rows.iloc[0]["Meal_Name"])


def users_for_meal(votes, selected_meal_id):
    return [
        user
        for user, voted_meal_id in votes.items()
        if str(voted_meal_id) == str(selected_meal_id)
    ]


def slot_state(day, meal_type):
    votes = get_votes_for_slot(day, meal_type)

    if not votes:
        return None, [], votes

    # Count meals chosen by users.
    counts = {}

    for voted_meal_id in votes.values():
        voted_meal_id = str(voted_meal_id)
        counts[voted_meal_id] = counts.get(voted_meal_id, 0) + 1

    # Show the meal with the most votes.
    winning_meal_id = max(counts, key=counts.get)
    winning_count = counts[winning_meal_id]

    voters = users_for_meal(votes, winning_meal_id)

    return winning_meal_id, voters, votes


def save_vote(meal_id, user, vote):
    if not API_URL or API_URL.startswith("PASTE_"):
        st.error(
            "Voting is not connected yet. Add your Google Apps Script Web App URL "
            "to API_URL at the top of app.py."
        )
        return False

    try:
        response = requests.get(
            API_URL,
            params={
                "mealId": str(meal_id),
                "roomie": user,
                "vote": vote,
            },
            timeout=15,
        )

        response.raise_for_status()

        try:
            payload = response.json()
            if payload.get("ok") is False:
                st.error(payload.get("error", "Google Apps Script rejected the vote."))
                return False
        except ValueError:
            # Apps Script may return plain text depending on deployment.
            pass

        load_sheet.clear()
        return True

    except Exception as exc:
        st.error(f"Couldn't save your choice: {exc}")
        return False


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">our table ♡</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-subtitle">what are we eating?</div>',
    unsafe_allow_html=True,
)

user = st.selectbox(
    "Profile",
    USERS,
    index=0,
    label_visibility="collapsed",
)

planned = 0

for day in DAYS:
    for _, meal_type in MEAL_TYPES:
        winning_meal, voters, votes = slot_state(day, meal_type)

        if winning_meal is not None:
            planned += 1

st.markdown(
    '<div class="topbar">'
    + "".join(
        f'<div class="user-pill {"active" if user == u else ""}">♡ {u}</div>'
        for u in USERS
    )
    + "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="progress">{planned} / 21 meals planned this week</div>',
    unsafe_allow_html=True,
)


# ============================================================
# CALENDAR
# ============================================================

today = date.today()

calendar_html = '<div class="calendar"><div class="calendar-grid">'

for day in DAYS:
    d = display_date_for_day(day)
    is_today = d == today

    calendar_html += f"""
        <div class="day-column">
            <div class="day-header {"today" if is_today else ""}">
                <div class="day-name">{day[:3]}</div>
                <div class="day-number">{d.day}</div>
                {"<div class='today-pill'>today</div>" if is_today else ""}
            </div>
    """

    for icon, meal_type in MEAL_TYPES:
        winning_meal, voters, votes = slot_state(day, meal_type)

        calendar_html += f"""
            <div class="slot">
                <div class="slot-label">{icon} {meal_type}</div>
        """

        if winning_meal is not None:
            name = meal_name(winning_meal)
            count = len(voters)
            confirmed = count == len(USERS)

            initials = "  ".join(u[0] for u in voters)

            calendar_html += f"""
                <div class="meal-card {"confirmed" if confirmed else "waiting"}">
                    <div class="meal-name">{name}</div>
                    <div class="avatar-row">{initials if initials else "·"}</div>
                    <div class="vote-line {"confirmed" if confirmed else ""}">
                        {"✓ everyone agrees ♡" if confirmed else f"{count}/3 · voting"}
                    </div>
                </div>
            """

        else:
            calendar_html += """
                <div class="empty-card">
                    <div class="empty-plus">＋</div>
                    <div class="empty-title">choose</div>
                    <div class="empty-subtitle">your turn</div>
                </div>
            """

        calendar_html += "</div>"

    calendar_html += "</div>"

calendar_html += "</div></div>"

st.markdown(calendar_html, unsafe_allow_html=True)


# ============================================================
# INTERACTION ROW
# ============================================================

st.markdown(
    '<div style="height:10px"></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div style="text-align:center;color:#9A8C91;font-size:0.75rem;">'
    'tap a meal slot below to change your choice'
    '</div>',
    unsafe_allow_html=True,
)

# Use three compact controls per day so the calendar itself remains
# the visual centerpiece.
for day in DAYS:
    cols = st.columns(3)

    for col, (_, meal_type) in zip(cols, MEAL_TYPES):
        with col:
            if st.button(
                f"{day[:3]} · {meal_type}",
                key=f"pick_{day}_{meal_type}",
                use_container_width=True,
            ):
                st.session_state["active_slot"] = f"{day}_{meal_type}"


# ============================================================
# MEAL PICKER
# ============================================================

if "active_slot" in st.session_state:
    active_slot = st.session_state["active_slot"]
    active_day, active_meal_type = active_slot.split("_", 1)

    st.markdown(
        f"""
        <div class="picker">
            <div class="picker-title">
                {active_day} · {active_meal_type}
            </div>
            <div class="picker-subtitle">
                choose your meal, {user} ♡
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    search = st.text_input(
        "Search meals",
        placeholder="🔍  search meals...",
        label_visibility="collapsed",
        key="meal_search",
    )

    meals = df.copy()

    if search:
        meals = meals[
            meals["Meal_Name"]
            .astype(str)
            .str.contains(search, case=False, na=False)
        ]

    meal_cols = st.columns(2)

    for i, (_, row) in enumerate(meals.iterrows()):
        with meal_cols[i % 2]:
            if st.button(
                f"🍛 {row['Meal_Name']}",
                key=f"choose_{active_slot}_{row['Meal_ID']}",
                use_container_width=True,
            ):
                success = save_vote(
                    row["Meal_ID"],
                    user,
                    active_slot,
                )

                if success:
                    st.session_state.pop("active_slot", None)
                    st.session_state.pop("meal_search", None)
                    st.success("saved ♡")
                    st.rerun()

    if st.button(
        "close",
        key="close_picker",
        use_container_width=True,
    ):
        st.session_state.pop("active_slot", None)
        st.session_state.pop("meal_search", None)
        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#B1A5A9;
        font-size:0.68rem;
        padding:18px 0 0;
    ">
        made for the flat ♡
    </div>
    """,
    unsafe_allow_html=True,
)

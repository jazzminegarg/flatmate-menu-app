import streamlit as st
import pandas as pd
import requests
from io import StringIO
from datetime import date, timedelta
from textwrap import dedent

# ============================================================
# CONFIGURATION
# ============================================================

SHEET_ID = "1XCwQ23-1RlkqKcHo6ECj6WDGMa3TUKxHc5AoB48CoBI"

API_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbxFvVUQcN1tnr9HCeRjrJz2nBSDH_TTdmWZCUxedU05TMgnNUwxWqFKTDip5hruuHMp"
    "/exec"
)

USERS = ["Jasmine", "Aashi", "Meera"]

MEAL_TYPES = [
    ("☕", "Breakfast"),
    ("☀", "Lunch"),
    ("🌙", "Dinner"),
]

DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="our table ♡",
    page_icon="♡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
<style>
.stApp {
    background: #F8F5F6;
    color: #332E30;
}

.main .block-container {
    max-width: 1500px;
    padding: 1.1rem 1.5rem 2rem;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

/* ---------- HEADER ---------- */

.app-title {
    text-align: center;
    font-size: 2.35rem;
    line-height: 1.1;
    font-weight: 750;
    letter-spacing: -1.8px;
    color: #332E30;
    margin-top: 0.1rem;
}

.app-subtitle {
    text-align: center;
    color: #9A8C91;
    font-size: 0.88rem;
    margin-top: 4px;
}

.profile-select {
    max-width: 260px;
    margin: 10px auto 5px;
}

/* ---------- USER PILLS ---------- */

.user-row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 7px;
    margin: 13px 0 6px;
}

.user-pill {
    background: #FFFFFF;
    border: 1px solid #E6DCE0;
    border-radius: 999px;
    padding: 6px 11px;
    color: #786C71;
    font-size: 0.73rem;
}

.user-pill.active {
    background: #F5E1E6;
    border-color: #E1AEB8;
    color: #A65E6C;
    font-weight: 700;
}

.progress {
    text-align: center;
    color: #96898E;
    font-size: 0.74rem;
    margin: 7px 0 15px;
}

/* ---------- CALENDAR ---------- */

.calendar-wrap {
    width: 100%;
    overflow-x: auto;
    padding-bottom: 4px;
}

.calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, minmax(125px, 1fr));
    min-width: 980px;
    background: #FFFFFF;
    border: 1px solid #E4DADD;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px 26px rgba(70, 45, 52, 0.07);
}

.day-column {
    min-width: 0;
    border-right: 1px solid #EEE7E9;
}

.day-column:last-child {
    border-right: none;
}

.day-header {
    height: 62px;
    box-sizing: border-box;
    padding: 9px 5px 7px;
    text-align: center;
    background: #FFFCFD;
    border-bottom: 1px solid #EEE7E9;
}

.day-header.today {
    background: #F9E8EC;
}

.day-name {
    color: #9B8D92;
    font-size: 0.63rem;
    font-weight: 750;
    letter-spacing: 1.1px;
    text-transform: uppercase;
}

.day-number {
    color: #383133;
    font-size: 1.3rem;
    font-weight: 750;
    line-height: 1.25;
}

.today-pill {
    display: inline-block;
    background: #FFFFFF;
    color: #AE6573;
    border-radius: 999px;
    padding: 1px 6px;
    font-size: 0.48rem;
    font-weight: 750;
    letter-spacing: 0.7px;
    text-transform: uppercase;
}

/* ---------- MEAL SLOTS ---------- */

.slot {
    height: 112px;
    box-sizing: border-box;
    padding: 8px 7px;
    border-bottom: 1px solid #EEE7E9;
}

.slot:last-child {
    border-bottom: none;
}

.slot-label {
    color: #A09398;
    font-size: 0.57rem;
    font-weight: 750;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 5px;
}

.meal-card {
    height: 78px;
    box-sizing: border-box;
    background: #FCFAFB;
    border: 1px solid #E9E0E3;
    border-radius: 11px;
    padding: 8px;
}

.meal-card.confirmed {
    background: #F5F9F3;
    border-color: #D9E5D5;
}

.meal-card.waiting {
    background: #FFF9FA;
    border-color: #F0DADF;
}

.meal-name {
    color: #423A3D;
    font-size: 0.69rem;
    font-weight: 750;
    line-height: 1.15;
    min-height: 28px;
    overflow: hidden;
    word-break: break-word;
}

.avatar-row {
    color: #B26D7A;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 4px;
    height: 12px;
}

.vote-line {
    color: #A0969A;
    font-size: 0.54rem;
    line-height: 1.1;
    margin-top: 3px;
}

.vote-line.confirmed {
    color: #71866A;
    font-weight: 750;
}

.empty-card {
    height: 78px;
    box-sizing: border-box;
    background: #FFFDFD;
    border: 1px dashed #DCCED2;
    border-radius: 11px;
    padding: 8px;
}

.empty-plus {
    color: #D28E9A;
    font-size: 1rem;
    line-height: 1;
}

.empty-title {
    color: #7D7075;
    font-size: 0.68rem;
    font-weight: 650;
    margin-top: 5px;
}

.empty-subtitle {
    color: #B0A4A8;
    font-size: 0.53rem;
    margin-top: 3px;
}

/* ---------- PROFILE SELECT ---------- */

div[data-testid="stSelectbox"] {
    max-width: 260px;
    margin: 8px auto 0;
}

div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #E3D9DD !important;
    border-radius: 11px !important;
    color: #51484B !important;
    min-height: 38px !important;
}

/* ---------- ACTION BUTTONS ---------- */

.stButton > button {
    background: #FFFFFF !important;
    color: #65595E !important;
    border: 1px solid #E5DBDE !important;
    border-radius: 11px !important;
    min-height: 36px !important;
    box-shadow: none !important;
    font-size: 0.7rem !important;
}

.stButton > button:hover {
    background: #FFF6F8 !important;
    color: #A65E6C !important;
    border-color: #DDAAB4 !important;
}

/* ---------- PICKER ---------- */

.picker {
    max-width: 650px;
    margin: 18px auto 0;
    padding: 18px;
    background: #FFFFFF;
    border: 1px solid #E5DBDE;
    border-radius: 18px;
    box-shadow: 0 8px 26px rgba(70, 45, 52, 0.08);
}

.picker-title {
    color: #40383B;
    font-size: 1.05rem;
    font-weight: 750;
}

.picker-subtitle {
    color: #9A8C91;
    font-size: 0.74rem;
    margin-top: 3px;
    margin-bottom: 12px;
}

/* ---------- FOOTER ---------- */

.footer-note {
    text-align: center;
    color: #B2A6AA;
    font-size: 0.65rem;
    padding-top: 14px;
}

/* ---------- MOBILE ---------- */

@media (max-width: 900px) {
    .main .block-container {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }

    .app-title {
        font-size: 2rem;
    }

    .calendar-grid {
        min-width: 910px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# LOAD GOOGLE SHEET
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
            "Set the Google Sheet to 'Anyone with the link → Viewer'."
        )

    data = pd.read_csv(StringIO(text))
    data.columns = data.columns.astype(str).str.strip()

    required = {"Meal_ID", "Meal_Name"}
    missing = required - set(data.columns)

    if missing:
        raise RuntimeError(
            "Missing required columns: "
            + ", ".join(sorted(missing))
            + ". Your sheet needs Meal_ID and Meal_Name."
        )

    for person in USERS:
        if person not in data.columns:
            data[person] = ""

        data[person] = (
            data[person]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    return data


try:
    df = load_sheet()
except Exception as exc:
    st.error("Couldn't load the kitchen sheet.")
    st.code(str(exc))
    st.stop()


# ============================================================
# HELPERS
# ============================================================

def get_week_start():
    today = date.today()
    return today - timedelta(days=today.weekday())


def get_date_for_day(day_name):
    return get_week_start() + timedelta(days=DAYS.index(day_name))


def get_votes_for_slot(day, meal_type):
    """
    Existing Google Sheet format:
    each user's cell contains values such as
    Monday_Lunch or Tuesday_Dinner.
    """

    target = f"{day}_{meal_type}"
    votes = {}

    for person in USERS:
        matches = df[
            df[person].str.contains(
                target,
                regex=False,
                na=False,
            )
        ]

        if not matches.empty:
            votes[person] = str(matches.iloc[0]["Meal_ID"])

    return votes


def get_meal_name(meal_id):
    matches = df[
        df["Meal_ID"].astype(str) == str(meal_id)
    ]

    if matches.empty:
        return "Unknown meal"

    return str(matches.iloc[0]["Meal_Name"])


def get_slot_info(day, meal_type):
    votes = get_votes_for_slot(day, meal_type)

    if not votes:
        return None, [], votes

    counts = {}

    for meal_id in votes.values():
        meal_id = str(meal_id)
        counts[meal_id] = counts.get(meal_id, 0) + 1

    winning_meal = max(
        counts,
        key=counts.get,
    )

    voters = [
        person
        for person, voted_meal in votes.items()
        if str(voted_meal) == str(winning_meal)
    ]

    return winning_meal, voters, votes


def save_vote(meal_id, person, slot):
    if not API_URL:
        st.error("API_URL is empty.")
        return False

    try:
        response = requests.get(
            API_URL,
            params={
                "mealId": str(meal_id),
                "roomie": person,
                "vote": slot,
            },
            timeout=15,
        )

        response.raise_for_status()

        try:
            result = response.json()

            if result.get("ok") is False:
                st.error(
                    result.get(
                        "error",
                        "Google Apps Script rejected the vote.",
                    )
                )
                return False

        except ValueError:
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

# User pills
user_pills = ""

for person in USERS:
    active_class = " active" if person == user else ""

    user_pills += (
        f'<div class="user-pill{active_class}">'
        f"♡ {person}"
        f"</div>"
    )

st.markdown(
    f'<div class="user-row">{user_pills}</div>',
    unsafe_allow_html=True,
)


# ============================================================
# WEEK PROGRESS
# ============================================================

planned = 0

for day in DAYS:
    for _, meal_type in MEAL_TYPES:
        winning_meal, _, _ = get_slot_info(
            day,
            meal_type,
        )

        if winning_meal is not None:
            planned += 1

st.markdown(
    f'<div class="progress">{planned} / 21 meals planned this week</div>',
    unsafe_allow_html=True,
)


# ============================================================
# CALENDAR
# ============================================================

today = date.today()

calendar_html = """
<div class="calendar-wrap">
<div class="calendar-grid">
"""

for day in DAYS:

    current_date = get_date_for_day(day)
    is_today = current_date == today

    today_html = (
        '<div class="today-pill">today</div>'
        if is_today
        else ""
    )

    calendar_html += f"""
<div class="day-column">
    <div class="day-header {'today' if is_today else ''}">
        <div class="day-name">{day[:3]}</div>
        <div class="day-number">{current_date.day}</div>
        {today_html}
    </div>
"""

    for icon, meal_type in MEAL_TYPES:

        winning_meal, voters, votes = get_slot_info(
            day,
            meal_type,
        )

        calendar_html += f"""
    <div class="slot">
        <div class="slot-label">{icon} {meal_type}</div>
"""

        if winning_meal is not None:

            name = get_meal_name(winning_meal)
            count = len(voters)
            confirmed = count == len(USERS)

            initials = "  ".join(
                person[0]
                for person in voters
            )

            card_class = (
                "confirmed"
                if confirmed
                else "waiting"
            )

            if confirmed:
                vote_text = "✓ everyone agrees ♡"
            else:
                vote_text = f"{count}/3 · voting"

            vote_class = (
                "confirmed"
                if confirmed
                else ""
            )

            calendar_html += f"""
        <div class="meal-card {card_class}">
            <div class="meal-name">{name}</div>
            <div class="avatar-row">{initials}</div>
            <div class="vote-line {vote_class}">
                {vote_text}
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

        calendar_html += """
    </div>
"""

    calendar_html += """
</div>
"""

calendar_html += """
</div>
</div>
"""

st.markdown(
    dedent(calendar_html),
    unsafe_allow_html=True,
)


# ============================================================
# SLOT PICKER
# ============================================================

st.markdown(
    """
<div style="
    text-align:center;
    color:#9A8C91;
    font-size:0.7rem;
    margin:14px 0 7px;
">
    choose a meal below to update your week ♡
</div>
""",
    unsafe_allow_html=True,
)

# Compact controls.
# These sit below the calendar so the calendar itself stays clean.
for day in DAYS:

    cols = st.columns(3)

    for col, (_, meal_type) in zip(cols, MEAL_TYPES):

        with col:

            if st.button(
                f"{day[:3]} · {meal_type}",
                key=f"slot_{day}_{meal_type}",
                use_container_width=True,
            ):
                st.session_state["active_slot"] = (
                    f"{day}_{meal_type}"
                )


# ============================================================
# MEAL PICKER
# ============================================================

if "active_slot" in st.session_state:

    active_slot = st.session_state["active_slot"]

    active_day, active_meal_type = active_slot.split(
        "_",
        1,
    )

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
            .str.contains(
                search,
                case=False,
                na=False,
            )
        ]

    meal_columns = st.columns(2)

    for index, (_, row) in enumerate(
        meals.iterrows()
    ):

        with meal_columns[index % 2]:

            if st.button(
                f"🍛 {row['Meal_Name']}",
                key=(
                    f"choose_{active_slot}_"
                    f"{row['Meal_ID']}"
                ),
                use_container_width=True,
            ):

                saved = save_vote(
                    row["Meal_ID"],
                    user,
                    active_slot,
                )

                if saved:

                    st.session_state.pop(
                        "active_slot",
                        None,
                    )

                    st.session_state.pop(
                        "meal_search",
                        None,
                    )

                    st.success("saved ♡")
                    st.rerun()

    if st.button(
        "close",
        key="close_picker",
        use_container_width=True,
    ):

        st.session_state.pop(
            "active_slot",
            None,
        )

        st.session_state.pop(
            "meal_search",
            None,
        )

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer-note">
    made for the flat ♡
</div>
""",
    unsafe_allow_html=True,
)

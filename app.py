import streamlit as st
import pandas as pd
import requests
from io import StringIO
from datetime import date, timedelta

# ============================================================
# CONFIG
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
# PAGE
# ============================================================

st.set_page_config(
    page_title="our table ♡",
    page_icon="♡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* ---------- PAGE ---------- */

.stApp {
    background: #F8F5F6;
    color: #332E30;
}

.main .block-container {
    max-width: 1500px;
    padding: 1rem 1.5rem 2rem;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

/* ---------- HEADER ---------- */

.app-title {
    text-align: center;
    color: #332E30;
    font-size: 2.35rem;
    font-weight: 800;
    letter-spacing: -1.8px;
    line-height: 1.05;
    margin-top: 0.1rem;
}

.app-subtitle {
    text-align: center;
    color: #9A8C91;
    font-size: 0.88rem;
    margin-top: 5px;
    margin-bottom: 8px;
}

/* ---------- PROFILE ---------- */

div[data-testid="stSelectbox"] {
    max-width: 270px;
    margin: 8px auto 5px;
}

div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #E2D7DB !important;
    border-radius: 12px !important;
    color: #51484B !important;
}

.user-row {
    display: flex;
    justify-content: center;
    gap: 7px;
    margin: 10px 0 6px;
}

.user-pill {
    background: #FFFFFF;
    border: 1px solid #E5DBDE;
    border-radius: 999px;
    padding: 6px 11px;
    color: #796D72;
    font-size: 0.72rem;
}

.user-pill.active {
    background: #F5E1E6;
    border-color: #E0AAB5;
    color: #A65D6C;
    font-weight: 750;
}

.progress {
    text-align: center;
    color: #94878C;
    font-size: 0.74rem;
    margin: 7px 0 14px;
}

/* ---------- CALENDAR ---------- */

.calendar-shell {
    background: #FFFFFF;
    border: 1px solid #E3D9DC;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 8px 28px rgba(70, 45, 52, 0.07);
}

/* Streamlit's 7 columns */

div[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
}

/* Day header */

.day-header {
    height: 62px;
    box-sizing: border-box;
    text-align: center;
    padding: 9px 4px 6px;
    background: #FFFCFD;
    border-bottom: 1px solid #EEE6E8;
}

.day-header.today {
    background: #F9E7EB;
}

.day-name {
    color: #9A8C91;
    font-size: 0.61rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.day-number {
    color: #393235;
    font-size: 1.25rem;
    font-weight: 800;
    line-height: 1.25;
}

.today-pill {
    display: inline-block;
    color: #A85D6C;
    background: #FFFFFF;
    border-radius: 999px;
    padding: 1px 6px;
    font-size: 0.45rem;
    font-weight: 800;
    letter-spacing: .7px;
    text-transform: uppercase;
}

/* ---------- SLOT LABEL ---------- */

.slot-label {
    color: #9A8C91;
    font-size: 0.57rem;
    font-weight: 800;
    letter-spacing: .75px;
    text-transform: uppercase;
    margin: 8px 7px 4px;
}

/* ---------- ACTUAL CLICKABLE MEAL CARD ---------- */

/*
The important part:
these are REAL Streamlit buttons, not HTML.
Therefore clicking them actually triggers Python.
*/

div[data-testid="stHorizontalBlock"] .stButton {
    margin: 0 6px 5px;
}

div[data-testid="stHorizontalBlock"] .stButton > button {
    width: 100%;
    height: 77px;
    min-height: 77px;

    background: #FCFAFB !important;
    color: #423A3D !important;

    border: 1px solid #E9E0E3 !important;
    border-radius: 12px !important;

    padding: 7px 7px !important;

    font-size: 0.68rem !important;
    font-weight: 700 !important;

    white-space: pre-wrap !important;
    line-height: 1.25 !important;

    box-shadow: none !important;
    transition: 0.12s ease !important;
}

div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: #FFF7F9 !important;
    border-color: #D998A4 !important;
    color: #A55C6A !important;
    transform: translateY(-1px);
}

/* Empty slot */

.empty-slot > div[data-testid="stButton"] > button {
    background: #FFFDFD !important;
    border: 1px dashed #DCCED2 !important;
    color: #7D7075 !important;
}

/* ---------- SEPARATOR BETWEEN MEAL TYPES ---------- */

.slot-divider {
    height: 1px;
    background: #EEE7E9;
    margin: 3px 0;
}

/* ---------- PICKER ---------- */

.picker {
    max-width: 680px;
    margin: 18px auto 0;
    background: #FFFFFF;
    border: 1px solid #E4DADD;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 8px 28px rgba(70, 45, 52, 0.08);
}

.picker-title {
    color: #40383B;
    font-size: 1.05rem;
    font-weight: 800;
}

.picker-subtitle {
    color: #9A8C91;
    font-size: 0.74rem;
    margin-top: 3px;
    margin-bottom: 12px;
}

/* ---------- PICKER BUTTONS ---------- */

.picker-button > button {
    height: 45px !important;
    min-height: 45px !important;
    border-radius: 12px !important;
}

/* ---------- FOOTER ---------- */

.footer-note {
    text-align: center;
    color: #B2A6AA;
    font-size: 0.65rem;
    padding-top: 16px;
}

/* ---------- MOBILE ---------- */

@media (max-width: 900px) {
    .main .block-container {
        padding-left: 0.35rem;
        padding-right: 0.35rem;
    }

    .calendar-shell {
        overflow-x: auto;
    }

    .calendar-inner {
        min-width: 920px;
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
# LOAD SHEET
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
            "Google returned HTML instead of CSV. "
            "Set the Google Sheet to "
            "'Anyone with the link → Viewer'."
        )

    data = pd.read_csv(StringIO(text))

    data.columns = (
        data.columns
        .astype(str)
        .str.strip()
    )

    required = {"Meal_ID", "Meal_Name"}

    missing = required - set(data.columns)

    if missing:
        raise RuntimeError(
            "Missing required columns: "
            + ", ".join(sorted(missing))
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
    return (
        get_week_start()
        + timedelta(days=DAYS.index(day_name))
    )


def get_votes_for_slot(day, meal_type):

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

            votes[person] = str(
                matches.iloc[0]["Meal_ID"]
            )

    return votes


def get_meal_name(meal_id):

    matches = df[
        df["Meal_ID"].astype(str)
        == str(meal_id)
    ]

    if matches.empty:
        return "Unknown meal"

    return str(
        matches.iloc[0]["Meal_Name"]
    )


def get_slot_info(day, meal_type):

    votes = get_votes_for_slot(
        day,
        meal_type,
    )

    if not votes:
        return None, [], votes

    counts = {}

    for meal_id in votes.values():

        meal_id = str(meal_id)

        counts[meal_id] = (
            counts.get(meal_id, 0) + 1
        )

    winning_meal = max(
        counts,
        key=counts.get,
    )

    voters = [
        person
        for person, voted_meal in votes.items()
        if str(voted_meal)
        == str(winning_meal)
    ]

    return winning_meal, voters, votes


def save_vote(meal_id, person, slot):

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

        st.error(
            f"Couldn't save your choice: {exc}"
        )

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

pills = ""

for person in USERS:

    active = (
        " active"
        if person == user
        else ""
    )

    pills += (
        f'<div class="user-pill{active}">'
        f"♡ {person}"
        f"</div>"
    )

st.markdown(
    f'<div class="user-row">{pills}</div>',
    unsafe_allow_html=True,
)


# ============================================================
# PROGRESS
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
    f'<div class="progress">'
    f'{planned} / 21 meals planned this week'
    f'</div>',
    unsafe_allow_html=True,
)


# ============================================================
# CALENDAR
# ============================================================

today = date.today()

st.markdown(
    '<div class="calendar-shell">',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="calendar-inner">',
    unsafe_allow_html=True,
)


# -------------------------
# DAY HEADERS
# -------------------------

header_cols = st.columns(7, gap="small")

for col, day in zip(header_cols, DAYS):

    with col:

        current_date = get_date_for_day(day)

        is_today = (
            current_date == today
        )

        today_html = (
            '<div class="today-pill">today</div>'
            if is_today
            else ""
        )

        st.markdown(
            f"""
            <div class="day-header {'today' if is_today else ''}">
                <div class="day-name">{day[:3]}</div>
                <div class="day-number">{current_date.day}</div>
                {today_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


# -------------------------
# THREE MEAL ROWS
# -------------------------

for meal_icon, meal_type in MEAL_TYPES:

    # Meal labels
    label_cols = st.columns(
        7,
        gap="small",
    )

    for col in label_cols:

        with col:

            st.markdown(
                f'<div class="slot-label">'
                f'{meal_icon} {meal_type}'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Actual clickable cards
    meal_cols = st.columns(
        7,
        gap="small",
    )

    for col, day in zip(
        meal_cols,
        DAYS,
    ):

        with col:

            winning_meal, voters, votes = (
                get_slot_info(
                    day,
                    meal_type,
                )
            )

            slot = f"{day}_{meal_type}"

            if winning_meal is None:

                label = (
                    "＋\n"
                    "choose\n"
                    "your turn"
                )

            else:

                name = get_meal_name(
                    winning_meal
                )

                count = len(voters)

                initials = " ".join(
                    person[0]
                    for person in voters
                )

                if count == len(USERS):

                    status = (
                        f"{initials}\n"
                        "✓ everyone agrees ♡"
                    )

                else:

                    status = (
                        f"{initials}\n"
                        f"{count}/3 · voting"
                    )

                label = (
                    f"🍛 {name}\n"
                    f"{status}"
                )

            clicked = st.button(
                label,
                key=f"calendar_{slot}",
                use_container_width=True,
            )

            if clicked:

                st.session_state[
                    "active_slot"
                ] = slot

                st.rerun()

    # Divider between rows
    if meal_type != "Dinner":

        st.markdown(
            '<div class="slot-divider"></div>',
            unsafe_allow_html=True,
        )


st.markdown(
    '</div></div>',
    unsafe_allow_html=True,
)


# ============================================================
# MEAL PICKER
# ============================================================

if "active_slot" in st.session_state:

    active_slot = (
        st.session_state["active_slot"]
    )

    active_day, active_meal_type = (
        active_slot.split("_", 1)
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

    picker_cols = st.columns(2)

    for index, (_, row) in enumerate(
        meals.iterrows()
    ):

        with picker_cols[index % 2]:

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

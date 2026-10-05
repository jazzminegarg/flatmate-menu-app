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

/* ---------- INLINE CALENDAR POPOVER CARDS ---------- */

/* Streamlit popover buttons are the actual calendar cards. */

div[data-testid="stHorizontalBlock"] .stPopover {
    margin: 0 6px 5px;
}

div[data-testid="stHorizontalBlock"] .stPopover > button {
    width: 100% !important;
    height: 77px !important;
    min-height: 77px !important;

    background: #FCFAFB !important;
    color: #423A3D !important;

    border: 1px solid #E9E0E3 !important;
    border-radius: 12px !important;

    padding: 7px !important;

    font-size: 0.68rem !important;
    font-weight: 700 !important;
    line-height: 1.25 !important;

    box-shadow: none !important;
}

div[data-testid="stHorizontalBlock"] .stPopover > button:hover {
    background: #FFF7F9 !important;
    color: #A55C6A !important;
    border-color: #D998A4 !important;
    transform: translateY(-1px);
}

.popover-title {
    color: #40383B;
    font-size: 0.98rem;
    font-weight: 800;
}

.popover-subtitle {
    color: #9A8C91;
    font-size: 0.7rem;
    margin: 2px 0 12px;
}

/* Compact popover controls */

div[data-testid="stPopoverBody"] {
    min-width: 260px;
}

div[data-testid="stPopoverBody"] div[data-baseweb="select"] > div {
    border-radius: 10px !important;
    border-color: #E4DADD !important;
    background: #FFFBFC !important;
}

div[data-testid="stPopoverBody"] .stButton > button {
    min-height: 38px !important;
    height: 38px !important;
    border-radius: 10px !important;
    font-size: 0.7rem !important;
}

/* Empty-looking card */
div[data-testid="stPopover"] > button[aria-label*="choose"] {
    background: #FFFDFD !important;
    border-style: dashed !important;
    color: #7D7075 !important;
}

/* ---------- SEPARATOR BETWEEN MEAL TYPES ---------- */

.slot-divider {
    height: 1px;
    background: #EEE7E9;
    margin: 3px 0;
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


def get_current_user_meal_id(day, meal_type, person):
    target = f"{day}_{meal_type}"

    matches = df[
        df[person].str.contains(
            target,
            regex=False,
            na=False,
        )
    ]

    if matches.empty:
        return None

    return str(matches.iloc[0]["Meal_ID"])


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
        is_today = current_date == today

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

for meal_index, (meal_icon, meal_type) in enumerate(MEAL_TYPES):

    # Small meal label above each row.
    label_cols = st.columns(7, gap="small")

    for col in label_cols:
        with col:
            st.markdown(
                f'<div class="slot-label">{meal_icon} {meal_type}</div>',
                unsafe_allow_html=True,
            )

    # Every calendar card is now a popover.
    # Nothing opens below the calendar.
    meal_cols = st.columns(7, gap="small")

    for col, day in zip(meal_cols, DAYS):

        with col:

            winning_meal, voters, votes = get_slot_info(
                day,
                meal_type,
            )

            slot = f"{day}_{meal_type}"

            current_user_meal = get_current_user_meal_id(
                day,
                meal_type,
                user,
            )

            if winning_meal is None:
                button_label = "＋  choose"
            else:
                name = get_meal_name(winning_meal)
                count = len(voters)

                if count == len(USERS):
                    button_label = f"🍛 {name}  ·  ✓"
                else:
                    button_label = f"🍛 {name}  ·  {count}/3"

            # Popover is attached directly to the calendar card.
            with st.popover(
                button_label,
                use_container_width=True,
            ):

                st.markdown(
                    f"""
                    <div class="popover-title">
                        {meal_icon} {day} · {meal_type}
                    </div>
                    <div class="popover-subtitle">
                        choose your meal, {user} ♡
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                meal_options = df[
                    ["Meal_ID", "Meal_Name"]
                ].copy()

                meal_options["Meal_ID"] = (
                    meal_options["Meal_ID"]
                    .astype(str)
                )

                meal_options["Meal_Name"] = (
                    meal_options["Meal_Name"]
                    .astype(str)
                )

                option_ids = meal_options["Meal_ID"].tolist()
                option_names = meal_options["Meal_Name"].tolist()

                if current_user_meal in option_ids:
                    default_index = option_ids.index(
                        current_user_meal
                    )
                else:
                    default_index = 0

                selected_id = st.selectbox(
                    "Meal",
                    option_ids,
                    index=default_index,
                    format_func=lambda meal_id: (
                        dict(
                            zip(option_ids, option_names)
                        ).get(
                            str(meal_id),
                            str(meal_id),
                        )
                    ),
                    key=f"select_{slot}",
                    label_visibility="collapsed",
                )

                save_col, clear_col = st.columns(2)

                with save_col:
                    save_clicked = st.button(
                        "Save ♡",
                        key=f"save_{slot}",
                        use_container_width=True,
                    )

                with clear_col:
                    close_clicked = st.button(
                        "Close",
                        key=f"close_{slot}",
                        use_container_width=True,
                    )

                if save_clicked:

                    saved = save_vote(
                        selected_id,
                        user,
                        slot,
                    )

                    if saved:
                        st.toast(
                            f"Saved for {day} {meal_type} ♡"
                        )
                        st.rerun()

                if close_clicked:
                    st.rerun()

    # Subtle separator between breakfast/lunch/dinner.
    if meal_index < len(MEAL_TYPES) - 1:
        st.markdown(
            '<div class="slot-divider"></div>',
            unsafe_allow_html=True,
        )


st.markdown(
    '</div></div>',
    unsafe_allow_html=True,
)


# ============================================================
# FOOTER
# ============================================================

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

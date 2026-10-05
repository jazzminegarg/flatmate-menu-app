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
# DESIGN
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   PAGE
   ============================================================ */

.stApp {
    background: #FAF7F8;
    color: #383134;
}

.main .block-container {
    max-width: 1480px;
    padding: 0.85rem 1.35rem 1.4rem;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

/* ============================================================
   HEADER
   ============================================================ */

.app-title {
    text-align: center;
    color: #302A2D;
    font-size: 2.25rem;
    font-weight: 800;
    letter-spacing: -1.8px;
    line-height: 1;
    margin: 0;
}

.app-subtitle {
    text-align: center;
    color: #A09297;
    font-size: 0.78rem;
    margin: 5px 0 8px;
}

/* ============================================================
   PROFILE
   ============================================================ */

div[data-testid="stSelectbox"].profile-box {
    max-width: 260px;
    margin: 7px auto 5px;
}

/* Streamlit does not preserve custom class names on every version,
   so this also targets the first selectbox by its position. */
div[data-testid="stSelectbox"] > div {
    border-radius: 11px;
}

div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #E4DADD !important;
    border-radius: 11px !important;
    color: #554B50 !important;
    box-shadow: none !important;
}

.user-row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 6px;
    margin: 9px 0 4px;
}

.user-pill {
    background: #FFFFFF;
    border: 1px solid #E5DBDE;
    border-radius: 999px;
    padding: 5px 10px;
    color: #817479;
    font-size: 0.68rem;
}

.user-pill.active {
    background: #F7E2E7;
    border-color: #E0AAB5;
    color: #A85D6C;
    font-weight: 750;
}

.progress {
    text-align: center;
    color: #9C8E93;
    font-size: 0.68rem;
    margin: 6px 0 12px;
}

/* ============================================================
   CALENDAR OUTER CARD
   ============================================================ */

.calendar-shell {
    background: #FFFFFF;
    border: 1px solid #E6DDE0;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 6px 22px rgba(77, 53, 60, 0.055);
}

.calendar-inner {
    width: 100%;
}

/* Remove spacing between the 7 calendar columns. */
.calendar-inner div[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    align-items: stretch !important;
}

.calendar-inner div[data-testid="column"] {
    padding: 0 !important;
}

/* ============================================================
   DAY HEADERS
   ============================================================ */

.day-header {
    height: 58px;
    box-sizing: border-box;
    text-align: center;
    padding: 8px 3px 5px;
    background: #FFFDFD;
    border-right: 1px solid #F0E9EB;
    border-bottom: 1px solid #ECE4E7;
}

.day-header.today {
    background: #F9E8EC;
}

.day-name {
    color: #9B8C92;
    font-size: 0.56rem;
    font-weight: 800;
    letter-spacing: 1.05px;
    text-transform: uppercase;
}

.day-number {
    color: #393235;
    font-size: 1.18rem;
    font-weight: 800;
    line-height: 1.18;
}

.today-pill {
    display: inline-block;
    margin-top: 1px;
    color: #A65B6A;
    background: #FFFFFF;
    border-radius: 999px;
    padding: 1px 5px;
    font-size: 0.42rem;
    font-weight: 800;
    letter-spacing: 0.65px;
    text-transform: uppercase;
}

/* ============================================================
   MEAL ROW LABELS
   ============================================================ */

.slot-label {
    color: #9A8C91;
    font-size: 0.54rem;
    font-weight: 800;
    letter-spacing: 0.72px;
    text-transform: uppercase;
    padding: 7px 7px 3px;
    height: 27px;
    box-sizing: border-box;
}

/* ============================================================
   INLINE DROPDOWN CARDS
   ============================================================ */

/*
   There is deliberately NO separate picker below the calendar.

   Every calendar cell is one compact selectbox:
       click card → dropdown opens → choose meal → auto-saves.
*/

.calendar-inner div[data-testid="stSelectbox"] {
    margin: 0 5px 7px !important;
    width: calc(100% - 10px) !important;
}

.calendar-inner div[data-baseweb="select"] > div {
    min-height: 58px !important;
    height: 58px !important;
    box-sizing: border-box !important;

    background: #FFFDFD !important;
    color: #5D5257 !important;

    border: 1px solid #E7DDE0 !important;
    border-radius: 11px !important;

    box-shadow: 0 1px 2px rgba(70, 45, 52, 0.025) !important;

    padding: 0 7px !important;

    transition:
        background-color 120ms ease,
        border-color 120ms ease,
        box-shadow 120ms ease !important;
}

.calendar-inner div[data-baseweb="select"] > div:hover {
    background: #FFF7F9 !important;
    border-color: #DCA4AF !important;
    box-shadow: 0 3px 10px rgba(170, 90, 105, 0.075) !important;
}

/* The selected text inside the card. */
.calendar-inner div[data-baseweb="select"] span {
    color: #5D5257 !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
}

/* Dropdown arrow. */
.calendar-inner div[data-baseweb="select"] svg {
    color: #B57A85 !important;
}

/* ============================================================
   DROPDOWN MENU
   ============================================================ */

div[data-baseweb="popover"] {
    border-radius: 12px !important;
}

div[data-baseweb="popover"] ul {
    background: #FFFCFD !important;
    border: 1px solid #E4DADD !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 30px rgba(70, 45, 52, 0.12) !important;
    padding: 4px !important;
}

div[data-baseweb="popover"] li {
    color: #5D5257 !important;
    font-size: 0.7rem !important;
    border-radius: 8px !important;
}

div[data-baseweb="popover"] li:hover {
    background: #F9E8EC !important;
    color: #A65D6C !important;
}

/* ============================================================
   ROW SEPARATORS
   ============================================================ */

.slot-divider {
    height: 1px;
    background: #EEE7E9;
    margin: 1px 0;
}

/* ============================================================
   STREAMLIT TOAST
   ============================================================ */

div[data-testid="stToast"] {
    background: #FFF8FA !important;
    border: 1px solid #E5B8C1 !important;
    color: #8F5360 !important;
}

/* ============================================================
   FOOTER
   ============================================================ */

.footer-note {
    text-align: center;
    color: #B4A7AC;
    font-size: 0.58rem;
    padding-top: 11px;
}

/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 900px) {
    .main .block-container {
        padding-left: 0.25rem;
        padding-right: 0.25rem;
    }

    .calendar-shell {
        overflow-x: auto;
    }

    .calendar-inner {
        min-width: 910px;
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

    data["Meal_ID"] = (
        data["Meal_ID"]
        .astype(str)
        .str.strip()
    )

    data["Meal_Name"] = (
        data["Meal_Name"]
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

    return str(
        matches.iloc[0]["Meal_ID"]
    )


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
            # Apps Script can occasionally return a redirect/html
            # response even though the write succeeded.
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
    key="active_user",
)


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


# ============================================================
# DAY HEADERS
# ============================================================

header_cols = st.columns(
    7,
    gap="small",
)

for col, day in zip(
    header_cols,
    DAYS,
):

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


# ============================================================
# BREAKFAST / LUNCH / DINNER
# ============================================================

for meal_index, (meal_icon, meal_type) in enumerate(
    MEAL_TYPES
):

    # Row labels.
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

    # Seven actual dropdowns.
    meal_cols = st.columns(
        7,
        gap="small",
    )

    for col, day in zip(
        meal_cols,
        DAYS,
    ):

        with col:

            slot = f"{day}_{meal_type}"

            current_user_meal = (
                get_current_user_meal_id(
                    day,
                    meal_type,
                    user,
                )
            )

            winning_meal, voters, _ = (
                get_slot_info(
                    day,
                    meal_type,
                )
            )

            # Options are IDs because IDs are what the Apps Script writes.
            # The placeholder makes an unvoted slot look like "choose".
            meal_ids = (
                ["__EMPTY__"]
                + df["Meal_ID"].astype(str).tolist()
            )

            meal_lookup = dict(
                zip(
                    df["Meal_ID"].astype(str),
                    df["Meal_Name"].astype(str),
                )
            )

            slot_votes = get_votes_for_slot(
                day,
                meal_type,
            )

            def format_meal(meal_id):
                if meal_id == "__EMPTY__":
                    return "＋  choose"

                meal_name = meal_lookup.get(
                    str(meal_id),
                    str(meal_id),
                )

                vote_count = sum(
                    1
                    for voted_meal in slot_votes.values()
                    if str(voted_meal) == str(meal_id)
                )

                if vote_count == len(USERS):
                    return f"🍛  {meal_name}  ·  ✓"

                if vote_count > 0:
                    return f"🍛  {meal_name}  ·  {vote_count}/3"

                return f"🍛  {meal_name}"

            if current_user_meal in meal_ids:
                default_index = meal_ids.index(
                    current_user_meal
                )
            else:
                default_index = 0

            # A unique key is essential so Streamlit can tell that
            # this particular calendar cell changed.
            widget_key = (
                f"meal_{user}_{slot}"
            )

            # If the user changed this dropdown, this value is the
            # new selection during this rerun.
            selected_id = st.selectbox(
                "meal",
                meal_ids,
                index=default_index,
                format_func=format_meal,
                key=widget_key,
                label_visibility="collapsed",
            )

            # Auto-save immediately after a real change.
            if (
                selected_id != "__EMPTY__"
                and str(selected_id)
                != str(current_user_meal)
            ):

                with st.spinner("saving ♡"):

                    saved = save_vote(
                        selected_id,
                        user,
                        slot,
                    )

                if saved:

                    st.toast(
                        f"Saved {day} {meal_type} ♡",
                        icon="♡",
                    )

                    st.rerun()

    # Small divider between meal groups.
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

st.markdown(
    """
    <div class="footer-note">
        made for the flat ♡
    </div>
    """,
    unsafe_allow_html=True,
)

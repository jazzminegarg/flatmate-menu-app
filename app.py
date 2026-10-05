import streamlit as st
import pandas as pd
import requests

# --------------------------------------------------------------------
# 1. APPLICATION & DB SETTINGS
# --------------------------------------------------------------------
SHEET_ID = "1XCwQ23-1RlkqKcHo6ECj6WDGMa3TUKxHc5AoB48CoBI"
READ_URL = f"https://google.com{SHEET_ID}/export?format=csv&gid=0"
API_URL = "YOUR_GOOGLE_WEB_APP_URL_HERE" 

st.set_page_config(page_title="Drag Menu Planner", page_icon="📅", layout="wide")

# Visual Styling to mimic a slick canvas dashboard
st.markdown("""
    <style>
    .dish-pill {
        background: #ff4b4b; padding: 10px 14px; border-radius: 20px;
        color: white; font-weight: bold; text-align: center; margin-bottom: 8px;
        cursor: grab; box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .cal-slot {
        background: #1e1e24; border: 2px dashed #3a3a42; border-radius: 10px;
        padding: 12px; min-height: 80px; text-align: center; margin-bottom: 10px;
    }
    .matched-box {
        background: #1c3d27; border: 2px solid #2e7d32; border-radius: 10px;
        color: #81c784; padding: 12px; font-weight: bold; text-align: center; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📅 Flatmate Drag & Drop Menu Board")
st.write("Drag or click items from your kitchen inventory directly into calendar slots.")

# Fetch active database states
try:
    df = pd.read_csv(READ_URL)
    df.columns = df.columns.str.strip()
except Exception:
    st.error("Database connection offline. Verify your Google Sheet share settings.")
    st.stop()

# Sanitize voting columns
for col in ['Aashi', 'Meera', 'Jasmine']:
    df[col] = df[col].fillna("").astype(str).str.strip()

# --------------------------------------------------------------------
# 2. TWO-COLUMN LAYOUT (SIDE SHELF VS CALENDAR CANVAS)
# --------------------------------------------------------------------
col_shelf, col_canvas = st.columns([1, 2], gap="large")

with col_shelf:
    st.subheader("🍲 Sabzi Inventory")
    st.caption("Select your flatmate profile:")
    user = st.selectbox("Active User:", ["Select Profile", "Aashi", "Meera", "Jasmine"])
    
    st.write("---")
    st.write("💡 *Click a meal below to pick it up, then assign it to a day on the right!*")
    
    # Render active list of database options as actionable items
    selected_meal = None
    for _, row in df.iterrows():
        if st.button(f"🥘 {row['Meal_Name']}", key=f"btn_{row['Meal_ID']}", use_container_width=True):
            st.session_state['active_pickup'] = row['Meal_Name']
            st.session_state['active_pickup_id'] = row['Meal_ID']
            
    if 'active_pickup' in st.session_state:
        st.info(f"Holding: **{st.session_state['active_pickup']}** 🖐️")

with col_canvas:
    st.subheader("🗓️ 7-Day Master Calendar")
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    if user == "Select Profile":
        st.warning("Please select your profile name on the left sidebar to start assigning slots.")
    else:
        # Generate responsive structural view grid
        for day in days:
            st.markdown(f"### {day}")
            col_l, col_d = st.columns(2)
            
            # Check for Consensus Matches automatically across your columns
            lunch_match = df[df['Aashi'].str.contains(f"{day}_Lunch", na=False) & 
                             df['Meera'].str.contains(f"{day}_Lunch", na=False) & 
                             df['Jasmine'].str.contains(f"{day}_Lunch", na=False)]
            
            dinner_match = df[df['Aashi'].str.contains(f"{day}_Dinner", na=False) & 
                              df['Meera'].str.contains(f"{day}_Dinner", na=False) & 
                              df['Jasmine'].str.contains(f"{day}_Dinner", na=False)]
            
            # LUNCH SLOT
            with col_l:
                if not lunch_match.empty:
                    st.markdown(f"<div class='matched-box'>☀️ Lunch<br>✨ {lunch_match.iloc['Meal_Name']} ✨</div>", unsafe_allow_html=True)
                else:
                    if st.button(f"📥 Drop in {day} Lunch", key=f"drop_{day}_lunch"):
                        if 'active_pickup' in st.session_state:
                            m_id = st.session_state['active_pickup_id']
                            slot_str = f"{day}_Lunch"
                            if API_URL != "YOUR_GOOGLE_WEB_APP_URL_HERE":
                                requests.get(f"{API_URL}?mealId={m_id}&roomie={user}&vote={slot_str}")
                            st.success(f"Placed {st.session_state['active_pickup']}!")
                            st.session_state.pop('active_pickup')
                            st.rerun()
                        else:
                            st.warning("Pick up a meal from the left menu first!")
            
            # DINNER SLOT
            with col_d:
                if not dinner_match.empty:
                    st.markdown(f"<div class='matched-box'>🌙 Dinner<br>✨ {dinner_match.iloc['Meal_Name']} ✨</div>", unsafe_allow_html=True)
                else:
                    if st.button(f"📥 Drop in {day} Dinner", key=f"drop_{day}_dinner"):
                        if 'active_pickup' in st.session_state:
                            m_id = st.session_state['active_pickup_id']
                            slot_str = f"{day}_Dinner"
                            if API_URL != "YOUR_GOOGLE_WEB_APP_URL_HERE":
                                requests.get(f"{API_URL}?mealId={m_id}&roomie={user}&vote={slot_str}")
                            st.success(f"Placed {st.session_state['active_pickup']}!")
                            st.session_state.pop('active_pickup')
                            st.rerun()
                        else:
                            st.warning("Pick up a meal from the left menu first!")

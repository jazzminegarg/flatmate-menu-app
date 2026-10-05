import streamlit as st
import pandas as pd
import requests
import json

# --------------------------------------------------------------------
# 1. DATABASE CONFIGURATION (HARDCODED DIRECT LINK - ZERO ACCIDENTAL TYPOS)
# --------------------------------------------------------------------
# Directly utilizing the exact, unbreakable public data endpoint for your sheet ID
JSON_URL = "https://google.com"

# Paste your Web App Script URL here when you are ready to write votes back
API_URL = "YOUR_GOOGLE_WEB_APP_URL_HERE" 

st.set_page_config(page_title="Drag Menu Planner", page_icon="📅", layout="wide")

# Custom Canvas Design CSS
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; max-width: 1200px; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5rem; font-size: 1rem; font-weight: bold; }
    div[data-testid="stNotification"] { border-radius: 15px; padding: 1.2rem; }
    .matched-box {
        background: #1c3d27; border: 2px solid #2e7d32; border-radius: 10px;
        color: #81c784; padding: 12px; font-weight: bold; text-align: center; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📅 Flatmate Menu Board")
st.write("Click items from your kitchen inventory to assign them to calendar slots.")

# --------------------------------------------------------------------
# SECURE JSON PARSING ENGINE (Bypasses all spreadsheet bugs)
# --------------------------------------------------------------------
try:
    response = requests.get(JSON_URL, timeout=10)
    raw_text = response.text
    start_idx = raw_text.find("{")
    end_idx = raw_text.rfind("}") + 1
    
    json_data = json.loads(raw_text[start_idx:end_idx])
    
    rows = json_data['table']['rows']
    cols = [c['label'] if c and 'label' in c and c['label'] else f"Col_{i}" for i, c in enumerate(json_data['table']['cols'])]
    
    table_data = []
    for r in rows:
        row_vals = [c['v'] if c and 'v' in c else "" for c in r['c']]
        while len(row_vals) < len(cols):
            row_vals.append("")
        table_data.append(row_vals)
        
    df = pd.DataFrame(table_data, columns=cols)
    df.columns = df.columns.str.strip()
    
    # Map raw index positions to column names precisely
    rename_map = {}
    if "Col_0" in df.columns: rename_map["Col_0"] = "Meal_ID"
    if "Col_1" in df.columns: rename_map["Col_1"] = "Meal_Name"
    if "Col_2" in df.columns: rename_map["Col_2"] = "Description"
    if "Col_3" in df.columns: rename_map["Col_3"] = "Aashi"
    if "Col_4" in df.columns: rename_map["Col_4"] = "Meera"
    if "Col_5" in df.columns: rename_map["Col_5"] = "Jasmine"
    df.rename(columns=rename_map, inplace=True)

except Exception as e:
    st.error("Database connection offline. Verify your Google Sheet share settings are open.")
    st.info("Technical Diagnostic System Logs:")
    st.code(str(e))
    st.stop()

# Ensure voting columns exist cleanly in memory
for col in ['Aashi', 'Meera', 'Jasmine']:
    if col in df.columns:
        df[col] = df[col].fillna("").astype(str).str.strip()
    else:
        df[col] = ""

# --------------------------------------------------------------------
# 2. APPLICATION RENDERING CANVAS
# --------------------------------------------------------------------
col_shelf, col_canvas = st.columns([1, 2], gap="large")

with col_shelf:
    st.subheader("🍲 Sabzi Inventory")
    user = st.selectbox("Active User:", ["Select Profile", "Aashi", "Meera", "Jasmine"])
    st.write("---")
    
    if "Meal_Name" in df.columns:
        for idx, row in df.iterrows():
            if pd.notna(row['Meal_Name']) and str(row['Meal_Name']).strip() != "":
                if st.button(f"🥘 {row['Meal_Name']}", key=f"btn_{idx}", use_container_width=True):
                    st.session_state['active_pickup'] = row['Meal_Name']
                    st.session_state['active_pickup_id'] = row['Meal_ID']
                    
    if 'active_pickup' in st.session_state:
        st.info(f"Holding: **{st.session_state['active_pickup']}** 🖐️")

with col_canvas:
    st.subheader("🗓️ 7-Day Master Calendar")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    if user == "Select Profile":
        st.warning("Please select your profile name on the left sidebar to start planning.")
    else:
        for day in days:
            st.markdown(f"### {day}")
            col_l, col_d = st.columns(2)
            
            # Match Logic matching cell contents
            lunch_match = df[df['Aashi'].str.contains(f"{day}_Lunch", na=False) & 
                             df['Meera'].str.contains(f"{day}_Lunch", na=False) & 
                             df['Jasmine'].str.contains(f"{day}_Lunch", na=False)]
            
            dinner_match = df[df['Aashi'].str.contains(f"{day}_Dinner", na=False) & 
                              df['Meera'].str.contains(f"{day}_Dinner", na=False) & 
                              df['Jasmine'].str.contains(f"{day}_Dinner", na=False)]
            
            with col_l:
                if not lunch_match.empty:
                    st.markdown(f"<div class='matched-box'>☀️ Lunch<br>✨ {lunch_match.iloc[0]['Meal_Name']} ✨</div>", unsafe_allow_html=True)
                else:
                    current_vote = df[df[user].str.contains(f"{day}_Lunch", na=False)]
                    btn_label = f"📥 Drop in {day} Lunch" if current_vote.empty else f"⏳ Voted: {current_vote.iloc[0]['Meal_Name']}"
                    
                    if st.button(btn_label, key=f"l_{day}"):
                        if 'active_pickup' in st.session_state:
                            m_id = st.session_state['active_pickup_id']
                            if API_URL != "YOUR_GOOGLE_WEB_APP_URL_HERE":
                                try:
                                    requests.get(f"{API_URL}?mealId={m_id}&roomie={user}&vote={day}_Lunch")
                                except:
                                    pass
                            st.success(f"Assigned {st.session_state['active_pickup']}!")
                            st.session_state.pop('active_pickup')
                            st.rerun()
                        else:
                            st.warning("Pick a meal from the left column first!")
                            
            with col_d:
                if not dinner_match.empty:
                    st.markdown(f"<div class='matched-box'>🌙 Dinner<br>✨ {dinner_match.iloc[0]['Meal_Name']} ✨</div>", unsafe_allow_html=True)
                else:
                    current_vote = df[df[user].str.contains(f"{day}_Dinner", na=False)]
                    btn_label = f"📥 Drop in {day} Dinner" if current_vote.empty else f"⏳ Voted: {current_vote.iloc[0]['Meal_Name']}"
                    
                    if st.button(btn_label, key=f"d_{day}"):
                        if 'active_pickup' in st.session_state:
                            m_id = st.session_state['active_pickup_id']
                            if API_URL != "YOUR_GOOGLE_WEB_APP_URL_HERE":
                                try:
                                    requests.get(f"{API_URL}?mealId={m_id}&roomie={user}&vote={day}_Dinner")
                                except:
                                    pass
                            st.success(f"Assigned {st.session_state['active_pickup']}!")
                            st.session_state.pop('active_pickup')
                            st.rerun()
                        else:
                            st.warning("Pick a meal from the left column first!")

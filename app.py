import streamlit as st
import pandas as pd
import requests

# --------------------------------------------------------------------
# 1. DATABASE CONFIGURATION (YOUR MATCHED LINK ID)
# --------------------------------------------------------------------
SHEET_ID = "1XCwQ23-1RlkqKcHo6ECj6WDGMa3TUKxHc5AoB48CoBI"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# PASTE YOUR GOOGLE WEB APP URL HERE:
API_URL = "YOUR_GOOGLE_WEB_APP_URL_HERE" 

st.set_page_config(page_title="Flatmate Menu App", page_icon="🍲", layout="centered")

# Mobile Optimization CSS
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; max-width: 420px; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.8rem; font-size: 1.1rem; font-weight: bold; }
    div[data-testid="stNotification"] { border-radius: 15px; padding: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍲 Flatmate Menu Swiper")
st.write("Swipe through meals to build next week's menu together.")

# --------------------------------------------------------------------
# 2. PROFILE SELECTOR (UPDATED TO MATCH YOUR SPREADSHEET HEADERS)
# --------------------------------------------------------------------
flatmates = ["Select Profile", "Aashi", "Meera", "Jasmine"]
current_user = st.selectbox("Who is swiping right now?", flatmates)

if current_user != "Select Profile":
    try:
        # Fetching data feed directly from your link
        df = pd.read_csv(READ_URL)
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error("Could not fetch data from Google Sheets.")
        st.info("Double-check that your Google Sheet's Share settings are explicitly set to 'Anyone with the link can edit'.")
        st.stop()

    # The column in your spreadsheet is exactly the flatmate's name (e.g., 'Aashi')
    user_col = current_user
    
    # Safely handle the Description column whether it is completely missing or empty
    has_description = 'Description' in df.columns
    if has_description:
        df['Description'] = df['Description'].fillna("").astype(str).str.strip()

    # Verify that the voting column exists
    if user_col in df.columns:
        df[user_col] = df[user_col].fillna("None").astype(str).str.strip()
        unvoted_meals = df[df[user_col] == "None"]
    else:
        st.error(f"Column '{user_col}' missing from your Google Sheet headers. Available headers: {list(df.columns)}")
        st.stop()

    # --------------------------------------------------------------------
    # 3. VOTING INTERFACE
    # --------------------------------------------------------------------
    if not unvoted_meals.empty:
        current_row = unvoted_meals.iloc[0]
        meal_id = current_row['Meal_ID']
        
        # Display the meal card 
        if has_description and current_row['Description'] != "":
            st.info(f"### {current_row['Meal_Name']}\n\n*{current_row['Description']}*")
        else:
            st.info(f"### {current_row['Meal_Name']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ DISLIKE", key="dislike_btn"):
                if API_URL != "YOUR_GOOGLE_WEB_APP_URL_HERE":
                    try:
                        requests.get(f"{API_URL}?mealId={meal_id}&roomie={current_user}&vote=Dislike", timeout=5)
                    except:
                        pass
                st.toast(f"Skipped {current_row['Meal_Name']}")
                st.rerun()
                
        with col2:
            if st.button("💚 LIKE", key="like_btn"):
                if API_URL != "YOUR_GOOGLE_WEB_APP_URL_HERE":
                    try:
                        requests.get(f"{API_URL}?mealId={meal_id}&roomie={current_user}&vote=Like", timeout=5)
                    except:
                        pass
                st.toast(f"Added {current_row['Meal_Name']} to choices!")
                st.rerun()
    else:
        st.success("🎉 You've swiped through all available meals!")

    # --------------------------------------------------------------------
    # 4. LIVE MATCHES CONSENSUS VIEW
    # --------------------------------------------------------------------
    st.markdown("### 📋 Final Group Consensus Matches")
    st.caption("Meals liked by Aashi, Meera, and Jasmine populate here:")

    # Clean data columns
    vote_cols = ['Aashi', 'Meera', 'Jasmine']
    for col in vote_cols:
        if col in df.columns:
            df[col] = df[col].fillna("None").astype(str).str.strip()
        else:
            df[col] = "None"

    # Match algorithm
    consensus_df = df[
        (df['Aashi'] == "Like") & 
        (df['Meera'] == "Like") & 
        (df['Jasmine'] == "Like")
    ]

    if not consensus_df.empty:
        for _, row in consensus_df.iterrows():
            if has_description and row['Description'] != "":
                st.markdown(f"✅ **{row['Meal_Name']}** — *{row['Description']}*")
            else:
                st.markdown(f"✅ **{row['Meal_Name']}**")
    else:
        st.warning("No uniform matches found yet. Keep swiping!")

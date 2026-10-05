import streamlit as st
import pandas as pd
import requests

# --------------------------------------------------------------------
# 1. DATABASE CONFIGURATION
# --------------------------------------------------------------------
SHEET_ID = "1XCwQ23-1RlkqKcHo6ECj6WDGMa3TUKxHc5AoB48CoBI"
READ_URL = f"https://google.com{SHEET_ID}/export?format=csv&gid=0"

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
# 2. PROFILE SELECTOR
# --------------------------------------------------------------------
flatmates = ["Select Profile", "Roomie1", "Roomie2", "Roomie3"]
current_user = st.selectbox("Who is swiping right now?", flatmates)

if current_user != "Select Profile":
    try:
        # Load spreadsheet data
        df = pd.read_csv(READ_URL)
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error("Could not fetch data from Google Sheets.")
        st.info("Check that your Google Sheet's Share settings are set to 'Anyone with the link can edit'.")
        st.stop()

    user_col = f"{current_user}_Vote"
    
    # Safely handle the Description column whether it is completely missing or empty
    has_description = 'Description' in df.columns
    if has_description:
        df['Description'] = df['Description'].fillna("").astype(str).str.strip()

    # Verify that the required user voting column exists
    if user_col in df.columns:
        df[user_col] = df[user_col].fillna("None").astype(str).str.strip()
        unvoted_meals = df[df[user_col] == "None"]
    else:
        st.error(f"Column '{user_col}' missing from your Google Sheet headers. Please check Row 1 spelling.")
        st.stop()

    # --------------------------------------------------------------------
    # 3. SWIPING / VOTING INTERFACE
    # --------------------------------------------------------------------
    if not unvoted_meals.empty:
        current_row = unvoted_meals.iloc[0]
        meal_id = current_row['Meal_ID']
        
        # Display the meal card (displays description only if it has text)
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
    st.caption("Meals liked by ALL 3 flatmates populate here:")

    # Sanitize and fill the rest of the roomie columns to avoid sorting errors
    vote_cols = ['Roomie1_Vote', 'Roomie2_Vote', 'Roomie3_Vote']
    for col in vote_cols:
        if col in df.columns:
            df[col] = df[col].fillna("None").astype(str).str.strip()
        else:
            df[col] = "None"

    # Filter out absolute matches where everyone voted 'Like'
    consensus_df = df[
        (df['Roomie1_Vote'] == "Like") & 
        (df['Roomie2_Vote'] == "Like") & 
        (df['Roomie3_Vote'] == "Like")
    ]

    if not consensus_df.empty:
        for _, row in consensus_df.iterrows():
            if has_description and row['Description'] != "":
                st.markdown(f"✅ **{row['Meal_Name']}** — *{row['Description']}*")
            else:
                st.markdown(f"✅ **{row['Meal_Name']}**")
    else:
        st.warning("No uniform matches found yet. Keep swiping!")

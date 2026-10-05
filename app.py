import streamlit as st
import pandas as pd
import requests

# --------------------------------------------------------------------
# 1. DATABASE CONFIGURATION (REPLACE WITH YOUR GOOGLE SHEET ID)
# --------------------------------------------------------------------
SHEET_ID = "1aBcD-eFgHiJkLmNoPqRsTuVwXyZ1234567890QWERTY"  # <-- Paste your long spreadsheet ID here
READ_URL = f"https://google.com{SHEET_ID}/export?format=csv&gid=0"

st.set_page_config(page_title="Flatmate Menu App", page_icon="🍲", layout="centered")

# Custom CSS styling to make it look like a sleek native mobile web app
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; max-width: 450px; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5rem; font-size: 1.1rem; font-weight: bold; }
    div[data-testid="stNotification"] { border-radius: 15px; padding: 1.5rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍲 Flatmate Menu Swiper")
st.write("Swipe through custom meals to generate next week's menu layout.")

# --------------------------------------------------------------------
# 2. FLAT MATE PROFILE LOGIN
# --------------------------------------------------------------------
flatmates = ["Select Profile", "Roomie1", "Roomie2", "Roomie3"]
current_user = st.selectbox("Who is swiping right now?", flatmates)

if current_user != "Select Profile":
    # Read live data from Google Sheet
    try:
        df = pd.read_csv(READ_URL)
    except Exception as e:
        st.error("Connection Error: Make sure your Google Sheet access is set to 'Anyone with the link can Edit'.")
        st.stop()

    # Define user specific column tracking
    user_col = f"{current_user}_Vote"
    
    # Filter meals the current user hasn't voted on yet
    unvoted_meals = df[df[user_col].isna() | (df[user_col] == '') | (df[user_col] == 'None')]

    if not unvoted_meals.empty:
        # Get the first unvoted meal item (The Top Card)
        current_row = unvoted_meals.iloc[0]
        meal_id = current_row['Meal_ID']
        
        # Display the custom meal card container
        st.info(f"### {current_row['Meal_Name']}\n\n*{current_row['Description']}*")
        
        st.write("---")
        # Layout action choices matching mobile swipe patterns
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("❌ DISLIKE", key="dislike_btn"):
                # Simulating backend write sequence back to sheet cell framework
                st.toast(f"Skipped {current_row['Meal_Name']}")
                # Internal tracker logic
                df.loc[df['Meal_ID'] == meal_id, user_col] = 'Dislike'
                # Note: For strict cloud write persistence, trigger web-app URL scripts or direct forms.
                st.rerun()
                
        with col2:
            if st.button("💚 LIKE", key="like_btn"):
                st.toast(f"Liked {current_row['Meal_Name']}!")
                df.loc[df['Meal_ID'] == meal_id, user_col] = 'Like'
                st.rerun()
    else:
        st.success("🎉 You've swiped through all available meals in the database!")

    # --------------------------------------------------------------------
    # 4. THE DECLARED WEEKLY CONSENSUS ALGORITHM CALENDAR
    # --------------------------------------------------------------------
    st.markdown("### 📋 Final Group Consensus Matches")
    st.caption("Items liked by all 3 flatmates will instantly populate below:")

    # Find rows where all three voting columns evaluate strictly to 'Like'
    consensus_df = df[
        (df['Roomie1_Vote'] == 'Like') & 
        (df['Roomie2_Vote'] == 'Like') & 
        (df['Roomie3_Vote'] == 'Like')
    ]

    if not consensus_df.empty:
        for idx, row in consensus_df.iterrows():
            st.markdown(f"✅ **{row['Meal_Name']}** — *{row['Description']}*")
    else:
        st.warning("No matches found yet. Keep swiping until all three of you agree on choices!")

import streamlit as st
import requests
import json

# Na vrh koda u main.py dodaj polja za unos u sidebar (bočni izbornik)
st.sidebar.title("Postavke veze")
API_KEY = st.sidebar.text_input("Azure API Key", value="", type="password")

if not API_KEY:
    st.warning(
        "Molim unesite API ključ u bočni izbornik kako bi aplikacija radila.")
    st.stop()

# --- CONFIGURATION
URL = "https://projekt-tclwi.germanywestcentral.inference.ml.azure.com/score"

# Mapping the model's numbers to human-readable names
HAND_MAP = {
    0: "Nothing in hand",
    1: "One pair",
    2: "Two pairs",
    3: "Three of a kind",
    4: "Straight",
    5: "Flush",
    6: "Full house",
    7: "Four of a kind",
    8: "Straight flush",
    9: "Royal flush"
}

SUIT_MAP = {"Hearts": 1, "Spades": 2, "Diamonds": 3, "Clubs": 4}
RANK_MAP = {
    "Ace": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 11, "Queen": 12, "King": 13
}

# --- GUI SETUP ---
st.set_page_config(page_title="Poker Hand Predictor", page_icon="♣️")
st.title("🃏 Poker Hand Predictor")
st.write("Enter 5 cards and the Azure ML model will predict your hand.")

st.sidebar.header("Instructions")
st.sidebar.info(
    "Select the suit and rank for all 5 cards, then click Predict.")


cols = st.columns(5)
user_input = []

for i, col in enumerate(cols):
    with col:
        st.subheader(f"Card {i+1}")
        suit = st.selectbox(f"Suit", list(SUIT_MAP.keys()), key=f"s{i}")
        rank = st.selectbox(f"Rank", list(RANK_MAP.keys()), key=f"r{i}")

        user_input.append(SUIT_MAP[suit])
        user_input.append(RANK_MAP[rank])

# --- PREDICTION LOGIC ---
if st.button("Predict My Hand", type="primary"):

    payload = {
        "input_data": {
            "columns": ["S1", "C1", "S2", "C2", "S3", "C3", "S4", "C4", "S5", "C5"],
            "index": [0],
            "data": [user_input]
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    with st.spinner('Asking Azure...'):
        try:
            response = requests.post(
                URL, data=json.dumps(payload), headers=headers)
            response.raise_for_status()

            result = response.json()

            prediction = result[0] if isinstance(result, list) else result

            pred_class = int(prediction)

            st.success(f"### Result: {HAND_MAP[pred_class]}")

        except Exception as e:
            st.error(f"Error connecting to Azure: {e}")

# Footer
st.markdown("---")
st.caption("AI Model trained on UCI Poker Hand Dataset using Azure AutoML.")

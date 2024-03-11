import streamlit as st
import requests
import pandas as pd
import datetime
import json

today = datetime.datetime.now()
next_year = today.year
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

min_year = 2020
max_year = 2030
min_date = datetime.date(min_year, 1, 1)
max_date = datetime.date(max_year, 12, 31)

# Streamlit UI Components
st.title("Östersund Destination AI-POC")
st.subheader("Planera ditt besök i Östersund med hjälp av AI")
st.write("Berätta mer om din vistelse i Östersund och ditt sällskap så hjälper vi dig att hitta rätt aktiviteter och upplevelser.")
user_input = st.text_area("Vilka är ni och vad vill ni hitta på?")
st.markdown("""
* _Aa_
* _Aa_
* _Aa_
""", unsafe_allow_html=True)
number_of_people = st.slider('Hur många personer är det i ert sällskap?', min_value=1, max_value=30)
arrival_dates = st.date_input(
    "När kommer ni till Östersund?",
    value=(jan_1, datetime.date(next_year, 1, 7)),
)
huvudfokus_semester = st.selectbox('Vad är huvudfokus för er semester?', ["Nöjen och äventyr", "Relax och avslappning", "Äldre människor som vill uppleva Åre", "Romantisk getaway med min partner"])
submit_button = st.button('Hitta aktiviteter')

# POST Request API
def send_post_request(input_text, number_of_people, arrival_dates, huvudfokus_semester):
    url = "https://api.retool.com/v1/workflows/19264845-59b3-4a0f-839a-4dd4654d2c73/startTrigger?workflowApiKey=retool_wk_db58371db0154924a61830a8928291a4"
    headers = {'Content-Type': 'application/json'}
    data = {
        "body": input_text, 
        "number_of_people": "Beskrivning från användare: " + str(number_of_people), 
        "arrival_start_date": "Datum för ankomst: " + arrival_dates[0].strftime("%Y-%m-%d"),  
        "arrival_and_end_date": "Datum för avfärd: " + arrival_dates[1].strftime("%Y-%m-%d"),  
        "huvudfokus_semester": "Huvudkategori:" + huvudfokus_semester
    }
    
    with st.spinner('Vi letar aktiviteter och rekommendationer...'):
        response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        data_field = response_data.get("data", "")
        return data_field
    else:
        return "Error in API response"

# Button Click
if submit_button:
    if user_input:
        data_field = send_post_request(user_input, number_of_people, arrival_dates, huvudfokus_semester)
        st.write("Response Data:")
        st.write(data_field)
    else:
        st.error("Du måste ju skriva något...")

# ULR list based on the Vector from Retool


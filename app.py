import streamlit as st
import pickle
import pandas as pd
import os

teams = [
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bengaluru',
    'Kolkata Knight Riders',
    'Punjab Kings',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals',
    'Gujarat Titans'
]

cities = ['Bangalore', 'Chandigarh', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
          'Hyderabad', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban',
          'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Rajkot', 'Kanpur', 'Bengaluru', 'Indore', 'Dubai', 'Sharjah',
          'Navi Mumbai', 'Guwahati', 'Mohali']


if os.path.exists("pipe.pkl"):
    with open("pipe.pkl", "rb") as file:
        pipe = pickle.load(file)
else:
    st.error("Model file not found. Please check deployment.")

st.title("Final Over Forecast")
st.text("A smart IPL match winning chance predictor")
st.markdown('---')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))

with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

selected_city = st.selectbox("Select city", sorted(cities))

target = st.number_input("Target")

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input("Score")

with col4:
    overs = st.number_input("Overs completed")

with col5:
    wickets = st.number_input("Wickets")

if st.button("Predict"):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame(
        {'batting_team': [batting_team],
         'bowling_team': [bowling_team],
         'city': [selected_city],
         'runs_left': [runs_left],
         'balls_left': [balls_left],
         'wickets': [wickets],
         'total_runs_x': [target],
         'crr': [crr],
         'rrr': [rrr]
         }
    )

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.markdown('---')
    st.text(batting_team + " - " + str(round(win*100)) + "%")
    st.text(bowling_team + " - " + str(round(loss*100)) + "%")
import streamlit as st
import pickle
import pandas as pd


teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Gujarat Lions',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Punjab Kings',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']

pipe = pickle.load(open('pipe.pkl','rb'))

st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Batting Team',sorted(teams))

with col2:
    bowling_team = st.selectbox('Bowling Team',sorted(teams))

selected_city = st.selectbox('City',sorted(cities))

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Current Score')

with col4:
    overs = st.number_input('Overs Completed')

with col5:
    curr_wickets = st.number_input('Current Wicket')

target = st.number_input('Target')

if st.button('Predict'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - curr_wickets
    crr = score/overs
    round_crr = round(crr,2)
    rrr = (runs_left * 6)/(balls_left)
    round_rrr = round(rrr,2)

    input_df = pd.DataFrame({'batting_team' : [batting_team] , 'bowling_team': [bowling_team],
                             'city': [selected_city] , 'runs_left' : [runs_left], 'balls_left' : [balls_left],
                             'wickets_left' : [wickets_left] , 'total_runs_x' : [target] , 'crr' : [crr] ,
                             'rrr' : [rrr]})

    #st.table(input_df)

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    st.header(batting_team + "- " + str(round(win*100)) + "%")
    st.header(bowling_team + "- " + str(round(loss*100)) + "%")

    st.text("To win " + batting_team + " needs " + str(round_rrr) + " run rate while current run rate is "+ str(round_crr))
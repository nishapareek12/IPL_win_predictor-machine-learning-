import streamlit as st
import pickle
import pandas as pd
teams =  [
    'Royal Challengers Bangalore',
    'Sunrisers Hyderabad',
    'Kolkata Knight Riders',
    'Gujarat Titans',
    'Rajasthan Royals',
    'Delhi Capitals',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Mumbai Indians'
]

cities= ['Hyderabad', 'Rajkot', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata',
       'Delhi', 'Chandigarh', 'Kanpur', 'Jaipur', 'Chennai', 'Cape Town',
       'Port Elizabeth', 'Durban', 'Centurion', 'East London',
       'Johannesburg', 'Kimberley', 'Bloemfontein', 'Ahmedabad',
       'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Pune',
       'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah']
pipe = pickle.load(open('pipe.pkl','rb'))
st.title('IPL Win Predictor')
col1,col2 = st.columns(2)
with col1:
    batting_team = st.selectbox("select batting team",teams)
with col2:
    bowling_team = st.selectbox("select bowling team",teams)

selected_city = st.selectbox('select host city',sorted(cities))
target = st.number_input('Target')
col3,col4,col5 = st.columns(3)
with col3:
    score = st.number_input('score')
with col4:
    overs = st.number_input('overs completed')
with col4:
    wickets = st.number_input('wickets_out')
if st.button('predict probability'):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets_left = (10-wickets)
    current_runrate = score/overs
    req_runrate  = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team], 'city': [selected_city],
                             'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets_left': [wickets_left],
                             'total_runs_x': [target], 'current_runrate': [current_runrate], 'req_runrate': [req_runrate]})

    result  = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + '-' + str(round(win*100)) + "%")
    st.header(bowling_team + '-' + str(round(loss * 100)) + "%")
    
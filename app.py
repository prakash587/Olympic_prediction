import streamlit as st
import pandas as pd

import helper
import preprocessor

df = pd.read_csv('athlete_events.csv')
country_df=pd.read_csv('country_definitions.csv')

df = preprocessor.preprocess(df,country_df)
st.sidebar.title('OLYMPICS ANALYSIS')

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis' , 'Country-wise Analysis', 'Athlete wise Analysis')
)


if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)


    medal_tally= helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_country ==  'overall' and selected_year == 'overall':
        st.title('Overall Tally')
    if selected_year !='overall' and selected_country == 'overall':
        st.title('Medal Tally in ' + str(selected_year) + " Olympics")
    if selected_year == 'overall' and selected_country != 'overall':
        st.title(selected_country  + " Overall Performance in Olympics")
    if selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)
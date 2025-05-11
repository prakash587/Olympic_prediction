import streamlit as st
import pandas as pd

import helper
import preprocessor

df = pd.read_csv('athlete_events.csv')
country_df=pd.read_csv('country_definitions.csv')

df = preprocessor.preprocess(df,country_df)


user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis' , 'Country-wise Analysis', 'Athlete wise Analysis')
)


if user_menu == 'Medal Tally':
    medal_tally= helper.medal_tally(df)
    st.dataframe(medal_tally)
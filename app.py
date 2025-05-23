import streamlit as st
import pandas as pd

import helper
import preprocessor
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

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

if user_menu ==  'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]


    st.title('Top Statistics')

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)

    with col2:
        st.header('Hosts')
        st.title(cities)

    with col3:
        st.header('Sports')
        st.title(sports)


    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)

    with col2:
        st.header('Nations')
        st.title(nations)

    with col3:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title('Participating Nations over the Year')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title('Events  over the Year')
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title('Athlete  over the Year')
    st.plotly_chart(fig)

    st.title("No. of Events Over the time(Every Sport")
    fig,ax = plt.subplots(figsize=(25,25))

    x = df.drop_duplicates(subset=['Year', 'Sport', 'Event'])

    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'overall')

    selected_sport = st.selectbox("Select Sport", sport_list)
    x= helper.most_successful(df, selected_sport)
    st.table(x)


if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select Country", country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)

    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + "Medal tally over the year")
    st.plotly_chart(fig)

    st.title(selected_country + " excels on the following year")
    pt= helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(25, 25))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)


    st.title("Top 10 athletes of " + selected_country)
    top10_df= helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)


if user_menu == 'Athlete wise Analysis':
        athlete_df = df.drop_duplicates(subset=['Name', 'region'])
        x1 = athlete_df['Age'].dropna()
        x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

        fig = ff.create_distplot([x1, x2, x3, x4],
                                 ['Overall Age', 'Gold Medalist', 'Silver medalist', 'Bronze Medalist'],
                                 show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.title("Distribution of Age")
        st.plotly_chart(fig)

        x = []
        name = []
        famous_sports = [
            "Athletics", "Swimming", "Gymnastics", "Football", "Basketball", "Tennis", "Cricket",
            "Boxing", "Wrestling", "Cycling", "Table Tennis", "Badminton", "Volleyball", "Rugby",
            "Baseball", "Ice Hockey", "Golf", "Skiing", "Fencing", "Archery", "Judo", "Taekwondo",
            "Weightlifting", "Canoeing", "Rowing", "Sailing", "Diving", "Handball", "Equestrian",
            "Skateboarding", "Surfing", "Karate", "Modern Pentathlon", "Triathlon", "Softball",
            "Hockey", "Artistic Swimming", "Trampoline", "BMX", "Mountain Biking", "Speed Skating",
            "Short Track", "Luge", "Skeleton", "Bobsleigh", "Snowboarding", "Nordic Combined",
            "Biathlon", "Curling", "Cross-Country Skiing"
        ]

        for sport in famous_sports:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            age_data = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
            if not age_data.empty:
                x.append(age_data)
                name.append(sport)

        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.title("Distribution of Age respect to Sports(Gold medalist)")
        st.plotly_chart(fig)

        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'overall')

        st.title("Height vs Weight")
        selected_sport = st.selectbox("Select Sport", sport_list)
        temp_df= helper.weight_v_height(df,selected_sport)
        fig, ax= plt.subplots()
        ax= sns.scatterplot(x=athlete_df['Weight'], y=athlete_df['Height'], hue=temp_df['Medal'],style=temp_df['Sex'],s=60)

        st.plotly_chart(fig)

        st.title("Men Vs Women participation over the year")
        final =  helper.men_vs_female(df)
        fig = px.line(final, x='Year', y=["Male", "Female"])
        st.plotly_chart(fig)



import pandas as pd
import matplotlib.pyplot as plt 
import io 
import requests 
import openpyxl
import streamlit as st 


header = st.beta_container()
user_input = st.beta_container()
output_graphs = st.beta_container()
author_credits = st.beta_container()

with header:
    st.title("Welcome to the Covid-19 County Tracker Application")
    st.markdown("""
    #### By: [Marco Cerrato](https://www.linkedin.com/in/marcocerratofontecha/)
    
    Welcome to the Covid-19 County tracker. This web application displays current information on the total number of Covid-19 cases reported in your selected county. With this application, you can get concise information on the number of total cases, deaths, and daily cases.

    **Note:** If you don't see the "User Selection" sidebar, please press the `>` icon on the top left side of your screen.
    
    """)

# Fetch Dataset from the New York Times Github Repository
url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2022.csv'
s = requests.get(url).content
df = pd.read_csv(io.StringIO(s.decode('utf-8')), parse_dates=True, index_col='date')

with user_input:
    st.sidebar.header('User Selection') 

    # Generating the list for states
    states_list = []
    counties_list = []

    states_list = df.state.unique()
    states_list.sort()


    state = st.sidebar.selectbox('Selecct Your State:',states_list) # We define the state variable

    # Generating the list of counties based on the state
    #state = input("Choose a state :")

    df_states = df[(df.state == state)].copy()
    counties_list = df_states.county.unique()
    conties_list = counties_list.sort()

    county = st.sidebar.selectbox('Select your County:',counties_list) # We define the county variable

    table_days = st.sidebar.slider('Select the number of days you want to be display in the Summary Table. ', min_value = 3, max_value= 15, value= 5, step=1)

    moving_average_day = st.sidebar.slider('How many days to consider for the moving average? ', min_value = 5, max_value = 14, value = 7, step=1)

    # Creating the dataframe for the county
    df_county = df[(df.county == county)& (df.state == state)].copy()

    #Create a new column with new cases
    df_county['new_cases'] = df_county.loc[:, 'cases'].diff()

    #Create a new column for 7-day moving average
    df_county['moving_average'] = df_county.loc[:,'new_cases'].rolling(window=moving_average_day).mean()

    #Create a 

with output_graphs:
    
    # Summary Table

    st.header(f'Summary Table for the last {table_days} days.')
    
    st.markdown(""" This table includes the number of cases, deaths, new cases and moving average for your selection.""")

    #st.write(df_county.iloc[-table_days:,-4:])

    a = df_county.iloc[-table_days:, -4:]
    
    my_table = st.table(a)


    # Total Cases Graph

    st.header(f'Total Cases for {county},{state}.')
    
    total_cases_chart = df_county['cases']

    
    st.line_chart(total_cases_chart)

    st.markdown("""**Note:** You can zoom on this graph if you are in front of a Desktop or Laptop by using your scrolling wheel on your mouse. You can also point on the line to get more information.""")

    # Moving Average Graph

    st.header(f'{moving_average_day} moving average for {county},{state}.')
    
    moving_average_chart = df_county['moving_average']
    
    st.line_chart(moving_average_chart)

    st.markdown("""**Note:** You can zoom on this graph if you are in front of a Desktop or Laptop by using your scrolling wheel on your mouse. You can also point on the line to get more information.""")

    # Death Graph

    st.header(f'Total Deaths for {county},{state}.')
    
    total_deaths_chart = df_county['deaths']
    
    st.line_chart(total_deaths_chart)

    st.markdown("""**Note:** You can zoom on this graph if you are in front of a Desktop or Laptop by using your scrolling wheel on your mouse. You can also point on the line to get more information.""")

with author_credits:
    st.header(f'Credits')
    st.markdown("""
    **Thank you for using my application!**
    
    The dataset used to feed this application is provided by [New York Times Covid-19 Github Repository](https://github.com/nytimes/covid-19-data).

    This application uses the Streamlit package library. You can learn more about me and my other projects by visiting my website [Not A Programmer] (https://notaprogrammer.com) or [my Github Repo] (https://github.com/cerratom).    
    """)



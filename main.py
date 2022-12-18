import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import base64

def add_bg_from_local(image):
    with open(image, "rb") as image:
        encoded_string = base64.b64encode(image.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )

add_bg_from_local('venv/image/streamlit_background.png')



c1, c2 = st.columns((1, 1))


with c2:
    st.title('Is your next exam coming? ')

    from PIL import Image

    image = Image.open('venv/image/clock.png')

    st.image(image, caption=None)

    st.subheader('Find out how long you need to study for your next exam. ')

    data = pd.read_csv('Data/Mydata .csv')
    data['STG'] = data['STG'] * 600
    data['PEG'] = data['PEG'] * 100

    y = data['STG'].values.reshape(-1, 1)
    X = data['PEG'].values.reshape(-1, 1)

    xmean = np.mean(X)
    ymean = np.mean(y)

    # Calculate the terms needed for the numator and denominator of beta
    data['xycov'] = (data['PEG'] - xmean) * (data['STG'] - ymean)
    data['xvar'] = (data['PEG'] - xmean) ** 2

    # Calculate beta and alpha
    beta = data['xycov'].sum() / data['xvar'].sum()
    alpha = ymean - (beta * xmean)
    print(f'alpha = {alpha}')
    print(f'beta = {beta}')

    wantScore = st.number_input('Enter the score you want to get:')

    if wantScore > 100:
        st.write('Please enter a score no more than 100.')

    st.write('You need to study at least: ')

c1, c2, c3, c4 = st.columns((1, 1, 1, 1))

with c3:
    if wantScore == 0:
        ypred = 0

    elif wantScore > 100:
        ypred = 0

    else:
        ypred = alpha + beta * wantScore
    st.title(round(ypred))



with c4:
    st.title('minutes*')

    if st.button('Convert to hours'):
        hours = ypred//60
        minutes= round(ypred) - (ypred//60)*60
        st.write(hours, 'hours and')
        st.write(minutes, 'minutes')



c1, c2 = st.columns((1, 1))

with c2:
    st.write("---")

    image = Image.open('venv/image/calendar.png')
    st.image(image, caption=None)



    st.subheader('Calculate how much time you need to study every day.')

    todayDate = st.date_input(
        "Today's date is: ")

    examDate = st.date_input(
        "The next exam is on: "
    )
    dateDifference = (examDate - todayDate).total_seconds() / 86400

    st.write("You have ",dateDifference, " days to study.")

    if dateDifference == 0:
        st.write("You need to study at least", round(ypred), "minutes every day.")
    else:
        st.write("You need to study at least ", ypred//dateDifference, " minutes every day.")


c1, c2, c3, c4 = st.columns((1, 1, 1, 1))

with c4:
    st.write('###')
    st.button('Send a reminder')




c1, c2 = st.columns((1, 1))

with c2:

    st.write('---')

    image = Image.open('venv/image/help.png')
    st.image(image, caption=None)


    st.subheader("Anything else we can help you?")

    st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #0099ff;
        color:#ffffff;
    }
    div.stButton > button:hover {
        background-color: #00ff00;
        color:#ff0000;
        }
    </style>""", unsafe_allow_html=True)


    if st.button('I need study tips.'):
       st.write('You can find some useful study tips here: ','https://www.uopeople.edu/blog/how-to-study-for-exams-strategies-and-tips/')


    if st.button('I need a tutor.'):
        st.write('You can find tutors who can help you with any subject here:', 'https://www.wyzant.com/')

    if st.button('I need help with my stress. '):
        st.write('You can learn how to release your stress here:', 'https://www.daniel-wong.com/2018/09/10/beat-exam-stress/')

    if st.button('I want to know how the time is predicted.'):

        st.write('We used a dataset provided by UCI (University of California Irvine). In this dataset, we only focus on 2 columns: STG and PEG.')
        st.write('STG represents values of study time in minutes from 0 to 600.')
        st.write('PEG represents values of scores from 0 to 100.')

        data = pd.read_csv('Data/Mydata .csv')
        data['STG'] = data['STG'] * 600
        data['PEG'] = data['PEG'] * 100
        st.write(data)

        st.write('In the scatterplot below, the correlation between the study time and exam score can be seen as weak positive, but the more time a person studies, a higher score he or she is likely to get.')

        fig = px.scatter(data, x='PEG', y='STG', hover_data=['PEG','STG'])
        st.plotly_chart(fig)

        st.write('In order to make predictions for the time to study, we have calculated the slope and y-intercept and found the line of best fit.')
        st.write('The equation of the line is:')
        st.subheader('y = 0.8x + 155.1')
        st.write('where y represents the exam score and x represents the time in minutes.')


    st.write('---')

    st.write('Made by Kyle C. Wang, NYU 2023')
    st.write('*This time is only a prediction. Please be adviced that we do not guarantee that you will get your desired score if you study for this amount of time. You could always decide on your own. Good luck!')














        



















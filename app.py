import streamlit as st
st.set_page_config(page_title="Airline Satisfaction Predictor", page_icon="✈️", layout="centered")

import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from catboost import Pool
from PIL import Image
from EDA import show_all 
from EDA import show_Dach

logo = Image.open("logo.png")


image = Image.open('photo2.jpg')
resized_image = image.resize((image.width, 200)) 
st.image(resized_image, use_container_width=True)

# lode data and model
df = pd.read_csv('train.csv')
model_dict = pickle.load(open('best_model_and_scaler.pkl', 'rb'))
model = model_dict['model']

st.sidebar.image(logo, width=170)
# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Data Exploration 📊", "Dashboard 📈","Predict Satisfaction"], index=0)

# Home
if page == "Home":
    st.title("Welcome to Our Airline Satisfaction Predictor ✈️")
    st.markdown("""
        This application helps you predict how satisfied customers are based on their travel details.

        **How to use:**
        - Use the sidebar to navigate between pages.
        - On the 'Data Exploration' page, you can view and explore the dataset.
        - On the 'Dashboard ' page,you can view simple Dashbord .
        - On the 'Predict Satisfaction' page, you can enter information and get predictions on customer satisfaction.

        Enjoy your experience! 😊
    """)

# Data Exploration
elif page == "Data Exploration 📊":
    st.title("Dataset Overview")
    st.write("Preview of the first 5 rows of the dataset:")
    st.dataframe(df.drop(columns=['Unnamed: 0', 'id']).head())
    show_all(df)
elif page=="Dashboard 📈":
    # st.title("Dashboard Overview ")
    show_Dach(df)

# predict
elif page == "Predict Satisfaction":
    st.title("Predict Customer Satisfaction")
    st.write("Please enter the traveler's information to predict their satisfaction level:")

    # Data entery
    Gender = st.selectbox('Gender', ['Male', 'Female'])
    Customer_Type = st.selectbox('Customer Type', ['Loyal Customer', 'disloyal Customer'])
    Age = st.slider('Age', 1, 85, 30)
    Type_of_Travel = st.selectbox('Type of Travel', ['Personal Travel', 'Business travel'])
    Class = st.selectbox('Class', ['Eco Plus', 'Business', 'Eco'])
    Flight_Distance = st.slider('Flight Distance', 50, 5000, 460)
    Inflight_wifi_service = st.selectbox('Inflight wifi service', list(range(6)))
    Departure_Arrival_time_convenient = st.selectbox('Departure/Arrival time convenient', list(range(6)))
    Ease_of_Online_booking = st.selectbox('Ease of Online booking', list(range(6)))
    Gate_location = st.selectbox('Gate location', list(range(6)))
    Food_and_drink = st.selectbox('Food and drink', list(range(6)))
    Online_boarding = st.selectbox('Online boarding', list(range(6)))
    Seat_comfort = st.selectbox('Seat comfort', list(range(6)))
    Inflight_entertainment = st.selectbox('Inflight entertainment', list(range(6)))
    On_board_service = st.selectbox('On-board service', list(range(6)))
    Leg_room_service = st.selectbox('Leg room service', list(range(6)))
    Baggage_handling = st.selectbox('Baggage handling', list(range(6)))
    Checkin_service = st.selectbox('Checkin service', list(range(6)))
    Inflight_service = st.selectbox('Inflight service', list(range(6)))
    Cleanliness = st.selectbox('Cleanliness', list(range(6)))
    Departure_Delay_in_Minutes = st.slider('Departure Delay in Minutes', 0, 1600, 500)
    Arrival_Delay_in_Minutes = st.slider('Arrival Delay in Minutes', 0, 1600, 500)

    # predict botton
    if st.button("Predict"):
        input_data = pd.DataFrame({
            'Gender': [Gender],
            'Customer Type': [Customer_Type],
            'Age': [Age],
            'Type of Travel': [Type_of_Travel],
            'Class': [Class],
            'Flight Distance': [Flight_Distance],
            'Inflight wifi service': [Inflight_wifi_service],
            'Departure/Arrival time convenient': [Departure_Arrival_time_convenient],
            'Ease of Online booking': [Ease_of_Online_booking],
            'Gate location': [Gate_location],
            'Food and drink': [Food_and_drink],
            'Online boarding': [Online_boarding],
            'Seat comfort': [Seat_comfort],
            'Inflight entertainment': [Inflight_entertainment],
            'On-board service': [On_board_service],
            'Leg room service': [Leg_room_service],
            'Baggage handling': [Baggage_handling],
            'Checkin service': [Checkin_service],
            'Inflight service': [Inflight_service],
            'Cleanliness': [Cleanliness],
            'Departure Delay in Minutes': [Departure_Delay_in_Minutes],
            'Arrival Delay in Minutes': [Arrival_Delay_in_Minutes]
        })

        # LabelEncoder
        encoders = {
            'Gender': LabelEncoder().fit(['Male', 'Female']),
            'Customer Type': LabelEncoder().fit(['Loyal Customer', 'disloyal Customer']),
            'Type of Travel': LabelEncoder().fit(['Personal Travel', 'Business travel']),
            'Class': LabelEncoder().fit(['Eco Plus', 'Business', 'Eco']),
        }

        for col in encoders:
            input_data[col] = encoders[col].transform(input_data[col])

        input_data = input_data.astype(float)
        input_pool = Pool(data=input_data)
        prediction = model.predict(input_pool)[0]

        # Prediction Result
        if prediction == 1:
            st.markdown(
                """
                <div style='
                    background-color: #e6ffed;
                    padding: 20px;
                    border-radius: 15px;
                    box-shadow: 4px 4px 12px rgba(0, 128, 0, 0.2);
                    text-align: center;
                    font-size: 22px;
                    font-weight: bold;
                    color: green;
                    margin-top: 20px;
                '>
                    ✅ Prediction Result: Satisfied
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style='
                    background-color: #ffe6e6;
                    padding: 20px;
                    border-radius: 15px;
                    box-shadow: 4px 4px 12px rgba(255, 0, 0, 0.2);
                    text-align: center;
                    font-size: 22px;
                    font-weight: bold;
                    color: red;
                    margin-top: 20px;
                '>
                    ❌ Prediction Result: Neutral or Dissatisfied
                </div>
                """,
                unsafe_allow_html=True
            )

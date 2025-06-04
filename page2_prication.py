import streamlit as st
import pandas as pd
import pickle

st.title("توقع رضا العملاء ✈️")

# تحميل الموديل
model = pickle.load(open(r'B:\Airline\best_model_and_scaler.pkl', 'rb'))

st.subheader("أدخل بيانات الرحلة للتوقع:")

gender = st.selectbox("الجنس", ["Male", "Female"])
age = st.slider("العمر", 1, 100, 30)
flight_distance = st.slider("مسافة الرحلة", 50, 5000, 1000)
wifi_service = st.slider("خدمة الواي فاي", 0, 5, 3)
seat_comfort = st.slider("راحة الكرسي", 0, 5, 3)

if st.button("توقع"):
    input_data = pd.DataFrame({
        'Gender': [gender],
        'Age': [age],
        'Flight Distance': [flight_distance],
        'Inflight wifi service': [wifi_service],
        'Seat comfort': [seat_comfort]
    })
    
    prediction = model.predict(input_data)[0]
    st.success(f"النتيجة: {prediction}")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# st.set_page_config(page_title="Airline Dashboard", page_icon="📊", layout="wide")

@st.cache_data

def load_data():
    return pd.read_csv("train.csv")

df = load_data()

def show_dashboard1(df):
    st.title("📊 Airline Customer Satisfaction Dashboard")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔹 Demographics", "🔹 Services Ratings", "🔹 Flight Info", "🔹 Satisfaction Analysis"])

    with tab1:
        st.subheader("Passenger Demographics")
        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.histogram(df, x='Age', nbins=30, color='Gender',
                                title="Age Distribution by Gender",
                                color_discrete_sequence=px.colors.sequential.Rainbow)
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = px.pie(df, names='Customer Type', title="Customer Type Distribution",
                         color_discrete_sequence=px.colors.sequential.Bluered_r)
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("Services Ratings Overview")
        service_cols = [
            'Inflight wifi service', 'Ease of Online booking', 'Food and drink',
            'Seat comfort', 'Inflight entertainment', 'On-board service',
            'Leg room service', 'Baggage handling', 'Checkin service',
            'Inflight service', 'Cleanliness']

        avg_services = df[service_cols].mean().sort_values()
        fig3 = px.bar(x=avg_services.index, y=avg_services.values,
                      title="Average Rating for Each Service",
                      labels={"x": "Service", "y": "Average Rating"},
                      color=avg_services.values,
                      color_continuous_scale='Turbo')
        fig3.update_traces(marker_line_color='black', marker_line_width=1.2)
        st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        st.subheader("Flight Details")
        col1, col2 = st.columns(2)

        with col1:
            fig4 = px.box(df, x='Type of Travel', y='Flight Distance',
                         color='Type of Travel',
                         title="Flight Distance by Travel Type",
                         color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig4, use_container_width=True)

        with col2:
            fig5 = px.scatter(df, x='Departure Delay in Minutes', y='Arrival Delay in Minutes',
                             color='satisfaction',
                             title="Delays vs Satisfaction",
                             color_discrete_sequence=px.colors.sequential.Viridis)
            st.plotly_chart(fig5, use_container_width=True)

    with tab4:
        st.subheader("Satisfaction Analysis")
        fig6 = px.histogram(df, x='satisfaction', color='Class', barmode='group',
                            title="Satisfaction by Class",
                            color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig6, use_container_width=True)

        st.markdown("### 🔥 Correlation Heatmap")
        corr = df.select_dtypes(include='number').corr()
        fig7 = px.imshow(corr, text_auto=True, title="Correlation Between Numeric Features",
                         color_continuous_scale='RdBu_r', aspect="auto")
        st.plotly_chart(fig7, use_container_width=True)

# Example usage if run directly

    show_dashboard1(df)

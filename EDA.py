import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import iplot

 
st.title("✈️ Data Visualization - Airline Passengers")
 
df = pd.read_csv(r'B:\Airline\train.csv')


def show_age_passengers(df):
    st.subheader("📊 Age Distribution of Passengers")
    passenger_counts = df['Age'].value_counts().sort_index()

    fig = go.Figure(data=[go.Scatter(x=passenger_counts.index, y=passenger_counts.values, mode='lines')])
    fig.update_layout(title='Distribution Age of Passengers', xaxis_title='Age', yaxis_title='Number of Passengers', width=900, height=600)
    st.plotly_chart(fig)

def show_gender(df):
    st.subheader("📊 Gender Frequency")

    gender_counts = df["Gender"].value_counts()
    fig = px.bar(
        gender_counts,
        x=gender_counts.index,
        y=(gender_counts / gender_counts.sum()) * 100,
        color=gender_counts.index,
        labels={"y": "Frequency (%)"},
        title="Gender Distribution (Percentage)",
        text=gender_counts.apply(lambda x: f'{(x / gender_counts.sum()) * 100:.1f}%'),
        template="plotly_dark",
        color_discrete_sequence=["DeepPink", "#66D3FA"]
    )
    fig.update_layout(width=900, height=600)
    fig.update_traces(textfont={"family": "consolas", "size": 20})
    st.plotly_chart(fig)

def show_gender_satisfaction(df):
    st.subheader("📊 Gender Distribution by Satisfaction")

    labels = df.groupby('satisfaction')['Gender'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=labels.index, values=labels.values)])
    fig.update_layout(title='Gender Distribution by Satisfaction', width=900, height=600)
    st.plotly_chart(fig)

def show_satisfaction_distribution(df):
    st.subheader("📊 Overall Satisfaction Distribution")

    fig = px.histogram(
        df, x='satisfaction', color='satisfaction', barmode='relative',
        color_discrete_map={'satisfied': 'lightblue', 'neutral or dissatisfied': 'teal'}
    )
    fig.update_layout(title='Distribution of Satisfied vs Dissatisfied', title_font={'size': 20}, width=900, height=600)
    fig.update_traces(marker_line_width=1, marker_line_color='black')
    st.plotly_chart(fig)

def show_customer_type_satisfaction(df):
    st.subheader("📊 Customer Type by Satisfaction")

    category = df.groupby('satisfaction')['Customer Type'].value_counts().reset_index()
    fig = px.bar(
        category, x='Customer Type', y='count', color='satisfaction',
        title="Customer Type Distribution by Satisfaction", text='count', template="plotly_dark"
    )
    fig.update_layout(width=900, height=600)
    fig.update_traces(textfont={"family": "consolas", "size": 18})
    st.plotly_chart(fig)

def show_travel_type_satisfaction(df):
    st.subheader("📊 Travel Type by Satisfaction")

    category = df.groupby('satisfaction')['Type of Travel'].value_counts().reset_index()
    fig = px.bar(
        category, x='Type of Travel', y='count', color='satisfaction',
        title="Type of Travel Distribution by Satisfaction", text='count', template="plotly_dark"
    )
    fig.update_layout(width=900, height=600)
    fig.update_traces(textfont={"family": "consolas", "size": 18})
    st.plotly_chart(fig)

def show_gander_with_class(df):
    st.subheader("📊Satisfied and dissatisfied passengers by Class")
    category = df.groupby('satisfaction')['Class'].value_counts().reset_index()
    fig = px.bar(
    category,
    x = 'Class',
    y = 'count',
    color='satisfaction',
    title="<b>Passenger Satisfaction by Flight Class<b>",

    text = 'count',
    template="plotly_dark")

    fig.update_layout(
        title='<b>Distribution of satisfied and dissatisfied passengers by Class<b>',
        title_font={'size': 20}
    )

    fig.update_layout(
        showlegend=True,
        width=900,
        height=600
                    )

    fig.update_traces(textfont= {"family": "consolas","size": 18})
    st.plotly_chart(fig)

def Flight_Distance_Departure_Delay(df):
    st.subheader('📊Relationship between Flight Distance,Departure Delay and Passenger Satisfaction')

    top_leagues = df['satisfaction'].value_counts().nlargest(3).index

    filtered_df = df[df['satisfaction'].isin(top_leagues)]

    fig = px.scatter(
        filtered_df,
        x='Flight Distance',
        y='Departure Delay in Minutes',
        size='Flight Distance',
        color='satisfaction',
        title='<b>Relationship between Flight Distance,Departure Delay in Minutes and Passenger Satisfaction<b>',
        labels={
            'Flight Distance': 'Flight Distance',
            'Departure Delay in Minutes': 'Departure Delay (Minutes)',
            'Class': 'Class',
        },
        template='plotly_white',
        width=950,
        height=600
    )

    st.plotly_chart(fig)


def Service_Ratings(df):
   
    st.subheader('📊 Service Ratings  ')
    service_cols = [
        'Inflight wifi service', 'Food and drink', 'Seat comfort',
        'Inflight entertainment', 'On-board service', 'Leg room service',
        'Cleanliness','Ease of Online booking','Gate location','Online boarding',
        'Baggage handling','Checkin service','Inflight service','Departure/Arrival time convenient'
    ]


    df[service_cols] = df[service_cols].apply(pd.to_numeric, errors='coerce')


    satisfied_avg = df[df['satisfaction'] == 'satisfied'][service_cols].mean()
    dissatisfied_avg = df[df['satisfaction'] != 'satisfied'][service_cols].mean()

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=satisfied_avg.tolist(),
        theta=service_cols,
        fill='toself',
        name='Satisfied',
        line_color='green'
    ))

    fig.add_trace(go.Scatterpolar(
        r=dissatisfied_avg.tolist(),
        theta=service_cols,
        fill='toself',
        name='Dissatisfied',
        line_color='red'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5])
        ),
        title='Service Ratings (Satisfied vs. Dissatisfied)',
        showlegend=True,
        width=900,
        height=600
    )

    st.plotly_chart(fig)



#-------------
#  Dashboard |
#-------------


def show_dashboard(df):

    st.markdown("<h2 style='color:#3366cc'>📊 Airline Analytics Dashboard</h2>", unsafe_allow_html=True)

    # --- KPIs ---
    total_passengers = len(df)
    avg_age = round(df["Age"].mean(), 1)
    avg_flight_distance = round(df["Flight Distance"].mean(), 1)
    satisfaction_rate = round((df['satisfaction'] == 'satisfied').mean() * 100, 1)
    avg_wifi = round(df['Inflight wifi service'].mean(), 1)
    avg_clean = round(df['Cleanliness'].mean(), 1)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Total Passengers", total_passengers)
    col2.metric("🎂 Avg Age", f"{avg_age} years")
    col3.metric("✈️ Avg Flight Distance", f"{avg_flight_distance} km")
    col4.metric("😊 Satisfaction Rate", f"{satisfaction_rate} %")

    col5, col6 = st.columns(2)
    col5.metric("📶 Avg Wifi Rating", avg_wifi)
    col6.metric("🧼 Avg Cleanliness", avg_clean)

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["👤 Demographics", "🛫 Services", "📈 Delays", "😊 Satisfaction"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Age Distribution")
            fig_age = px.histogram(df, x='Age', nbins=30, color_discrete_sequence=["#66b3ff"])
            st.plotly_chart(fig_age, use_container_width=True)

        with col2:
            st.subheader("Gender Distribution")
            fig_gender = px.pie(df, names='Gender', title='Passengers by Gender', color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_gender, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Class Breakdown")
            class_counts = df['Class'].value_counts().reset_index()
            class_counts.columns = ['Class', 'Count']
            fig_class = px.bar(class_counts, x='Class', y='Count', color='Class',
                               labels={'Class': 'Class', 'Count': 'Count'},
                               color_discrete_sequence=px.colors.qualitative.Safe)
            st.plotly_chart(fig_class, use_container_width=True)

        with col4:
            st.subheader("Customer Type Ratio")
            fig_cust = px.pie(df, names='Customer Type', title='Customer Type Distribution')
            st.plotly_chart(fig_cust, use_container_width=True)

    with tab2:
        st.subheader("Average Service Ratings")
        service_cols = [
            'Inflight wifi service', 'Ease of Online booking', 'Food and drink',
            'Seat comfort', 'Inflight entertainment', 'On-board service',
            'Leg room service', 'Baggage handling', 'Checkin service',
            'Inflight service', 'Cleanliness'
        ]
        avg_services = df[service_cols].mean().sort_values()
        fig_services = px.bar(
            x=avg_services.index, y=avg_services.values,
            labels={'x': 'Service', 'y': 'Average Rating'},
            title="Average Rating per Service",
            color=avg_services.values,
            color_continuous_scale='Bluered_r'
        )
        fig_services.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_services, use_container_width=True)

    with tab3:
        st.subheader("Delays vs Satisfaction")
        fig_delay = px.box(df, x='satisfaction', y='Departure Delay in Minutes', color='satisfaction',
                           color_discrete_sequence=['red', 'green'])
        st.plotly_chart(fig_delay, use_container_width=True)

        st.subheader("Arrival Delay vs Departure Delay")
        fig_scatter = px.scatter(df, x='Departure Delay in Minutes', y='Arrival Delay in Minutes',
                                 color='satisfaction', title="Delays Correlation",
                                 color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab4:
        st.subheader("Satisfaction by Type of Travel")
        fig_satisf = px.histogram(df, x='Type of Travel', color='satisfaction',
                                  barmode='group', color_discrete_sequence=px.colors.qualitative.G10)
        st.plotly_chart(fig_satisf, use_container_width=True)

        st.subheader("Satisfaction by Class")
        fig_satisf_class = px.histogram(df, x='Class', color='satisfaction', barmode='group')
        st.plotly_chart(fig_satisf_class, use_container_width=True)

        st.subheader("Correlation Heatmap")
        corr = df.select_dtypes(include='number').corr()
        fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r')
        st.plotly_chart(fig_corr, use_container_width=True)

# -----------------------------------
# 📦All Founcation
# -----------------------------------

def show_all(df):
    show_age_passengers(df)
    show_gender(df)
    show_gender_satisfaction(df)
    show_satisfaction_distribution(df)
    show_customer_type_satisfaction(df)
    show_travel_type_satisfaction(df)
    show_gander_with_class(df)
    Flight_Distance_Departure_Delay(df)
    Service_Ratings(df)
  


def show_Dach(df):
    show_dashboard(df)

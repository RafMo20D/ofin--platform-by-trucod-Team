import streamlit as st
import pandas as pd
import openai
import matplotlib.pyplot as plt
import plotly.express as px
from prophet import Prophet
from prophet.plot import plot_plotly
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import IsolationForest
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

openai.api_key = ''


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
nltk.download('vader_lexicon')

def forecast_financials(data):
    """Predict future financial metrics using Prophet."""
    
    date_column_name = 'Period'  
    value_column_name = 'Revenue' 

    if date_column_name not in data.columns or value_column_name not in data.columns:
        raise ValueError(f"Dataframe must include the columns '{date_column_name}' and '{value_column_name}'")

    df = data.rename(columns={date_column_name: 'ds', value_column_name: 'y'})

    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)
    fig = plot_plotly(model, forecast)
    return fig

def detect_anomalies(data):
    """Detect anomalies in financial data."""
    isolation_forest = IsolationForest(n_estimators=100)
    isolation_forest.fit(data[['Revenue']].values.reshape(-1, 1))
    anomalies = isolation_forest.predict(data[['Revenue']].values.reshape(-1, 1))
    data['anomaly'] = anomalies
    return data[data['anomaly'] == -1]  

def analyze_sentiment(text):
    """Analyze sentiment of financial texts."""
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    return sentiment_score

def plot_financial_data(data):
    """Visualize financial data using Plotly."""
    fig = px.line(data, x='Period', y='Revenue', title='Financial Data Over Time')
    st.plotly_chart(fig)


st.title('Ofin Financial Analysis Platform')

analysis_type = st.sidebar.selectbox("Select Analysis Type", ["Data Visualization", "Predictive Analytics", "Text Analysis", "Similarity Analysis", "Anomaly Detection", "Sentiment Analysis"])

if analysis_type == "Data Visualization":
    uploaded_file = st.file_uploader("Upload Financial Data", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        plot_financial_data(data)

elif analysis_type == "Predictive Analytics":
    uploaded_file = st.file_uploader("Upload Financial Data with Dates", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        fig = forecast_financials(data)
        st.plotly_chart(fig)

elif analysis_type == "Text Analysis":
    text_data = st.text_area("Paste your financial report text here:")
    if st.button('Analyze Text'):
        insights = analyze_text_data(text_data)
        st.write(insights)

elif analysis_type == "Similarity Analysis":
    report1 = st.text_area("Paste the first financial report text:")
    report2 = st.text_area("Paste the second financial report text:")
    if st.button('Compare Texts'):
        similarity_score = text_similarity_analysis(report1, report2)
        st.write(f"Similarity Score: {similarity_score}")

elif analysis_type == "Anomaly Detection":
    uploaded_file = st.file_uploader("Upload Financial Data for Anomaly Detection", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        anomalies = detect_anomalies(data)
        st.write("Detected Anomalies:", anomalies)

elif analysis_type == "Sentiment Analysis":
    text_data = st.text_area("Paste the financial text for sentiment analysis:")
    if st.button('Analyze Sentiment'):
        sentiment_score = analyze_sentiment(text_data)
        st.write(f"Sentiment Score: {sentiment_score}")


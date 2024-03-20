import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
import openai
import plotly.express as px

# Setup OpenAI key
openai.api_key = ''

def generate_financial_insights(financial_data):
    prompt = f"Generate financial insights based on the following data: {financial_data}"
    try:
        data = {
            "model": "gpt-3.5-turbo",  # Specify the chat model you're using
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }
        headers = {
            "Authorization": f"Bearer {openai.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            # Extracting the response from the last message in the chat
            last_message = response_data['choices'][0]['message']['content']
            return last_message.strip()
        else:
            return f"Error: Could not generate insights. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_identity_data(entity_id):
    url = "https://sandbox.leantech.me/data/v1/identity"
    headers = {
        "lean-app-token": "a7d91218-1312365--exmp",
        "Content-Type": "application/json"
    }
    payload = {"entity_id": entity_id}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: Could not fetch data. Status code: {response.status_code}"

def fetch_financial_data(entity_id):
    # This is a placeholder for fetching real financial data
    # In a real scenario, you would replace this with actual data fetching logic
    return {
        'market_value': 100000,
        'earnings': 5000,
        'revenue': [10000, 15000, 20000, 25000],
    }

def create_interactive_charts(financial_data):
    df = pd.DataFrame({
        'Quarter': pd.date_range(start='2021-01-01', periods=len(financial_data['revenue']), freq='Q'),
        'Revenue': financial_data['revenue']
    })
    fig = px.line(df, x='Quarter', y='Revenue', title='Revenue Over Time')
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


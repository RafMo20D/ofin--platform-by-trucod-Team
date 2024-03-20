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
        "lean-app-token": "a7d9121-8c40-41ae-56566-exmp",
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

def calculate_financial_ratios(financial_data):
    ratios = {
        'P/E Ratio': financial_data['market_value'] / financial_data['earnings'],
       
    }
    return ratios

def perform_horizontal_vertical_analysis(financial_data):
    df = pd.DataFrame({
        'Quarter': pd.date_range(start='2021-01-01', periods=len(financial_data['revenue']), freq='Q'),
        'Revenue': financial_data['revenue']
    })
  
    df['Revenue Growth'] = df['Revenue'].pct_change() * 100
    
    df['Revenue as % of Total Revenue'] = (df['Revenue'] / df['Revenue'].sum()) * 100
    return df

def main():
    st.title("Smart Financial Analysis Platform with Open Banking and AI Insights")
    entity_id = st.text_input("Entity ID", help="Enter the entity ID here")

    if st.button("Analyze Financial Data"):
        if not entity_id:
            st.error("Please enter a valid entity ID.")
        else:
            identity_data = get_identity_data(entity_id)
            if isinstance(identity_data, dict):
                financial_data = fetch_financial_data(entity_id)
                insights = generate_financial_insights(str(financial_data))
                
                st.subheader("Generated Financial Insights")
                st.write(insights)
                
                financial_ratios = calculate_financial_ratios(financial_data)
                st.subheader("Financial Ratios")
                st.json(financial_ratios)
                
                hv_analysis = perform_horizontal_vertical_analysis(financial_data)
                st.subheader("Horizontal and Vertical Analysis")
                st.dataframe(hv_analysis)
                
                st.subheader("Revenue Over Time")
                create_interactive_charts(financial_data)


if __name__ == "__main__":
    main()                

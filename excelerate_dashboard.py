import streamlit as st
import pandas as pd
import plotly.express as px

# Title and description
st.title("Excelerate Dashboard")
st.markdown("### A Comparative Trend Analysis Dashboard for Opportunities and User Data")

# Load the data from CSV
@st.cache_data
def load_data():
    try:
        opportunity_data = pd.read_csv('OpportunitiesData_Aligned.csv')
        user_data = pd.read_csv('UserData.csv')
        return opportunity_data, user_data
    except FileNotFoundError as e:
        st.error(f"File not found: {e}")
        return None, None

# Load the data
opportunity_data, user_data = load_data()

# Check if data loaded correctly
if opportunity_data is None or user_data is None:
    st.stop()

# Debug: Display column names to verify structure
st.write("### Debug Info: Column Names in Uploaded Files")
st.write("Opportunities Data Columns:", opportunity_data.columns.tolist())
st.write("User Data Columns:", user_data.columns.tolist())

# Data Preprocessing and Checks
if 'Stage' in opportunity_data.columns:
    stage_counts = opportunity_data['Stage'].value_counts().reset_index()
    stage_counts.columns = ['Stage', 'Count']
    
    # Plot Stage distribution
    fig_stage = px.bar(stage_counts, x='Stage', y='Count', title='Opportunity Stages')
    st.plotly_chart(fig_stage)
else:
    st.warning("No 'Stage' column found in Opportunities Data. Please check the file.")

if 'UserName' in user_data.columns:
    user_counts = user_data['UserName'].value_counts().reset_index()
    user_counts.columns = ['UserName', 'Count']
    
    # Plot User distribution
    fig_user = px.pie(user_counts, names='UserName', values='Count', title='User Distribution')
    st.plotly_chart(fig_user)
else:
    st.warning("No 'UserName' column found in User Data. Please check the file.")

# Comparative Trend Analysis
if 'Date' in opportunity_data.columns and 'CreatedDate' in user_data.columns:
    opportunity_data['Date'] = pd.to_datetime(opportunity_data['Date'])
    user_data['CreatedDate'] = pd.to_datetime(user_data['CreatedDate'])

    opportunity_trend = opportunity_data.groupby(opportunity_data['Date'].dt.to_period('M')).size()
    user_trend = user_data.groupby(user_data['CreatedDate'].dt.to_period('M')).size()

    trend_df = pd.DataFrame({
        'Month': opportunity_trend.index.astype(str),
        'Opportunities': opportunity_trend.values,
        'Users': user_trend.reindex(opportunity_trend.index, fill_value=0).values
    })

    # Plot comparative trends
    fig_trend = px.line(trend_df, x='Month', y=['Opportunities', 'Users'],
                        title='Comparative Trend Over Time')
    st.plotly_chart(fig_trend)
else:
    st.warning("Date columns missing in either Opportunities or User Data for trend analysis.")

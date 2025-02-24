import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the Streamlit page
st.set_page_config(page_title="Excelerate Dashboard", layout="wide")

# Load data from CSV files in the root directory
@st.cache_data
def load_data():
    try:
        opportunity_data = pd.read_csv('OpportunityWiseData_Aligned.csv')
        user_data = pd.read_csv('UserData_Aligned.csv')
        return opportunity_data, user_data
    except FileNotFoundError as e:
        st.error(f"File not found: {e}")
        return None, None

# Load actual data
opportunity_data, user_data = load_data()

# Check if the data loaded successfully
if opportunity_data is not None and user_data is not None:
    # Dashboard Title
    st.title("📊 Excelerate Dashboard")

    # Opportunity Stage Distribution
    if 'Stage' in opportunity_data.columns:
        st.subheader("🚀 Opportunity Stage Distribution")
        stage_counts = opportunity_data['Stage'].value_counts().reset_index()
        stage_counts.columns = ['Stage', 'Count']

        fig_stage = px.bar(
            stage_counts, 
            x='Stage', 
            y='Count', 
            color='Stage',
            title="Distribution of Opportunity Stages",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_stage, use_container_width=True)
    else:
        st.warning("⚠️ No 'Stage' column found in Opportunity Data.")

    # Top Performing Users
    if 'UserName' in user_data.columns and 'Opportunities' in user_data.columns:
        st.subheader("🏆 Top Performing Users")
        top_users = user_data.sort_values(by='Opportunities', ascending=False).head(10)

        fig_users = px.bar(
            top_users, 
            x='UserName', 
            y='Opportunities', 
            color='UserName',
            title="Top 10 Users by Opportunities",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig_users, use_container_width=True)
    else:
        st.warning("⚠️ 'UserName' or 'Opportunities' column missing in User Data.")

    # Filters for deeper analysis
    if 'Stage' in opportunity_data.columns:
        st.subheader("🔍 Filter Opportunities by Stage")
        selected_stage = st.selectbox("Select a stage to filter:", opportunity_data['Stage'].unique())
        filtered_data = opportunity_data[opportunity_data['Stage'] == selected_stage]
        st.dataframe(filtered_data)
else:
    st.error("❌ Failed to load data. Please check if the CSV files are in the root directory.")

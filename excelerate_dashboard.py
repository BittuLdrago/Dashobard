import streamlit as st
import pandas as pd
import plotly.express as px

# Set the title of the dashboard
st.set_page_config(page_title="Excelerate Dashboard", layout="wide")
st.title("📊 Excelerate Dashboard")

# Load the data
@st.cache_data
def load_data():
    try:
        opportunity_data = pd.read_csv('OpportunityWiseData_Aligned.csv')
        user_data = pd.read_csv('UserData_Aligned.csv')
        return opportunity_data, user_data
    except FileNotFoundError as e:
        st.error(f"❌ File not found: {e}")
        return None, None

# Load CSV files from the root directory
opportunity_data, user_data = load_data()

# Check if the data loaded successfully
if opportunity_data is not None and user_data is not None:
    # Basic data preview
    st.subheader("📄 Data Overview")
    st.write("### Opportunities Data Sample")
    st.dataframe(opportunity_data.head())

    st.write("### User Data Sample")
    st.dataframe(user_data.head())

    # Check if required columns exist
    if 'Stage' in opportunity_data.columns and 'UserName' in user_data.columns:
        # Stage-wise Opportunity Count
        st.subheader("📈 Opportunity Stage Distribution")
        stage_counts = opportunity_data['Stage'].value_counts().reset_index()
        stage_counts.columns = ['Stage', 'Count']
        fig_stage = px.bar(stage_counts, x='Stage', y='Count', color='Stage', title="Opportunities by Stage")
        st.plotly_chart(fig_stage, use_container_width=True)

        # User-wise Opportunity Count
        st.subheader("👤 User Opportunity Distribution")
        user_counts = opportunity_data['UserName'].value_counts().reset_index()
        user_counts.columns = ['UserName', 'Count']
        fig_user = px.bar(user_counts, x='UserName', y='Count', color='UserName', title="Opportunities by User")
        st.plotly_chart(fig_user, use_container_width=True)

        # Monthly Trend Analysis
        st.subheader("📅 Monthly Opportunity Trends")
        if 'CreatedDate' in opportunity_data.columns:
            opportunity_data['CreatedDate'] = pd.to_datetime(opportunity_data['CreatedDate'])
            opportunity_data['Month'] = opportunity_data['CreatedDate'].dt.to_period('M').astype(str)
            monthly_trend = opportunity_data.groupby('Month').size().reset_index(name='Count')
            fig_monthly = px.line(monthly_trend, x='Month', y='Count', title='Monthly Opportunity Creation Trend')
            st.plotly_chart(fig_monthly, use_container_width=True)
        else:
            st.warning("⚠️ 'CreatedDate' column not found in Opportunity Data.")
    else:
        st.error("❌ Required columns ('Stage' in Opportunities or 'UserName' in User Data) not found.")
else:
    st.warning("📥 Please upload your data files manually.")
    uploaded_opportunity = st.file_uploader("Upload OpportunityWiseData_Aligned.csv", type=['csv'])
    uploaded_user = st.file_uploader("Upload UserData_Aligned.csv", type=['csv'])

    if uploaded_opportunity is not None and uploaded_user is not None:
        opportunity_data = pd.read_csv(uploaded_opportunity)
        user_data = pd.read_csv(uploaded_user)
        st.success("✅ Files uploaded successfully. Please rerun the app.")

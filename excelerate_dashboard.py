import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the Dashboard
st.title("Excelerate Dashboard")

# File uploader for CSV files
opportunity_file = st.file_uploader("Upload Opportunities Data CSV", type="csv")
user_file = st.file_uploader("Upload User Data CSV", type="csv")

# Load data if both files are uploaded
if opportunity_file is not None and user_file is not None:
    # Read uploaded CSV files
    opportunity_data = pd.read_csv(opportunity_file)
    user_data = pd.read_csv(user_file)

    st.success("Files uploaded successfully!")

    # Display uploaded data
    st.subheader("Opportunities Data")
    st.dataframe(opportunity_data)

    st.subheader("User Data")
    st.dataframe(user_data)

    # Visualization - Opportunities by Stage
    if 'Stage' in opportunity_data.columns:
        st.subheader("Opportunities by Stage")
        fig = px.bar(opportunity_data, x='Stage', title="Opportunities by Stage")
        st.plotly_chart(fig)
    else:
        st.error("No 'Stage' column found in Opportunities Data.")

    # Visualization - User Analysis (Example)
    if 'UserName' in user_data.columns:
        st.subheader("User Participation")
        user_counts = user_data['UserName'].value_counts().reset_index()
        user_counts.columns = ['UserName', 'Count']
        fig = px.pie(user_counts, names='UserName', values='Count', title="User Participation Breakdown")
        st.plotly_chart(fig)
    else:
        st.error("No 'UserName' column found in User Data.")
else:
    st.warning("Please upload both CSV files to proceed.")

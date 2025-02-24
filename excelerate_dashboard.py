import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Set up the Streamlit app
st.set_page_config(page_title="Excelerate Dashboard", layout="wide")
st.title("Excelerate Dashboard")

# Load the datasets
@st.cache_data
def load_data():
    opportunity_data = pd.read_csv('data/OpportunitiesData_Aligned.csv')
    user_data = pd.read_csv('data/UserData_Aligned.csv')
    return opportunity_data, user_data

opportunity_data, user_data = load_data()

# Convert 'Profile Id' columns to the same data type (string)
opportunity_data['Profile Id'] = opportunity_data['Profile Id'].astype(str)
user_data['Profile Id'] = user_data['Profile Id'].astype(str)

# Merge datasets on 'Profile Id'
merged_data = pd.merge(opportunity_data, user_data, on='Profile Id', how='inner')

# Sidebar filters
st.sidebar.header("Filter the data")
selected_country = st.sidebar.multiselect(
    "Select Country:",
    options=merged_data['Country'].unique(),
    default=merged_data['Country'].unique()
)

selected_program_type = st.sidebar.multiselect(
    "Select Program Type:",
    options=merged_data['Program Type'].unique(),
    default=merged_data['Program Type'].unique()
)

# Apply filters
filtered_data = merged_data[
    (merged_data['Country'].isin(selected_country)) &
    (merged_data['Program Type'].isin(selected_program_type))
]

# Display summary statistics
st.subheader("Summary Statistics")
st.write(filtered_data.describe())

# Visualizations
st.subheader("Opportunities by Country")
opportunity_country = filtered_data['Country'].value_counts().reset_index()
opportunity_country.columns = ['Country', 'Count']
fig_country = px.bar(opportunity_country, x='Country', y='Count', title='Opportunities by Country')
st.plotly_chart(fig_country, use_container_width=True)

st.subheader("Program Types Distribution")
program_type_count = filtered_data['Program Type'].value_counts().reset_index()
program_type_count.columns = ['Program Type', 'Count']
fig_program = px.pie(program_type_count, names='Program Type', values='Count', title='Program Types Distribution')
st.plotly_chart(fig_program, use_container_width=True)

# Display filtered data table
st.subheader("Filtered Data")
st.dataframe(filtered_data)

# Export filtered data
st.subheader("Download Filtered Data")
csv = filtered_data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download as CSV",
    data=csv,
    file_name='filtered_data.csv',
    mime='text/csv',
)

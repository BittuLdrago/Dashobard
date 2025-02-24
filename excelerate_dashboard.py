import streamlit as st
import pandas as pd

# Load the cleaned datasets
opportunity_data = pd.read_csv("OpportunityWiseData_Aligned.csv")
user_data = pd.read_csv("UserData_Aligned.csv")

# Ensure 'Profile Id' exists in both datasets and has the same data type
opportunity_data.rename(columns=lambda x: x.strip(), inplace=True)
user_data.rename(columns=lambda x: x.strip(), inplace=True)

if 'Profile Id' in opportunity_data.columns and 'Profile Id' in user_data.columns:
    opportunity_data['Profile Id'] = opportunity_data['Profile Id'].astype(str)
    user_data['Profile Id'] = user_data['Profile Id'].astype(str)

    # Merge datasets on 'Profile Id'
    merged_data = pd.merge(opportunity_data, user_data, on='Profile Id', how='left')
else:
    st.error("The 'Profile Id' column is missing from one of the files. Please check your CSV files.")

# Display the dashboard title
st.title("Excelerate Platform Dashboard")

# Example Metrics
total_users = merged_data['Profile Id'].nunique()
signed_up_opportunities = merged_data[merged_data['Status Description'] == 'Signed Up'].shape[0]

st.metric("Total Users Signed Up", total_users)
st.metric("Opportunities Signed Up", signed_up_opportunities)

# Top 10 countries by signups
st.subheader("Top 10 Countries by Signups")
top_countries = merged_data['Country'].value_counts().head(10)
st.bar_chart(top_countries)

# US Cities signups
st.subheader("US Cities Signups")
us_cities = merged_data[merged_data['Country'] == 'United States']['City'].value_counts().head(10)
st.bar_chart(us_cities)

# Most popular opportunity signed up for
st.subheader("Most Popular Opportunity Signed Up For")
popular_opportunity = merged_data['Opportunity Name'].value_counts().idxmax()
st.write(f"**{popular_opportunity}**")

# Run the Streamlit app
st.success("Dashboard is running successfully!")


import streamlit as st
import pandas as pd

# Load data
opportunity_data = pd.read_csv('OpportunityWiseData_Aligned.csv')
user_data = pd.read_csv('UserData_Aligned.csv')

# Merge datasets on Profile Id
merged_data = pd.merge(opportunity_data, user_data, on='Profile Id', how='left')

# Title and Overview
st.title("Excelerate Platform Analytics Dashboard")
st.markdown("### Key Metrics Overview")

# Total Signups vs. Opportunities
total_signups = merged_data['Profile Id'].nunique()
opportunity_signups = merged_data[~merged_data['Opportunity Id'].isna()]['Profile Id'].nunique()

col1, col2 = st.columns(2)
col1.metric("Total Signups", total_signups)
col2.metric("Signed up for Opportunities", opportunity_signups)

# Top 10 Countries
st.markdown("### Top 10 Countries with Most Learners")
top_countries = merged_data['Country'].value_counts().head(10)
st.bar_chart(top_countries)

# US Cities Analysis
st.markdown("### US Cities with Signups")
us_cities = merged_data[merged_data['Country'] == 'United States']['City'].value_counts().head(10)
st.bar_chart(us_cities)

# Popular Opportunities
st.markdown("### Most Popular Opportunities")
popular_opps = merged_data['Opportunity Name'].value_counts().head(5)
st.bar_chart(popular_opps)

# Completed Opportunities
completed_opps = merged_data[merged_data['Status Description'] == 'Completed']['Opportunity Name'].value_counts().head(5)
st.markdown("### Most Completed Opportunities")
st.bar_chart(completed_opps)

# Demographics
st.markdown("### Demographics")
gender_distribution = merged_data['Gender'].value_counts()
st.pie_chart(gender_distribution)

student_status = merged_data['Current Student Status'].value_counts()
st.bar_chart(student_status)

# Most Gained Skills
st.markdown("### Most Gained Skills")
skills = merged_data.groupby('Opportunity Name')['Skill Points Earned'].sum().sort_values(ascending=False).head(10)
st.bar_chart(skills)

# Total Scholarship Awards
st.markdown("### Scholarships Awarded by Opportunity")
scholarships = merged_data.groupby('Opportunity Name')['Reward Amount'].sum().sort_values(ascending=False).head(10)
st.bar_chart(scholarships)

# Filters
st.sidebar.title("Filters")
country_filter = st.sidebar.multiselect("Filter by Country", merged_data['Country'].unique())
gender_filter = st.sidebar.multiselect("Filter by Gender", merged_data['Gender'].unique())

# Apply filters
filtered_data = merged_data
if country_filter:
    filtered_data = filtered_data[filtered_data['Country'].isin(country_filter)]
if gender_filter:
    filtered_data = filtered_data[filtered_data['Gender'].isin(gender_filter)]

st.dataframe(filtered_data.head(50))

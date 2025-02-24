import streamlit as st import pandas as pd import plotly.express as px

Load Data

def load_data(): opportunity_data = pd.read_csv('OpportunityWiseData_Aligned.csv') user_data = pd.read_csv('UserData_Aligned.csv') return opportunity_data, user_data

Load datasets

opportunity_data, user_data = load_data()

Title

st.title('Excelerate Dashboard')

Opportunity Stage-wise Distribution

if 'Stage' in opportunity_data.columns: st.subheader('Opportunity Stage-wise Distribution') stage_count = opportunity_data['Stage'].value_counts().reset_index() stage_count.columns = ['Stage', 'Count'] fig_stage = px.bar(stage_count, x='Stage', y='Count', color='Stage', title='Distribution of Opportunities by Stage') st.plotly_chart(fig_stage) else: st.warning("No 'Stage' column found in Opportunity Data.")

Top Users by Opportunities Created

if 'UserName' in user_data.columns: st.subheader('Top Users by Opportunities Created') user_opps = user_data['UserName'].value_counts().reset_index() user_opps.columns = ['UserName', 'Opportunities'] fig_users = px.bar(user_opps.head(10), x='UserName', y='Opportunities', color='Opportunities', title='Top 10 Users by Opportunities Created') st.plotly_chart(fig_users) else: st.warning("No 'UserName' column found in User Data.")

Opportunity Amount Analysis

if 'Amount' in opportunity_data.columns: st.subheader('Opportunity Amount Analysis') amount_by_stage = opportunity_data.groupby('Stage')['Amount'].sum().reset_index() fig_amount = px.pie(amount_by_stage, names='Stage', values='Amount', title='Total Opportunity Amount by Stage') st.plotly_chart(fig_amount) else: st.warning("No 'Amount' column found in Opportunity Data.")

Data Preview

st.subheader('Raw Data Preview') if st.checkbox('Show Opportunity Data'): st.dataframe(opportunity_data)

if st.checkbox('Show User Data'): st.dataframe(user_data)


import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the data
data = pd.read_csv('survey_lung_cancer.csv')

# Pre-process data
age_bins = [30, 40, 50, 60, 70, 80, 90]
data['Age Group'] = pd.cut(data['AGE'], bins=age_bins, labels=['31-40', '41-50', '51-60', '61-70', '71-80', '81-90'])
data['SMOKING'] = data['SMOKING'].map({1: 'Non-Smoker', 2: 'Smoker'})
data['Symptom Count'] = data.iloc[:, 3:14].apply(lambda x: x.eq(2).sum(), axis=1)

# Group the data by 'Symptom Count', 'SMOKING', and 'GENDER' and calculate the count of people
grouped_df = data.groupby(['Symptom Count', 'SMOKING', 'GENDER']).size().reset_index(name='Number of People')

############### plot 1 

st.subheader('Number of Symptoms by Count of Patients')

# Filter by gender for the graph
gender_filter = st.selectbox("Filter by Gender", ['All', 'M', 'F'])

# Create the Plotly figure for plot 1
fig1 = go.Figure()

for smoking_type in grouped_df['SMOKING'].unique():
    temp_df = grouped_df[grouped_df['SMOKING'] == smoking_type]
    
    if gender_filter != 'All':
        temp_df = temp_df[temp_df['GENDER'] == gender_filter]

    fig1.add_trace(go.Bar(
        x=temp_df['Symptom Count'],
        y=temp_df['Number of People'],
        name=smoking_type
    ))

# Update the layout for plot 1
fig1.update_layout(
    xaxis_title='Number of Symptoms',
    yaxis_title='Count of Patients',
    barmode='group'
)

############### plot 2

# Create the Plotly figure for plot 2
fig2 = go.Figure()

df = data.groupby(['Age Group', 'SMOKING']).size().reset_index(name='Number of Cases')

for smoking_type in df['SMOKING'].unique():
    temp_df = df[df['SMOKING'] == smoking_type]
    
    fig2.add_trace(go.Scatter(
        x=temp_df['Age Group'],
        y=temp_df['Number of Cases'],
        mode='lines+markers',
        name=smoking_type
    ))

# Update the layout for plot 2
fig2.update_layout(
    title='Count of Lung Cancer Cases by Age Group and Smoking Status',
    xaxis_title='Age Group',
    yaxis_title='Number of Cases',
    legend=dict(title='Smoking Status')
)

# Display the plots using Streamlit
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1)

with col2:
    st.plotly_chart(fig2)

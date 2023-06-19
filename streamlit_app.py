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

# Create the Plotly figure
fig = go.Figure()

# Filter by gender for the graph
gender_filter = st.selectbox("Filter by Gender", ['All', 'M', 'F'])

for smoking_type in grouped_df['SMOKING'].unique():
    temp_df = grouped_df[grouped_df['SMOKING'] == smoking_type]
    
    if gender_filter != 'All':
        temp_df = temp_df[temp_df['GENDER'] == gender_filter]

    fig.add_trace(go.Bar(
        x=temp_df['Symptom Count'],
        y=temp_df['Number of People'],
        name=smoking_type
    ))

# Update the layout
fig.update_layout(
    xaxis_title='Number of Symptoms',
    yaxis_title='Count of Patients',
    barmode='group'
)

# Display the plot using Streamlit
st.plotly_chart(fig)


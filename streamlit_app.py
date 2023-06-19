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

# Filter options
smoking_filter = st.sidebar.selectbox("Filter by Smoking", ['All', 'Smoker', 'Non-Smoker'])
gender_filter = st.selectbox("Filter by Gender", ['All', 'M', 'F'])

# Apply filters
filtered_df = data.copy()
if smoking_filter != 'All':
    filtered_df = filtered_df[filtered_df['SMOKING'] == smoking_filter]
if gender_filter != 'All':
    filtered_df = filtered_df[filtered_df['GENDER'] == gender_filter]

# Group the filtered data and calculate the count of people
grouped_df = filtered_df.groupby(['Symptom Count', 'SMOKING'], as_index=False)['Number of People'].sum()

# Create the Plotly figure
fig = go.Figure()

for smoking_type in grouped_df['SMOKING'].unique():
    temp_df = grouped_df[grouped_df['SMOKING'] == smoking_type]
    
    fig.add_trace(go.Bar(
        x=temp_df['Symptom Count'],
        y=temp_df['Number of People'],
        name=smoking_type
    ))

# Update the layout
fig.update_layout(
    title='Sign Violators Count by Symptom Count',
    xaxis_title='Number of Symptoms',
    yaxis_title='Count of People',
    barmode='group'
)

# Display the plot using Streamlit
st.plotly_chart(fig)

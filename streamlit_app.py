import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go

# Load the data
data = pd.read_csv('survey_lung_cancer.csv')

# Pre - proccess 
age_bins = [30, 40, 50, 60, 70, 80, 90]

data['Age Group'] = pd.cut(data['AGE'], bins=age_bins, labels=['31-40', '41-50', '51-60', '61-70', '71-80', '81-90'])
data['SMOKING'] = data['SMOKING'].map({1: 'Non-Smoker', 2: 'Smoker'})

graph_data = data.groupby(['Age Group', 'SMOKING']).size().reset_index(name='Number of Cases')

symptom_columns = ['YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC DISEASE', 'FATIGUE ',
                   'ALLERGY ', 'WHEEZING', 'COUGHING', 'SHORTNESS OF BREATH', 'SWALLOWING DIFFICULTY',
                   'CHEST PAIN']

data['Symptom Count'] = data[symptom_columns].apply(lambda x: x.eq(2).sum(), axis=1)

df = data.groupby(['Symptom Count', 'SMOKING','GENDER']).size().reset_index(name='Number of People')

# Filter the data based on user selection
smoking_filter = st.sidebar.selectbox("Filter by Smoking", ['All', 'Smoker', 'Non-Smoker'])
gender_filter = None

# Group the filtered data by 'Symptom Count' and 'SMOKING' and calculate the count of people
grouped_df = df.groupby(['Symptom Count', 'SMOKING'], as_index=False)['Number of People'].sum()

# Filter the data based on user selection
if smoking_filter != 'All':
    grouped_df = grouped_df[grouped_df['SMOKING'] == smoking_filter]
    # Get the gender options for the filtered data
    gender_options = df[df['SMOKING'] == smoking_filter]['GENDER'].unique()
    # User input - Gender filter
    gender_filter = st.sidebar.selectbox("Filter by Gender", ['All'] + list(gender_options), index=0)

    if gender_filter != 'All':
        grouped_df = grouped_df[grouped_df['GENDER'] == gender_filter]

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

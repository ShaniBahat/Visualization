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
gender_filter = st.sidebar.selectbox("Filter by Gender", ['All', 'M', 'F'])

filtered_df = df.copy()

if smoking_filter != 'All':
    filtered_df = filtered_df[filtered_df['SMOKING'] == smoking_filter]

if gender_filter != 'All':
    filtered_df = filtered_df[filtered_df['GENDER'] == gender_filter]

# Group the filtered data by 'Symptom Count' and 'SMOKING' and calculate the count of people
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



# Create the Plotly figure
fig = go.Figure()

df = data.groupby(['Age Group', 'SMOKING']).size().reset_index(name='Number of Cases')

for smoking_type in df['SMOKING'].unique():
    temp_df = df[df['SMOKING'] == smoking_type]
    
    fig.add_trace(go.Scatter(
        x=temp_df['Age Group'],
        y=temp_df['Number of Cases'],
        mode='lines+markers',
        name=smoking_type
    ))

# Update the layout
fig.update_layout(
    title='Count of Lung Cancer Cases by Age Group and Smoking Status',
    xaxis_title='Age Group',
    yaxis_title='Number of Cases',
    legend=dict(title='Smoking Status')
)

# Display the plot using Streamlit
st.plotly_chart(fig)







with st.container():
    # Filter the data based on the user selection
    filtered_df = df[df['GENDER'] == gender_filter]
    
    # Group the filtered data by 'Symptom Count' and 'SMOKING' and calculate the count of people
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

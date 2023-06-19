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

# Set x-axis tick labels for every number
fig.update_xaxes(type='category')

# Display the plot using Streamlit
st.plotly_chart(fig)


########## Plot 2
st.subheader('Lung Cancer Cases by Age Group')

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
    xaxis_title='Age Group',
    yaxis_title='Number of Cases',
    legend=dict(title='Smoking Status')
)

# Display the plot using Streamlit
st.plotly_chart(fig)

####### plot 3 
# Load the data
data_new = pd.read_csv('survey_lung_cancer.csv')
data_new['SMOKING'] = data_new['SMOKING'].map({1: 'Non-Smoker', 2: 'Smoker'})

# Pre-process data
symptoms = ['YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC DISEASE', 'FATIGUE ',
            'ALLERGY ', 'WHEEZING', 'COUGHING', 'SHORTNESS OF BREATH', 'SWALLOWING DIFFICULTY',
            'CHEST PAIN']

# Filter the data based on selected symptoms
selected_symptoms = st.multiselect('Select Symptoms', symptoms)

# Count the occurrences of selected symptoms in each row
data_new['symptom_count'] = data_new[selected_symptoms].sum(axis=1)

# Filter the data to include only rows with a symptom count of 2
filtered_data = data_new[data_new['symptom_count'] == len(selected_symptoms)*2]

# Separate data for smokers and non-smokers
smokers_data = filtered_data[filtered_data['SMOKING'] == 'Smoker']
non_smokers_data = filtered_data[filtered_data['SMOKING'] == 'Non-Smoker']

# Calculate the count of cancer and non-cancer cases for smokers
smoker_cancer_count = smokers_data[smokers_data['LUNG_CANCER'] == 'YES'].shape[0]
smoker_non_cancer_count = smokers_data[smokers_data['LUNG_CANCER'] == 'NO'].shape[0]

# Calculate the count of cancer and non-cancer cases for non-smokers
non_smoker_cancer_count = non_smokers_data[non_smokers_data['LUNG_CANCER'] == 'YES'].shape[0]
non_smoker_non_cancer_count = non_smokers_data[non_smokers_data['LUNG_CANCER'] == 'NO'].shape[0]

# Create the Plotly figures
fig1 = go.Figure(data=[go.Pie(labels=['Cancer', 'Non-Cancer'],
                              values=[smoker_cancer_count, smoker_non_cancer_count],
                              title='Smokers')])

fig2 = go.Figure(data=[go.Pie(labels=['Cancer', 'Non-Cancer'],
                              values=[non_smoker_cancer_count, non_smoker_non_cancer_count],
                              title='Non-Smokers')])

# Update the layout for both figures
fig1.update_layout(title='Division of Cancer and Non-Cancer Cases - Smokers')
fig2.update_layout(title='Division of Cancer and Non-Cancer Cases - Non-Smokers')

# Display the pie charts side by side using Streamlit
col1, col2 = st.beta_columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)

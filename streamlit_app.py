import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.image("picture for app.png")


# Load the data
data_new = pd.read_csv('survey_lung_cancer.csv')
data_new['SMOKING'] = data_new['SMOKING'].map({1: 'Non-Smoker', 2: 'Smoker'})

# Pre-process data
symptoms = ['YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC DISEASE', 'FATIGUE ',
            'ALLERGY ', 'WHEEZING', 'COUGHING', 'SHORTNESS OF BREATH', 'SWALLOWING DIFFICULTY',
            'CHEST PAIN']

st.subheader("Cancer Cases for Smokers and Non-Smokers")

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
                              title='Smokers',
                              hole=0.5)])
fig1.update_traces(marker=dict(line=dict(color='#000000', width=2)))

fig2 = go.Figure(data=[go.Pie(labels=['Cancer', 'Non-Cancer'],
                              values=[non_smoker_cancer_count, non_smoker_non_cancer_count],
                              title='Non-Smokers',
                              hole=0.5)])

fig2.update_traces(marker=dict(line=dict(color='#000000', width=2)))

# Update the layout for both figures
# fig1.update_layout(title='Division of Cancer and Non-Cancer Cases - Smokers')
# fig2.update_layout(title='Division of Cancer and Non-Cancer Cases - Non-Smokers')

# Display the pie charts side by side using Streamlit
col1, col2 = st.columns(2)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)
#####################################################
# Load the data
data = pd.read_csv('survey_lung_cancer.csv')

# Pre-process data
age_bins = [30,35, 40,45, 50,55, 60,65, 70,75, 80,85, 90]
data['Age Group'] = pd.cut(data['AGE'], bins=age_bins, labels=['31-35','36-40', '41-45','56-50', '51-55', '56-60', '61-65','66-70', '71-75','76-80','81-85', '86-90'])
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
data = pd.read_csv('survey_lung_cancer.csv')
data['SMOKING'] = data['SMOKING'].map({1: 'Non-Smoker', 2: 'Smoker'})

# Group the data by age group and smoking status
df = data.groupby(['Age Group', 'SMOKING']).size().reset_index(name='Number of Cases')

# Create the Plotly figure
fig = go.Figure()

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

# Add user selection
selected_age = st.slider('Select Age', min_value=data['AGE'].min(), max_value=data['AGE'].max(), step=1)
selected_smoking = st.radio('Select Smoking Status', ['Smoker', 'Non-Smoker'])

# Add a point on the plot for the selected age and smoking status
if selected_smoking == 'Smoker':
    marker_color = 'red'
else:
    marker_color = 'blue'

fig.add_trace(go.Scatter(
    x=[selected_age],
    y=[df[(df['Age Group'] == str(selected_age)) & (df['SMOKING'] == selected_smoking)]['Number of Cases']],
    mode='markers',
    marker=dict(color=marker_color, size=10),
    name=f'Selected ({selected_smoking})'
))

# Update the layout again to include the selected point
fig.update_layout(
    xaxis_title='Age Group',
    yaxis_title='Number of Cases',
    legend=dict(title='Smoking Status'),
    title='Lung Cancer Cases by Age Group (with Selection)'
)

# Display the updated plot with the selected point
st.plotly_chart(fig)

######### plot 4 

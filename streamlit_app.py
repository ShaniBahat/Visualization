import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.image("title for app.png")

########## Plot 1
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

# Update the colors for the pie charts
fig1.update_traces(marker=dict(colors=['#c6cccc', '#baddde']))
fig2.update_traces(marker=dict(colors=['#c6cccc', '#baddde']))

# Display the pie charts side by side using Streamlit
col1, col2 = st.columns(2)
col1.plotly_chart(fig1, use_container_width=True)
col2.plotly_chart(fig2, use_container_width=True)

#####################################################

###### Plot 2 

data = pd.read_csv('survey_lung_cancer.csv')

# Pre-process data
age_bins = [30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
data['Age Group'] = pd.cut(data['AGE'], bins=age_bins, labels=['31-35', '36-40', '41-45', '56-50', '51-55', '56-60', '61-65', '66-70', '71-75', '76-80', '81-85', '86-90'])
data['SMOKING'] = data['SMOKING'].map({1: 'Non-Smoker', 2: 'Smoker'})
data['Symptom Count'] = data.iloc[:, 3:14].apply(lambda x: x.eq(2).sum(), axis=1)

# Group the data by 'Symptom Count', 'SMOKING', and 'GENDER' and calculate the count of people
grouped_df = data.groupby(['Symptom Count', 'SMOKING', 'GENDER']).size().reset_index(name='Number of People')

st.subheader('Lung Cancer Cases by Age Group')

# Create the Plotly figure
fig = go.Figure()

df = data.groupby(['Age Group', 'SMOKING']).size().reset_index(name='Number of Cases')

colors = {'Non-Smoker': '#b3baba', 'Smoker': '#008f94'}

for smoking_type in df['SMOKING'].unique():
    temp_df = df[df['SMOKING'] == smoking_type]
    
    fig.add_trace(go.Scatter(
        x=temp_df['Age Group'],
        y=temp_df['Number of Cases'],
        mode='lines+markers',
        name=smoking_type,
        opacity=0.8,
        line=dict(width=5, color=colors[smoking_type]),
        marker=dict(color=colors[smoking_type])
    ))

# Update the layout
fig.update_layout(
    xaxis_title='Age Group',
    yaxis_title='Number of Cases',
    legend=dict(title='Smoking Status')
)

# Add selection options for age and smoking status
selected_age_group = st.selectbox('Select Age Group', df['Age Group'].unique())
selected_smoking_status = st.selectbox('Select Smoking Status', df['SMOKING'].unique())

# Filter the data based on selected age group and smoking status
filtered_df = df[(df['Age Group'] == selected_age_group) & (df['SMOKING'] == selected_smoking_status)]

# Get the corresponding x and y values for the selected age group and smoking status
x_value = filtered_df['Age Group'].values[0]
y_value = filtered_df['Number of Cases'].values[0]

# Update the layout to add a point for the selected data
fig.add_trace(go.Scatter(
    x=[x_value],
    y=[y_value],
    mode='markers',
    name='Your Selection',
    marker=dict(symbol='star-diamond-open-dot', color='black', size=14, line=dict(width=3))
))

st.plotly_chart(fig)

####### plot 3 
st.subheader('Number of Symptoms by Count of Patients')

# Create the Plotly figure
fig = go.Figure()

# Filter by gender for the graph
gender_filter = st.selectbox("Filter by Gender", ['All', 'M', 'F'])

colors = {'Non-Smoker': '#b3baba', 'Smoker': '#008f94'}

for smoking_type in grouped_df['SMOKING'].unique():
    temp_df = grouped_df[grouped_df['SMOKING'] == smoking_type]
    
    if gender_filter != 'All':
        temp_df = temp_df[temp_df['GENDER'] == gender_filter]

    fig.add_trace(go.Bar(
        x=temp_df['Symptom Count'],
        y=temp_df['Number of People'],
        name=smoking_type, opacity=0.8,
        marker=dict(color=colors[smoking_type])
    ))



# Update the layout
fig.update_layout(
    xaxis_title='Number of Symptoms',
    yaxis_title='Count of Patients',
    barmode='group',
    bargap=0.2,
    bargroupgap=0.1 
)

# Set x-axis tick labels for every number
fig.update_xaxes(type='category')

# Display the plot using Streamlit
st.plotly_chart(fig)

######### plot 4 


import plotly.express as px

# Load the data
data = pd.read_csv('survey_lung_cancer.csv')

# Filter the data to include only rows where the symptom appears (value equals 2)
symptom_counts = data.iloc[:, 2:14].eq(2).sum()

# Calculate the count of lung cancer cases
lung_cancer_counts = data[data['LUNG_CANCER'] == 'YES'].iloc[:, 2:14].eq(2).sum()

# Generate a unique numeric value for each symptom
symptom_color_mapping = {symptom: index for index, symptom in enumerate(symptom_counts.index)}

# Create a DataFrame for the bubble chart
bubble_data = pd.DataFrame({
    'Symptom': symptom_counts.index,
    'Occurrences': symptom_counts.values,
    'Cancer Cases': lung_cancer_counts.values
})

# Create the Bubble Chart
fig = px.scatter(
    bubble_data,
    x='Symptom',
    y='Occurrences',
    size='Cancer Cases'*1.5,
    color='Symptom',
    hover_data=['Symptom', 'Occurrences', 'Cancer Cases'],
    labels={'Occurrences': 'Number of Occurrences', 'Cancer Cases': 'Number of Cancer Cases'}
)

# Customize the layout
fig.update_layout(
    xaxis=dict(
        tickangle=45,
        tickfont=dict(size=10),
        title='Symptom'
    ),
    yaxis=dict(
        title='Number of Occurrences',
        range=[0, 250]
    ),
    legend_title='Symptom',
    hovermode='closest'
)

# Display the chart using Streamlit
st.plotly_chart(fig)


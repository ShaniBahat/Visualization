import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go


# Load the data
data = pd.read_csv('survey_lung_cancer.csv')

age_bins = [30, 40, 50, 60, 70, 80, 90]

data['Age Group'] = pd.cut(data['AGE'], bins=age_bins, labels=['31-40', '41-50', '51-60', '61-70', '71-80', '81-90'])
data['SMOKING'] = data['SMOKING'].map({1: 'Non-Smoker', 2: 'Smoker'})

graph_data = data.groupby(['Age Group', 'SMOKING']).size().reset_index(name='Number of Cases')


st.title('Lung Cancer Cases')
show_smoker = st.checkbox('Smoker', value=True)
show_non_smoker = st.checkbox('Non-Smoker', value=True)

color_scale = alt.Scale(domain=['Smoker', 'Non-Smoker'], range=['#678282', '#23D1D1'])

chart = alt.Chart(graph_data).mark_circle().encode(
    x='Age Group',
    y='Number of Cases',
    color=alt.Color('SMOKING:N', scale=color_scale),
    tooltip=['Age Group', 'Number of Cases'],
    opacity=alt.condition(
        alt.datum['SMOKING'] == 'Smoker',
        alt.value(1) if show_smoker else alt.value(0),
        alt.value(1) if show_non_smoker else alt.value(0)
    )).interactive()

trend_line_smoker = alt.Chart(graph_data[graph_data['SMOKING'] == 'Smoker']).mark_line(color='#678282').encode(
    x='Age Group',
    y='Number of Cases',
    opacity=alt.value(1) if show_smoker else alt.value(0)
).transform_window(
    rolling_mean='mean(Number of Cases)',
    frame=[-2, 2]
).mark_line(color='#678282')

trend_line_non_smoker = alt.Chart(graph_data[graph_data['SMOKING'] == 'Non-Smoker']).mark_line(color='#23D1D1').encode(
    x='Age Group',
    y='Number of Cases',
    opacity=alt.value(1) if show_non_smoker else alt.value(0)
).transform_window(
    rolling_mean='mean(Number of Cases)',
    frame=[-2, 2]
).mark_line(color='#23D1D1')

combined_chart = chart + trend_line_smoker + trend_line_non_smoker

# Display the graph
st.altair_chart(combined_chart, use_container_width=True)

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

# Group the filtered data by 'Symptom Count' and 'SMOKING' and calculate the count
grouped_df = filtered_df.groupby(['Symptom Count', 'SMOKING']).count()['Number of People'].reset_index()

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

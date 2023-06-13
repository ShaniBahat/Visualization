import streamlit as st
import pandas as pd
import altair as alt

# Load the data
data = pd.read_csv('survey_lung_cancer.csv')

# Check if the 'Age' column exists
if 'AGE' not in data.columns:
    st.error("The 'Age' column is not present in the dataset.")
else:
    # Define the age bins
    age_bins = [30, 40, 50, 60, 70, 80, 90]

    # Create a new column to categorize ages into bins
    data['Age Group'] = pd.cut(data['AGE'], bins=age_bins, labels=['31-40', '41-50', '51-60', '61-70', '71-80', '81-90'])

    # Map smoking values to appropriate labels
    data['SMOKING'] = data['SMOKING'].map({1: 'Non-Smoker', 2: 'Smoker'})

    # Prepare the data for the graph
    graph_data = data.groupby(['Age Group', 'SMOKING']).size().reset_index(name='Number of Cases')

    # Create the interactive graph
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
        )
    ).interactive()

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



    


data = pd.read_csv('survey lung cancer.csv')

# Check if the symptom columns exist
symptom_columns = ['YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC DISEASE', 'FATIGUE ',
                   'ALLERGY ', 'WHEEZING', 'COUGHING', 'SHORTNESS OF BREATH', 'SWALLOWING DIFFICULTY',
                   'CHEST PAIN']
missing_symptoms = [col for col in symptom_columns if col not in data.columns]

data[symptom_columns] = data[symptom_columns].replace(symptom_labels)

# Calculate the symptom count for each patient
data['Symptom Count'] = data[symptom_columns].apply(lambda x: x.eq(2).sum(), axis=1)
data['SMOKING'] = data['SMOKING'].map({1: 'Non-Smoker', 2: 'Smoker'})

# Prepare the data for the graph
graph_data = data.groupby(['Symptom Count', 'SMOKING']).size().reset_index(name='Number of People')

# Create the interactive graph
st.title('Distribution of Symptom Counts by Smoking Status')
show_smoker = st.checkbox('Show Smoker', value=True)
show_non_smoker = st.checkbox('Show Non-Smoker', value=True)

color_scale = alt.Scale(domain=['Smoker', 'Non-Smoker'], range=['#678282', '#23D1D1'])

chart = alt.Chart(graph_data).mark_bar().encode(
x='Symptom Count:Q',
y='Number of People:Q',
color=alt.Color('SMOKING:N', scale=color_scale),
tooltip=['Symptom Count', 'Number of People'],
opacity=alt.condition(
    alt.datum['SMOKING'] == 'Smoker',
    alt.value(1) if show_smoker else alt.value(0),
    alt.value(1) if show_non_smoker else alt.value(0)
)
).interactive()

    # Display the graph
    st.altair_chart(chart, use_container_width=True)

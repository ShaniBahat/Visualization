import pandas as pd
import streamlit as st
import altair as alt

# Load the data into a pandas DataFrame
df = pd.read_csv('/content/survey_lung_cancer.csv')

# Filter data for lung cancer cases
filtered_data = df[df['LUNG_CANCER'] == 'YES']

# Replace the smoking labels
filtered_data['SMOKING'] = filtered_data['SMOKING'].replace({2: 'Smoking', 1: 'Non-smoking'})

# Create age groups
age_bins = [30, 40, 50, 60, 70, 80, 90]
age_labels = ['31-40', '41-50', '51-60', '61-70', '71-80', '81-90']
filtered_data['AGE_GROUP'] = pd.cut(filtered_data['AGE'], bins=age_bins, labels=age_labels)

# Group the filtered data by age group and smoking status and calculate the count of lung cancer cases
grouped_data = filtered_data.groupby(['AGE_GROUP', 'SMOKING']).size().unstack().fillna(0)

# Create a new Streamlit app
st.title('Count of Lung Cancer Cases by Age Group and Smoking Status')

# Convert the DataFrame to an Altair chart
chart = alt.Chart(grouped_data.reset_index()).mark_line().encode(
    x='AGE_GROUP',
    y='Non-smoking',
    color=alt.value('#267868'),
    tooltip=['AGE_GROUP', 'Non-smoking']
).properties(
    title='Count of Lung Cancer Cases by Age Group and Smoking Status',
    width=600,
    height=400
)

# Display the chart in Streamlit
st.altair_chart(chart)

# Display the DataFrame if desired
st.write(grouped_data)

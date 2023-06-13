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

    # Prepare the data for the graph
    graph_data = data.groupby(['Age Group', 'SMOKING']).size().reset_index(name='Number of Cases')

    # Create the interactive graph
    st.title('Lung Cancer Cases')
    show_both = st.checkbox('Show Smoker and Non-Smoker')

    if show_both:
        chart = alt.Chart(graph_data).mark_circle().encode(
            x='Age Group',
            y='Number of Cases',
            color='SMOKING:N',
            tooltip=['Age Group', 'Number of Cases']
        ).interactive()
    else:
        smoker_or_non_smoker = st.radio('Select Smoker or Non-Smoker:', ['Smoker', 'Non-Smoker'])
        filtered_data = graph_data[graph_data['SMOKING'] == smoker_or_non_smoker]

        chart = alt.Chart(filtered_data).mark_circle().encode(
            x='Age Group',
            y='Number of Cases',
            tooltip=['Age Group', 'Number of Cases']
        ).interactive()

    # Add trend lines
    trend_line = alt.Chart(graph_data).mark_line().encode(
        x='Age Group',
        y='Number of Cases',
        color='SMOKING:N'
    )

    # Combine the chart and trend line
    combined_chart = chart + trend_line

    # Display the graph
    st.altair_chart(combined_chart, use_container_width=True)

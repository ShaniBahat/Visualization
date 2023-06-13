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

    # Filter the data for smoker and non-smoker
    smoker_data = data[data['SMOKING'] == 2]
    non_smoker_data = data[data['SMOKING'] == 1]

    # Count the number of cases for each age group and smoker category
    smoker_counts = smoker_data['Age Group'].value_counts().sort_index()
    non_smoker_counts = non_smoker_data['Age Group'].value_counts().sort_index()

    # Create the interactive graph
    st.title('Lung Cancer Cases')
    show_smoker = st.checkbox('Show Smoker', value=True)
    show_non_smoker = st.checkbox('Show Non-Smoker', value=True)

    if show_smoker and show_non_smoker:
        counts = smoker_counts + non_smoker_counts
    elif show_smoker:
        counts = smoker_counts
    elif show_non_smoker:
        counts = non_smoker_counts
    else:
        counts = pd.Series()

    # Prepare the data for the graph
    graph_data = pd.DataFrame({'Age Group': counts.index, 'Number of Cases': counts.values})

    # Create the graph using Altair
    chart = alt.Chart(graph_data).mark_circle().encode(
        x='Age Group',
        y='Number of Cases',
        tooltip=['Age Group', 'Number of Cases']
    ).interactive()

    # Add trend lines
    trend_data = pd.DataFrame({'x': range(len(counts)), 'y': counts.values})
    trend_line = alt.Chart(trend_data).mark_line().encode(
        x='x',
        y='y',
        opacity=alt.condition(
            alt.datum.y > 0,
            alt.value(1.0),
            alt.value(0.0)
        )
    )

    # Combine the chart and trend line
    combined_chart = chart + trend_line

    # Display the graph
    st.altair_chart(combined_chart, use_container_width=True)

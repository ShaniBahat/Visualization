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
    show_smoker = st.checkbox('Show Smoker Trend Line', value=True)
    show_non_smoker = st.checkbox('Show Non-Smoker Trend Line', value=True)

    chart = alt.Chart(graph_data).mark_circle().encode(
        x='Age Group',
        y='Number of Cases',
        color='SMOKING:N',
        tooltip=['Age Group', 'Number of Cases']
    ).interactive()

    trend_line_smoker = alt.Chart(graph_data[graph_data['SMOKING'] == 'Smoker']).mark_line(color='red').encode(
        x='Age Group',
        y='Number of Cases',
    ).transform_filter(
        alt.FieldOneOfPredicate(field='SMOKING', oneOf=['Smoker'])
    ).transform_window(
        rolling_mean='mean(Number of Cases)',
        frame=[-2, 2]
    ).mark_line(color='red')

    trend_line_non_smoker = alt.Chart(graph_data[graph_data['SMOKING'] == 'Non-Smoker']).mark_line(color='blue').encode(
        x='Age Group',
        y='Number of Cases',
    ).transform_filter(
        alt.FieldOneOfPredicate(field='SMOKING', oneOf=['Non-Smoker'])
    ).transform_window(
        rolling_mean='mean(Number of Cases)',
        frame=[-2, 2]
    ).mark_line(color='blue')

    combined_chart = chart + \
        alt.Chart(graph_data).transform_filter(
            alt.FieldOneOfPredicate(field='SMOKING', oneOf=['Smoker'])
        ).mark_line(opacity=int(show_smoker)).encode(
            x='Age Group',
            y='Number of Cases',
            color='SMOKING:N'
        ) + \
        alt.Chart(graph_data).transform_filter(
            alt.FieldOneOfPredicate(field='SMOKING', oneOf=['Non-Smoker'])
        ).mark_line(opacity=int(show_non_smoker)).encode(
            x='Age Group',
            y='Number of Cases',
            color='SMOKING:N'
        )

    # Display the graph
    st.altair_chart(combined_chart, use_container_width=True)

import pandas as pd
import streamlit as st
import altair as alt

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv('lung_cancer_data.csv')

# Define the age bins
age_bins = [30, 40, 50, 60, 70, 80, 90]

# Create a new column to categorize ages into bins
data['Age Group'] = pd.cut(data['Age'], bins=age_bins, labels=['31-40', '41-50', '51-60', '61-70', '71-80', '81-90'])

# Filter the data for smoker and non-smoker
smoker_data = data[data['Smoker'] == 'Yes']
non_smoker_data = data[data['Smoker'] == 'No']

# Count the number of cases for each age group and smoker category
smoker_counts = smoker_data['Age Group'].value_counts().sort_index()
non_smoker_counts = non_smoker_data['Age Group'].value_counts().sort_index()

# Create the interactive graph
st.title('Lung Cancer Cases')
smoker_or_non_smoker = st.radio('Select Smoker or Non-Smoker:', ['Smoker', 'Non-Smoker'])

if smoker_or_non_smoker == 'Smoker':
    counts = smoker_counts
else:
    counts = non_smoker_counts

# Plot the graph
fig, ax = plt.subplots()
ax.plot(counts.index, counts.values, marker='o')
ax.set_xlabel('Age Group')
ax.set_ylabel('Number of Cases')

# Add trend lines
z = np.polyfit(range(len(counts)), counts.values, 1)
p = np.poly1d(z)
ax.plot(counts.index, p(range(len(counts))), 'r--')

# Customize the plot
plt.xticks(rotation=45)
ax.set_title(f'Lung Cancer Cases ({smoker_or_non_smoker})')
st.pyplot(fig)

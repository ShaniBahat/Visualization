import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Plot the line chart
plt.plot(age_labels, grouped_data['Non-smoking'], marker='.', color='#267868', ms=10, label='Non-smoking')
plt.plot(age_labels, grouped_data['Smoking'], marker='.', color='#68C4AD', ms=10, label='Smoking')

plt.legend(title='Smoking Status', loc='upper right')
plt.xlabel('Age Group')
plt.ylabel('Count')

# Convert the Matplotlib figure to an image
fig_image = plt.gcf().canvas.tostring_rgb()
plt.close()

# Display the image in Streamlit
st.image(fig_image, format='png')

# Display the DataFrame if desired
st.write(grouped_data)

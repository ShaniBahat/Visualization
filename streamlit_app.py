# Load the data
data = pd.read_csv('survey_lung_cancer.csv')

# Define the symptom columns and their corresponding values
symptom_columns = ['YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC DISEASE', 'FATIGUE ', 'ALLERGY ', 'WHEEZING',
                   'COUGHING', 'SHORTNESS OF BREATH', 'SWALLOWING DIFFICULTY', 'CHEST PAIN']

symptom_values = {
    'YELLOW_FINGERS': {1: 'No', 2: 'Yes'},
    'ANXIETY': {1: 'No', 2: 'Yes'},
    'PEER_PRESSURE': {1: 'No', 2: 'Yes'},
    'CHRONIC DISEASE': {1: 'No', 2: 'Yes'},
    'FATIGUE ': {1: 'No', 2: 'Yes'},
    'ALLERGY ': {1: 'No', 2: 'Yes'},
    'WHEEZING': {1: 'No', 2: 'Yes'},
    'COUGHING': {1: 'No', 2: 'Yes'},
    'SHORTNESS OF BREATH': {1: 'No', 2: 'Yes'},
    'SWALLOWING DIFFICULTY': {1: 'No', 2: 'Yes'},
    'CHEST PAIN': {1: 'No', 2: 'Yes'}
}

# Calculate the number of symptoms for each patient
data['Num Symptoms'] = data[symptom_columns].apply(lambda x: x.value_counts().get(2, 0), axis=1)

# Prepare the data for the graph
graph_data = data.groupby(['Num Symptoms', 'SMOKING']).size().reset_index(name='Count')

# Create the interactive graph
st.title('Distribution of Symptom Counts by Smoking Status')

color_scale = alt.Scale(domain=['Non-Smoker', 'Smoker'], range=['#23D1D1', '#678282'])

chart = alt.Chart(graph_data).mark_bar().encode(
    x=alt.X('Num Symptoms:Q', title='Number of Symptoms'),
    y=alt.Y('Count:Q', title='Count'),
    color=alt.Color('SMOKING:N', scale=color_scale)
).properties(
    width=600,
    height=400
)

# Display the graph
st.altair_chart(chart, use_container_width=True)

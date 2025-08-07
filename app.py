from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('medicine.csv')

# Prepare symptom list
all_symptoms = set()
for symptoms in df['symptoms']:
    all_symptoms.update([s.strip().lower() for s in symptoms.split(',')])
symptom_list = sorted(all_symptoms)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    matched_diseases = []
    if request.method == 'POST':
        input_symptoms = [s.strip().lower() for s in request.form['symptoms'].split(',')]
        
        for _, row in df.iterrows():
            disease_symptoms = [s.strip().lower() for s in row['symptoms'].split(',')]
            if any(symptom in disease_symptoms for symptom in input_symptoms):
                matched_diseases.append({
                    'disease': row['disease'],
                    'symptoms': row['symptoms'],
                    'medicine': row['medicines'],
                    'category': row['category'],
                    'notes': row['notes']
                })

        if not matched_diseases:
            result = 'No matching disease found.'
    
    return render_template('index.html', results=matched_diseases, result=result, symptoms=symptom_list)

if __name__ == '__main__':
    app.run(debug=True)

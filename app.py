from flask import Flask, request, jsonify, render_template
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pandas as pd
import joblib

app = Flask(__name__)

# Function to load and preprocess the data
def load_data(file):
    df = pd.read_csv(file)
    if 'country_destination' not in df.columns:
        return None, 'Target column not found in the uploaded CSV file'
    y_train = df['country_destination']
    X_train = df.drop(columns=['country_destination'])
    return X_train, y_train

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def train_model():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return 'No file uploaded'
    
    file = request.files['file']
    
    # Check if the file is a CSV file
    if file.filename == '':
        return 'No file selected'
    
    if file and file.filename.endswith('.csv'):
        X_train, y_train = load_data(file)
        if X_train is None:
            return y_train
        
        # Train the model
        rf_model = RandomForestClassifier(n_estimators=100, random_state=100)
        rf_model.fit(X_train, y_train)
        
        # Save the trained model
        joblib.dump(rf_model, 'random_forest_model.pkl')
        
        # Redirect to the test page
        return render_template('test.html')
    
    else:
        return 'Invalid file format'

@app.route('/test', methods=['POST'])
def test_model():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return 'No file uploaded'
    
    file = request.files['file']
    
    # Check if the file is a CSV file
    if file.filename == '':
        return 'No file selected'
    
    if file and file.filename.endswith('.csv'):
        X_test, y_test = load_data(file)
        if X_test is None:
            return y_test
        
        # Load the trained model
        rf_model = joblib.load('random_forest_model.pkl')
        
        # Predict using the loaded model
        y_pred = rf_model.predict(X_test)
        
        # Generate and return classification report
        report = classification_report(y_test, y_pred)
        return report
    
    else:
        return 'Invalid file format'

if __name__ == '__main__':
    app.run(debug=True)

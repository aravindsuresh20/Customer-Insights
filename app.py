from flask import Flask, request, render_template, send_file
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import os

app = Flask(__name__)

# Load and preprocess the dataset
df = pd.read_csv('Comprehensive_Banking_Database.csv')
df = df.dropna(subset=['Loan Status'])
df['Gender'] = df['Gender'].astype('category').cat.codes
df['Loan Status'] = df['Loan Status'].astype('category').cat.codes

feature_columns = ['Age', 'Gender', 'Account Balance', 'Transaction Amount', 'Loan Amount', 'Interest Rate', 'Loan Term']
X = df[feature_columns]
y = df['Loan Status']

# Train and save the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

with open('loan_approval_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Perform backend-only EDA
def perform_backend_eda():
    numeric_df = df.select_dtypes(include=['number'])
    summary_stats = numeric_df.describe()
    missing_values = numeric_df.isnull().sum()
    correlation_matrix = numeric_df.corr()

    with open('eda_summary.txt', 'w') as f:
        f.write("Summary Statistics:\n")
        f.write(summary_stats.to_string())
        f.write("\n\nMissing Values:\n")
        f.write(missing_values.to_string())
        f.write("\n\nCorrelation Matrix:\n")
        f.write(correlation_matrix.to_string())

perform_backend_eda()

# Load the trained model
with open('loan_approval_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()
    input_data = pd.DataFrame([data])
    input_data['Age'] = input_data['Age'].astype(int)
    input_data['Gender'] = input_data['Gender'].astype('category').cat.codes
    input_data['Account Balance'] = input_data['Account Balance'].astype(float)
    input_data['Transaction Amount'] = input_data['Transaction Amount'].astype(float)
    input_data['Loan Amount'] = input_data['Loan Amount'].astype(float)
    input_data['Interest Rate'] = input_data['Interest Rate'].astype(float)
    input_data['Loan Term'] = input_data['Loan Term'].astype(int)

    prediction = model.predict(input_data[feature_columns])[0]
    loan_status = {0: 'Approved', 1: 'Closed', 2: 'Rejected'}
    result = loan_status.get(prediction, 'Unknown')

    return render_template('results.html', prediction=result)

@app.route('/download_result')
def download_result():
    result_text = request.args.get('result', 'No result provided')
    file_path = os.path.join('downloads', 'loan_result.txt')
    os.makedirs('downloads', exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(f"Loan Prediction Result: {result_text}")
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

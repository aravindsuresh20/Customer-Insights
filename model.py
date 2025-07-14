import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load the dataset
df = pd.read_csv('Comprehensive_Banking_Database.csv')

# Drop rows with missing target values
df = df.dropna(subset=['Loan Status'])

# Define feature columns and target column
feature_columns = ['Age', 'Gender', 'Account Balance', 'Transaction Amount', 'Loan Amount', 'Interest Rate', 'Loan Term']
target_column = 'Loan Status'

# Encode categorical variables
df['Gender'] = df['Gender'].astype('category').cat.codes
df[target_column] = df[target_column].astype('category').cat.codes

# Split the data
X = df[feature_columns]
y = df[target_column]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print(classification_report(y_test, y_pred, target_names=['Approved', 'Closed', 'Rejected']))

# Save the model
with open('loan_approval_model.pkl', 'wb') as f:
    pickle.dump(model, f)

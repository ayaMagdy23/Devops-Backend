import os
import time
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import psycopg2
from urllib.parse import urlparse

MODEL_DIR = "global_model"
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

def label_scaling(row):
    if row['cpu_usage'] > 85 or row['memory_usage'] > 90:
        return "scale_up"
    elif row['cpu_usage'] < 30 and row['memory_usage'] < 40:
        return "scale_down"
    else:
        return "no_scaling"

def train_model(df):
    df['scaling_action'] = df.apply(label_scaling, axis=1)
    le = LabelEncoder()
    df['scaling_action_encoded'] = le.fit_transform(df['scaling_action'])

    X = df[['cpu_usage', 'memory_usage', 'disk_usage', 'network_usage']]
    y = df['scaling_action_encoded']
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    joblib.dump((model, le), MODEL_PATH)
    print("[INFO] Global model trained and saved.")

def predict_action(row):
    if not os.path.exists(MODEL_PATH):
        return label_scaling(row)

    model, le = joblib.load(MODEL_PATH)
    X_input = np.array([[row['cpu_usage'], row['memory_usage'], row['disk_usage'], row['network_usage']]])
    encoded = model.predict(X_input)[0]
    return le.inverse_transform([encoded])[0]

def process_data(df):
    df['scaling_action'] = df.apply(predict_action, axis=1)
    return df

# PostgreSQL connection string
db_url = "postgresql://postgres:G7vK93aZpT2wL1xB@devops-proj.chmswo02gtgh.eu-west-2.rds.amazonaws.com:5432/postgres?sslmode=require"
url = urlparse(db_url)

# Continuous loop
while True:
    try:
        connection = psycopg2.connect(
            host=url.hostname,
            port=url.port,
            user=url.username,
            password=url.password,
            dbname=url.path[1:],
            sslmode='require'
        )
        cursor = connection.cursor()

        # Fetch all monitoring data
        cursor.execute("SELECT * FROM myapps_monitoringdata")
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)

        # Train the model if it doesn't exist
        if not os.path.exists(MODEL_PATH):
            train_model(df)

        # Predict and 
        #print
        df = process_data(df)
        print(df[['id', 'cpu_usage', 'memory_usage', 'scaling_action']].to_string(index=False))

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    time.sleep(10)
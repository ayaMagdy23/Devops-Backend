import psycopg2
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib  

# 1. Connect to your PostgreSQL database and retrieve the data
def fetch_data_from_db():
    # Setup your PostgreSQL connection
    conn = psycopg2.connect(
        dbname="postgres", 
        user="postgres", 
        password="ayagedoteta", 
        host="localhost", 
        port="5432"
    )

    query = "SELECT cpu_usage, memory_usage, disk_usage, network_sent, network_received FROM myapps_systemusage"
    
    # Fetch the data into a pandas DataFrame
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 2. Preprocess the data (handle missing values, scaling)
def preprocess_data(df, scaler=None):
    df.fillna(df.mean(), inplace=True)

    s
    if scaler:
        df_scaled = scaler.transform(df)  
    else:
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df) 

    return df_scaled, scaler

# 3. Load the pre-trained model and scaler
def load_model_and_scaler():
    # Assuming your model and scaler are saved
    model = model = joblib.load("../ai_modeling/scripts_/best_model.pkl")
    scaler = joblib.load("../ai_modeling/scripts_/scaler.pkl")  # Make sure the scaler is saved during training
    return model, scaler

# 4. Predict scaling needs based on the collected metrics
def predict_scaling_needs(df_scaled, model):
    predictions = model.predict(df_scaled)
    return predictions

# Main function to integrate all the steps
def main():
    # Fetch data from the PostgreSQL database
    df = fetch_data_from_db()

    # Load the pre-trained model and scaler
    model, scaler = load_model_and_scaler()

    # Preprocess the data
    df_scaled, scaler = preprocess_data(df, scaler)

    # Predict whether scaling is needed or not
    predictions = predict_scaling_needs(df_scaled, model)

    # Output the predictions
    df['needs_scaling'] = predictions
    print(df)

if __name__ == "__main__":
    main()

import os
import django
import time
import pandas as pd
import joblib

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from myapps.models import SystemUsage, ScalingPrediction

def load_model_and_scaler():
    model = joblib.load("ai_modeling/scripts_/best_model.pkl")
    scaler = joblib.load("ai_modeling/scripts_/scaler.pkl")
    return model, scaler

def get_unprocessed_data(limit=10):
    predicted_ids = ScalingPrediction.objects.values_list('system_usage_id', flat=True)
    return SystemUsage.objects.exclude(id__in=predicted_ids).order_by('-timestamp')[:limit]

def predict_scaling():
    model, scaler = load_model_and_scaler()

    while True:
        new_data = get_unprocessed_data()
        if new_data:
            df = pd.DataFrame(list(new_data.values(
                'cpu_usage', 'memory_usage', 'disk_usage', 'network_sent', 'network_received'
            )))
            df.fillna(df.mean(), inplace=True)

            # ✅ Rename to match feature names used during training
            df = df.rename(columns={
                'cpu_usage': 'cpu',
                'memory_usage': 'ram',
                'disk_usage': 'disk',
                'network_sent': 'network'
            })

            # Optional: Drop extra columns if model was trained on 4 features
            expected_columns = ['cpu', 'ram', 'disk', 'network']
            df = df[expected_columns]

            df_scaled = scaler.transform(df)
            results = model.predict(df_scaled)

            for usage_entry, prediction in zip(new_data, results):
                ScalingPrediction.objects.create(
                    system_usage=usage_entry,
                    needs_scaling=bool(prediction)
                )
            print(f"[✓] Predicted scaling for {len(new_data)} records.")
        else:
            print("[⏳] No new data. Waiting...")

        time.sleep(60)  # Run every 60 seconds

if __name__ == "__main__":
    predict_scaling()

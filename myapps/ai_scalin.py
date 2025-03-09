from .models import MonitoringData, ScalingAction, CloudInstance
import requests

def ai_based_scaling():
    """
    Uses AI to analyze past monitoring data and predict future resource needs.
    Automatically scales cloud resources based on demand predictions.
    """
    instances = CloudInstance.objects.all()
    
    for instance in instances:
        past_data = MonitoringData.objects.filter(instance=instance).order_by("-timestamp")[:100]
        predicted_demand = ai_model.predict(past_data)  # Mock AI model

        if predicted_demand == "increase":
            response = requests.post(f"{instance.api_url}/scale_up")
            ScalingAction.objects.create(instance=instance, action="scale_up", status=response.status_code)
        elif predicted_demand == "decrease":
            response = requests.post(f"{instance.api_url}/scale_down")
            ScalingAction.objects.create(instance=instance, action="scale_down", status=response.status_code)

    return "Scaling operation completed"

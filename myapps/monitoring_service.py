import requests
from .models import CloudInstance, MonitoringData

def monitor_cloud_resources():
    """
    Collects real-time monitoring data from cloud instances and stores it in the database.
    """
    instances = CloudInstance.objects.all()
    for instance in instances:
        response = requests.get(f"{instance.api_url}/metrics")  # Fetch metrics
        if response.status_code == 200:
            data = response.json()
            MonitoringData.objects.create(
                instance=instance,
                cpu_usage=data.get("cpu", 0),
                ram_usage=data.get("ram", 0),
                disk_usage=data.get("disk", 0),
            )
    return "Monitoring data updated successfully"

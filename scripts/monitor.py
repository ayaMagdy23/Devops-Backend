# import psutil
# import requests

# # URL for your Django API endpoint
# API_URL = "http://35.179.146.101:8000/api/post-monitor-data/"


# def collect_metrics():
#     """Collect system resource usage and send to Django API."""
#     cpu = psutil.cpu_percent(interval=1)
#     memory = psutil.virtual_memory().percent
#     disk = psutil.disk_usage('/').percent
#     net_io = psutil.net_io_counters()

#     # Calculate network usage in MB
#     network_sent = net_io.bytes_sent / (1024 * 1024)  
#     network_received = net_io.bytes_recv / (1024 * 1024)  

#     # Data to send to API
#     data = {
#         "cpu_usage": cpu,
#         "memory_usage": memory,
#         "disk_usage": disk,
#         "network_usage": network_sent + network_received,
#     }

#     # Print the data being sent to the server (for debugging purposes)
#     print(f"Data being sent: {data}")

#     try:
#         headers = {'Content-Type': 'application/json'}

#         # Send the data to the API
#         response = requests.post(API_URL, json=data, headers=headers)

#         # Log the response code and body
#         print("🔄 Request Sent:")
#         print(f"Response Code: {response.status_code}")
#         print(f"Response Body: {response.text}")

#         # Check the response status code for success
#         if response.status_code in [200, 201]:
#             print("✅ Metrics sent successfully!")
#         else:
#             print(f"❌ Failed to send data. Response: {response.text}")

#     except Exception as e:
#         print(f"⚠️ Error sending data: {e}")

# if __name__ == "__main__":
#     collect_metrics()

import socket
import psutil
import requests
import time

# URL for your Django API endpoint
API_URL = "http://35.179.146.101:8000/api/post-monitor-data/"

def collect_metrics():
    server_id = socket.gethostname()  # Get the server's hostname

    """Collect system resource usage and send to Django API."""
    cpu = psutil.cpu_percent(interval=60)  # Collect CPU usage over 60 seconds
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    net_io = psutil.net_io_counters()

    # Network usage in MB
    network_sent = net_io.bytes_sent / (1024 * 1024)
    network_received = net_io.bytes_recv / (1024 * 1024)
    network_usage = network_sent + network_received

    # Include server_id in the data sent to the API
    data = {
        "server_id": server_id,
        "cpu_usage": cpu,
        "memory_usage": memory,
        "disk_usage": disk,
        "network_usage": network_usage,
    }

    print(f"\n🔁 Sending metrics at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data being sent: {data}")

    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(API_URL, json=data, headers=headers)

        print("🔄 Request Sent:")
        print(f"Response Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        if response.status_code in [200, 201]:
            print("✅ Metrics sent successfully!")
        else:
            print(f"❌ Failed to send data. Response: {response.text}")

    except Exception as e:
        print(f"⚠️ Error sending data: {e}")

def start_monitoring(interval=60):
    """Continuously collect and send system metrics every N seconds."""
    try:
        while True:
            collect_metrics()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user.")
    except Exception as e:
        print(f"❗ Monitoring stopped due to error: {e}")

if __name__ == "__main__":
    start_monitoring(interval=60)  # Collect metrics every 60 seconds


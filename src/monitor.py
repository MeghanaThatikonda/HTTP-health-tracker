import sys
import yaml
import requests
import time
import logging

# Setting up logging configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(message)s', 
    handlers=[
        logging.StreamHandler(),  # Print to console
        logging.FileHandler('log/monitor_log.txt')  # Log to file
    ]
)

# function to load the input YAML file
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logging.error(f"Error: File {file_path} not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML file: {e}")
        sys.exit(1)

# checks the health of a single HTTP endpoint
def check_health(endpoint):
    """
    Parameters:
        endpoint (dict): Dictionary containing the details of the endpoint (url, method, headers, body).

    Returns:
        str: "UP" if the endpoint is healthy, "DOWN" otherwise.
        float: Response time in milliseconds.
    """
    url = endpoint.get("url")
    method = endpoint.get("method", "GET").upper()  # Default method is GET
    headers = endpoint.get("headers", {})
    body = endpoint.get("body", None)

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, data=body, timeout=5)
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds

        if 200 <= response.status_code < 300 and latency < 500:
            logging.info(f"Endpoint {url} is UP. Status Code: {response.status_code}, Latency: {latency:.2f}ms")
            return "UP", latency
        else:
            logging.warning(f"Endpoint {url} is DOWN. Status Code: {response.status_code}, Latency: {latency}ms")
            return "DOWN", latency

    except requests.RequestException as e:
        # Log the error and return DOWN
        logging.error(f"Error checking {url}: {e}")
        return "DOWN", None

# Monitors the health of endpoints periodically (every 15 seconds)
def monitor_endpoints(config):
    """
    Parameters:
        config (list): List of endpoint configurations.
    """
    domain_status = {}  # Dictionary to store availability stats for each domain
    domain_checks = {}  # Dictionary to count the total checks per domain

    while True:  # Infinite loop to keep monitoring
        print("\nStarting a new health check cycle...")
        for endpoint in config:
            url = endpoint["url"]
            domain = url.split("//")[-1].split("/")[0]  # Extract domain (e.g., fetch.com)
            
            # Check the health of the endpoint
            status, _ = check_health(endpoint)

            # Update domain stats
            if domain not in domain_status:
                domain_status[domain] = 0
                domain_checks[domain] = 0

            domain_checks[domain] += 1
            if status == "UP":
                domain_status[domain] += 1

        # Log availability percentages
        print("\nAvailability percentages:")
        for domain in domain_status:
            availability = (domain_status[domain] / domain_checks[domain]) * 100
            print(f"{domain} has {round(availability)}% availability")
            logging.info(f"{domain} has {round(availability)}% availability")

        # Wait for 15 seconds before the next cycle
        time.sleep(15)

if __name__ == "__main__":
    # checking if the input YAML file is passed in arguments
    if len(sys.argv) != 2:
        print("Usage: python monitor.py <configuration_file_path>")
        logging.error("Usage: python monitor.py <configuration_file_path>")
        sys.exit(1)
    config_file = sys.argv[1]
    # Reading the config YAML file
    config = read_file(config_file)
    # Checking health of endpoints every 15 secs
    monitor_endpoints(config)
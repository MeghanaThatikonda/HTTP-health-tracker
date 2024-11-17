# HTTP-health-tracker
A Python tool to monitor HTTP endpoint health, logging availability percentages and latency checks every 15 seconds.

Directory Structure
```
project-root/
├── input/                 # Contains configuration files (e.g., YAML files for endpoints)
│   └── config.yaml        # Example input configuration file
├── log/                   # Directory to store log files
│   └── monitor_log.txt    # Log file generated during monitoring
├── src/                   # Contains the source code
│   └── monitor.py         # Main script for monitoring endpoints
├── LICENSE                # License file for the project
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignored files and directories
```
## STEPS TO SIMULATE
1. Clone the repo
Clone the Repository:
```
git clone https://github.com/MeghanaThatikonda/HTTP-health-tracker.git
cd HTTP-health-tracker
```
2. Requirements
To install the required dependencies, run the following command:
```
pip install -r requirements.txt
```
3. Prepare Configuration: 
Place your YAML configuration file in the input/ directory for better structure. Alternatively, you can directly pass the file path to the script. This file should specify the endpoints to monitor. 

4. Run the Monitor: Execute the monitoring script:
```
python src/monitor.py <path_to_config_file>
```
Example: python src/monitor.py input/config.yaml

5. Check Logs: Monitor logs will be written to log/monitor_log.txt. Status messages will also appear in the console.
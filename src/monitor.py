import sys
import yaml

# function to load the input YAML file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


if __name__ == "__main__":
    # checking if the input YAML file is passed in arguments
    if(len(sys.argv) != 2):
        print("Usage: python monitor.py <configuration_file_path>")
        sys.exit(1)
    config_file = sys.argv[1]
    # Reading the config YAML file
    try:
        config = read_file(config_file)
    except FileNotFoundError:
        print(f"Error: File {config_file} not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")

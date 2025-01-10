import json
import os
import sys

# Default configuration values
default_config = {
    "TWEET_MAX_CHARS": 280,
    "HEADLESS_MODE": True,
    "ENGLISH_ONLY_REGEX": True,
    "SLEEP_TIME_PAGE_LOAD": 3,
    "SLEEP_TIME_AFTER_COOKIE_CONSENT": 0,
    "SLEEP_TIME_AFTER_TAB_CLICK": 1
}

# Get the config file path (in the same folder as the executable)
def get_config_file_path():
    if getattr(sys, 'frozen', False):  # If the program is running as a bundled executable
        # PyInstaller sets the 'frozen' attribute to True for bundled apps
        return os.path.join(os.path.dirname(sys.executable), 'config.txt')
    else:
        # If the script is running as a regular Python file
        return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'config.txt')

# Function to create default config file
def create_default_config(config_file_path):
    with open(config_file_path, 'w') as file:
        json.dump(default_config, file, indent=4)
    print(f"Config file created with default values at {config_file_path}")

# Load configuration from file
def load_config():
    config_file_path = get_config_file_path()

    # Check if the config file exists
    if not os.path.exists(config_file_path):
        # If config doesn't exist, create it with default values
        create_default_config(config_file_path)

    # Now try reading the config file
    try:
        with open(config_file_path, 'r') as file:
            config_data = json.load(file)
        return config_data

    # Handle the case where the JSON format is corrupted
    except json.JSONDecodeError:
        print(f"Error: The configuration file '{config_file_path}' is corrupted.")
        print("Please delete the file, and a new default config file will be generated next time.")
        exit(1)  # Exit with an error code

import argparse
import json
import logging
import requests
import subprocess
import time
import yaml
import sys
import os
import pathlib


#*Code to run a series of commands and parse the output to a json payload that can be sent to an API.
#?Not sure if this will work on Windows, but.....it Might
#!This is untested!


def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Command execution failed: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred during command execution: {e}")
        return None


def send_payload(url, payload):
    retries = 3
    for _ in range(retries):
        try:
            response = requests.post(url, json=payload)
            if response.ok:
                logging.info("Payload sent successfully")
                return True
            else:
                logging.warning(f"Failed to send payload: {response.status_code} {response.text}")
        except requests.exceptions.RequestException as e:
            logging.warning(f"API request failed: {e}")
        except Exception as e:
            logging.error(f"An error occurred during API request: {e}")

        #*Retry after a delay a total of 3 times before failing out.
        time.sleep(5)

    logging.error("Failed to send payload after retries")
    return False


def main(args):
    #*Configure a VERY basic logging function. Dont want to go too crazy here.
    logging.basicConfig(filename="script.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    #*try to load commands from YAML file
    try:
        
        with open(args.yaml_file) as file:
            commands = yaml.safe_load(file)
    except yaml.YAMLError as e:
        logging.error(f"Unable to open {yaml_file}. Received the following exception: {e}")
      

    #*Execute OS commands and build JSON payload
    #*Loop through the commands from a yaml file as key/value pairs.
    #Todo add handling for OS or Server specific commands. 
    payload = {}
    for key, command in commands.items():
        output = execute_command(command)
        if output is not None:
            payload[key] = output

    #*Send payload to API
    if not args.print_output:
        try:
            success = send_payload(args.api_url, payload)
        except Exception as e:
            logging.error(f"An error occurred during API request: {e}")
            success = False

        if success:
            logging.info("Script execution completed successfully")
        else:
            logging.error("Script execution failed")
            
            
    #* Option to simply print output instead of sending it somewhere. Handy for debugging or just simply printing a report.         
    if args.print_output:
        json_output = json.dumps(payload, indent=4)
        print(json_output)
        


if __name__ == "__main__":
    #*Parse command-line arguments
    parser = argparse.ArgumentParser(description="Script to execute commands and send payload with results to to an API")
    parser.add_argument("api_url", help="URL of the API endpoint")
    parser.add_argument("yaml_file", help="Path to the YAML file")
    parser.add_argument("--print-output", action="store_true", help="Print JSON output to the screen")
    args = parser.parse_args()

    # Run the main function with the provided API URL
    main(args.api_url, args.yaml_file)

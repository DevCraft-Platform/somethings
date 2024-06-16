# TPEdit, create your amazing website with ease.

import os
import sys
import json
import argparse
import logging
import subprocess
import shutil
import re
import time
import datetime
import survey
from app import main as window
import datetime


# Now we need to create a series of functions that will help us to check if everything is ok with the project

def parse_templates():
    # Returns a list of templates
    templates = []
    # We need to check if the templates folder exists
    if os.path.exists('templates'):
        # If it exists, append the dirs to the templates list
        if os.listdir('templates') != []:
            for template in os.listdir('templates'):
                if os.path.isdir('templates/' + template):
                    templates.append(template)
        else:
            logging.error('No templates found in the templates folder')
            sys.exit(1)
    else:
        logging.error('No templates folder found')
        sys.exit(1)
    return templates

if __name__ == "__main__":
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(filename='logs/tpe.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%H:%M:%S')
    logging.info(f"==================== {datetime.date.today()} - {datetime.datetime.now().strftime('%H:%M:%S')} ====================")
    logging.info('Starting TPEdit')
    logging.info('Checking if the project is valid')
    # First check if templates folder exists
    templates = parse_templates()
    # Now show the user the available templates
    template = survey.routines.select("Select a template: ", options=templates)
    print(f"Selected template: {templates[0]}")
    # Once the user has selected a template, we need to check if the project folder exists
    if template == 'None':
        print('No template selected')
        logging.error('No template selected')
        sys.exit(1)
    elif templates[template]:
        logging.info(f"Template selected: {templates[template]}")
        # Search for the template folder inside the templates folder
        if os.path.exists(f'templates/{templates[template]}'):
            logging.info(f'Template folder "{templates[template]}" found')
            # Check if a template.json file exists
            if os.path.exists(f'templates/{templates[template]}/template.json') and os.path.isfile(f'templates/{templates[template]}/template.json'):
                logging.info('template.json file found')
                # Load the template.json file
                with open(f'templates/{templates[template]}/template.json', 'r') as file:
                    template_json = json.load(file)
                # Now print the template information
                logging.info('Template information:')
                logging.info(f"Name: {template_json['template_name']}")
                logging.info(f"Author: {template_json['template_author']}")
                logging.info(f"Version: {template_json['template_version']}")
                # Now we execute the creation of the window
                    <script src="https://cdn.tailwindcss.com"></script>

        else:
            logging.error(f'No template folder "{template}" found')
            sys.exit(1)
    
    
    
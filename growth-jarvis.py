import requests

import json

import csv

# Set up authentication details (replace with your own)

email = 'matt.wilson@believes.co.uk'

api_token = 'nunyabizhoe'

# JIRA instance URL and API endpoint

server = 'https://nunyabiz.atlassian.net'

 

api_url = '/rest/api/2/search'  # We'll append parameters

 

# Set up the request headers and data payload

headers = {'Content-Type': 'application/json'}

data = {

    "jql": "assignee = currentUser()",

    "fields": [

        "key",

        "summary",

        "description",

        "status",

    ],

    "maxResults": 50,  # Using smaller batch size for better pagination

}

 

params = {"jsonwc": "v2"}  # Jira requires this for the JSON response format

 

# Make the request

try:

    response = requests.post(

        f"{server}{api_url}?maxResults=1000",

        auth=(email, api_token),

        headers=headers,

        json=data,

    )

 

    if response.status_code == 200:

        result = response.json()

        # Save the JSON to a file

        with open('my_tickets.json', 'w') as f:

            json.dump(result, indent=4, fp=f)

        print("Successfully saved tickets to my_tickets.json")

    else:

        print(f"Error: Received status code {response.status_code}, Response: {response.text}")

 

except Exception as e:

    print(f"An error occurred: {e}")

   

api_url = '/rest/api/3/search'  # v3 API

headers = {'Content-Type': 'application/json'}

 

# Query and fields

data = {

    "jql": "assignee = currentUser()",

    "fields": [

        "key",

        "summary",

        "description",

        "status"

    ],

    "maxResults": 50

}

 

# Request

response = requests.post(

    f"{server}{api_url}",

    auth=(email, api_token),

    headers=headers,

    json=data

)

 

# Flatten description from ADF

def extract_description(adf_content):

    if not adf_content:

        return ""

 

    def walk_nodes(nodes):

        text = ""

        for node in nodes:

            if node.get("type") == "text":

                text += node.get("text", "")

            elif "content" in node:

                text += walk_nodes(node["content"])

            elif node.get("type") == "paragraph":

                text += "\n"

        return text

 

    return walk_nodes(adf_content.get("content", []))

 

# Save and print

if response.status_code == 200:

    result = response.json()

    for issue in result["issues"]:

        key = issue["key"]

        summary = issue["fields"]["summary"]

        raw_description = issue["fields"].get("description", {})

        clean_description = extract_description(raw_description)

 

        print(f"\n🧾 {key}: {summary}")

        print(clean_description)

 

    with open('my_tickets.json', 'w') as f:

        json.dump(result, f, indent=4)

else:

    print(f"Error {response.status_code}: {response.text}")

   

    

 

if response.status_code == 200:

    result = response.json()

 

    with open('my_tickets.csv', 'w', newline='', encoding='utf-8') as csvfile:

        fieldnames = ['key', 'summary', 'description']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

 

        for issue in result["issues"]:

            key = issue["key"]

            summary = issue["fields"]["summary"]

            raw_description = issue["fields"].get("description", {})

            clean_description = extract_description(raw_description)

 

            writer.writerow({

                'key': key,

                'summary': summary,

                'description': clean_description

            })

 

    print("✅ CSV export complete: my_tickets.csv")

else:

    print(f"Error {response.status_code}: {response.text}")
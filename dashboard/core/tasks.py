from celery import shared_task

from django.shortcuts import render , redirect
import requests
import ssl
import json
from bs4 import BeautifulSoup
import certifi

@shared_task(bind=True)
def crawler_task(self):
    # Read the JSON file
    with open('file.json', encoding='utf-8' ) as f:
        data = json.load(f)
        timeout_seconds = 10  # Set the timeout period to 10 seconds

        # Fetch all keys in the JSON data
        keys = data.keys()
        
        # Print all keys
        for url in keys:
            # CHECK IF URL RUNS OR NOT 
            try:    
                response = requests.get(url, verify=False,timeout=timeout_seconds)
                if response.status_code == 200:
                    data[url]["domain_token"] = True
        
            except requests.ConnectionError as e:
                data[url]["domain_token"] =  False    

            # CHECK IF SSL IS VALID OR NOT 
            try:
                response = requests.get(url,verify=certifi.where())
                print("SSL RESPONSE ", response)
                if response.status_code == 200:
                    data[url]["ssl_token"] =  True                  
            except requests.ConnectionError:
                data[url]["ssl_token"] =  False
            except ssl.SSLError:
                data[url]["ssl_token"] =  False
       
            # CHECK LANGUAGE OF CONTENT 
            try:
                # Fetch HTML content from the URL
                response = requests.get(url,verify=False)
                print("RESPONSE CODE ---------------------------- ",response.status_code)
                if response.status_code == 200:
                    # Parse HTML content
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract text content from HTML
                    text = soup.get_text()
                   
                    # Detect language of the text
                    try:
                        service_url = 'http://gist-nlp-cip:8080/languageIdentify'
                        headers = {'User-Agent': 'Mozilla/5.0'}  # Example of headers
                        myobj = {"ip_text": text}
                        x = requests.post(service_url, headers=headers, json= myobj)
                        data[url]["content_token"] = json.loads(x.text)['Output']
                    except requests.ConnectionError as e:
                        print("Exception -----", e)
                        print("Service Not Available ")
                        data[url]["content_token"] = "Service Not Available"
                else:
                    print(f"Failed to fetch URL. Status code: {response.status_code}")
                    data[url]["content_token"] = False

            except requests.ConnectionError as e:
                print(f"Connection error: {e}")
                data[url]["content_token"] = False

            except Exception as e:
                print(f"Error occurred: {e}")
                data[url]["content_token"] = False
    # Convert dictionary back to JSON
    updated_json_data = json.dumps(data)

    # Write updated JSON data to a new file
    with open('updated_file.json', 'w') as outfile:
        outfile.write(updated_json_data)
    # Print updated JSON
    return "Done"
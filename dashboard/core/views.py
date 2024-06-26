from django.shortcuts import render , redirect
import requests
import ssl
import json
from bs4 import BeautifulSoup
import json
import plotly.graph_objs as go
import idna
import punycode
import idna
import idna
from urllib.parse import urlparse
import certifi
from core.tasks import crawler_task
from django.contrib import messages
import pandas as pd
from .forms import idn_dashboard_form
# Create your views here.


    
def idn_dashboard_view(request):
    idn_dashboard_form_obj = idn_dashboard_form()
    
    if request.method == 'POST':
        form = idn_dashboard_form(request.POST)
        # english_domain = request.POST.get('English_domain')
        # idn_domain=request.POST.get('IDN_domain')
        # idn_language =request.POST.get('Idn_language')
        # print("english domain-----------",english_domain)
        # print("idn domain-----------",idn_domain)
        # print("language---------", idn_language)

        # Check if form is valid or not and any params is not null
        if form.is_valid():
            form_obj = form.save(commit=False)
            print('form_OBJ',form_obj)

            form_obj.content_language = 'False'
            form_obj.ssl_configuration_status='False'
            form_obj.idn_domain_running_status='False'
            form_obj.Remark='test'

            
            try:
                print("inside save")
                form_obj.save()
            except Exception as e:
                print('e',e)
            return render(request, 'core/test.html', {'idn_dashboard_form_obj': "your entry submitted successfully"})
        else:
            print("not submitting ", form.errors)
            return render(request, 'core/urladdform.html', {'idn_dashboard_form_obj': idn_dashboard_form_obj}) 

    else:
        return render(request, 'core/urladdform.html', {'idn_dashboard_form_obj': idn_dashboard_form_obj})
   


def home(request):
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
                response = requests.get(url,verify=False,allow_redirects=True, max_redirects=60)
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
                        lang_token = json.loads(x.text)['Output']
                        if (lang_token == "latin"):
                            data[url]["content_token"] = "English"
                        else:
                            data[url]["content_token"] = lang_token
                    except requests.ConnectionError as e:
                        print("Language Content Exception -----", e)
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
    print(updated_json_data)
    return render(request,'core/home.html',{'updated_json_data':updated_json_data})


def display_table2(request):
    with open('updated_file.json') as f:
        Tabledata = json.load(f) 
    return render(request, 'core/table2.html', {'Tabledata': Tabledata})


def urladd(request):
    
    return render(request,'core/urladdform.html')


def update_json(request):
    new_url = request.POST.get('url')
    new_lang = request.POST.get('language')
   
    # Read the JSON file
    with open('file.json', encoding='utf-8' ) as f:
        data = json.load(f)

    # Add new key-value pair
    data[new_url] = {
        "Language": new_lang,
        "domain_token": "",
        "ssl_token": "",
        "content_token": ""
    }

    # Write the updated JSON data back to the file
    with open('file.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Convert dictionary back to JSON
    updated_json_data = json.dumps(data)
    ##crawler_task.delay()
    messages.info(request,"Your data would be populated in IDN Readiness Index List within 24 Hours ")
    return redirect('core:display_table2')
    # return render(request,'core/updatejson.html',{"updated_json_data":updated_json_data})




from urllib.request import urlopen
from urllib.error import HTTPError, URLError

def check(request):
    # URL to fetch
    url = 'https://dpe.gov.in'

    try:
        # Open the URL and read its contents
        with urlopen(url) as response:
            # Check the HTTP status code
            status_code = response.getcode()
            print("codeeeeeeeeeeeeeeeeeeeeeeeeeeeeee----",status_code)
            if 1:
                # If the status code is 200 (OK), read the response content
                html = response.read()
                # Print the HTML content
                print(html.decode('utf-8'))  # Decode bytes to UTF-8 and print
            else:
                # If the status code is not 200, print an error message
                print(f'Error: HTTP status code {status_code}')
                
    except HTTPError as e:
        # Handle HTTP errors
        print(f'HTTPError: {e.code} - {e.reason}')
        
    except URLError as e:
        # Handle URL errors
        print(f'URLError: {e.reason}')


def add_urls(request):
    # Load the existing JSON data
    existing_data = {
        "https://bhashanet.in": {
            "Language": "English",
            "domain_token": "",
            "ssl_token": "",
            "content_token": ""
        }
    }

    # Read data from the Excel file
    excel_file = "url_excel_file.xlsx"  # Replace with the path to your Excel file
    df = pd.read_excel(excel_file)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        url = row["URL"]
        url = "https://"+url
        language = row["Language"]

        # Update the existing JSON data with the new URL and language
        existing_data[url] = {
            "Language": language,
            "domain_token": "",
            "ssl_token": "",
            "content_token": ""
        }
        
        # Save the updated JSON data to a file
    output_file = "updated_data.json"  # Specify the path for the output JSON file
    with open(output_file, "w") as f:
        json.dump(existing_data, f, indent=2)
    print(f"Updated JSON data has been saved to {output_file}")
from django.shortcuts import render
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
# from langdetect import detect
def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain

# Create your views here.
def home(request):

    # Read the JSON file
    with open('file.json') as f:
        data = json.load(f)
        # Fetch all keys in the JSON data
        keys = data.keys()
        print(keys)
        # Print all keys
        for url in keys:
            baseurl = url
            print("ALLLLLLLLLLLLLLLLLLLL--",url)
            # CHECK IF URL RUNS OR NOT 
            try:
                domain = extract_domain(url)
                print("DOMAINNNNNNNNNNNNNNNN",domain)
                full_url = idna.encode("डीपीई.सरकार.भारत")
                print("Full N",full_url)
                full_url = full_url.decode('utf-8')
                url = "https://"+ full_url
                print("SANJAY -----0",url)
                response = requests.get(url)
                data[baseurl]["domain_token"] =  response.status_code == 200
            except requests.ConnectionError:
                data[baseurl]["domain_token"] =  False    
             
            # CHECK IF SSL IS VALID OR NOT 
            try:
                response = requests.get(url, verify=True)
                if response.status_code == 200:
                    data[url]["ssl_token"] =  True
                  
            except requests.ConnectionError:
                data[baseurl]["ssl_token"] =  False
            except ssl.SSLError:
                data[baseurl]["ssl_token"] =  False
       
            # CHECK LANGUAGE OF CONTENT 
            try:
                # Fetch HTML content from the URL
                response = requests.get(url)
                if response.status_code == 200:
                    # Parse HTML content
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Extract text content from HTML
                    text = soup.get_text()
                    # print(text)
                    # Detect language of the text
                    service_url = 'http://gist-nlp-cip:8080/languageIdentify'
                    headers = {'User-Agent': 'Mozilla/5.0'}  # Example of headers
                    myobj = {"ip_text": text}
                    x = requests.post(service_url, headers=headers, json= myobj)
                    data[url]["content_token"] = json.loads(x.text)['Output']
                else:
                    print(f"Failed to fetch URL. Status code: {response.status_code}")
                    data[url]["content_token"] = False
            except requests.ConnectionError as e:
                print(f"Connection error: {e}")
                data[baseurl]["content_token"] = False
            except Exception as e:
                print(f"Error occurred: {e}")
                data[baseurl]["content_token"] = False
    # Convert dictionary back to JSON
    updated_json_data = json.dumps(data)

    # Write updated JSON data to a new file
    with open('updated_file.json', 'w') as outfile:
        outfile.write(updated_json_data)
    # Print updated JSON
    print(updated_json_data)

    return render(request,'core/home.html',{'updated_json_data':updated_json_data})



def chart(request):

    with open('updated_file.json') as f:
        data = json.load(f)

        # Extracting keys and values for the chart
        urls = list(data.keys())
        content_tokens = [data[url]["content_token"] for url in urls]

        # Counting occurrences of each content token
        token_counts = {}
        for token in content_tokens:
            token_counts[token] = token_counts.get(token, 0) + 1

        # Creating the bar chart
        chart_data = [go.Bar(x=list(token_counts.keys()), y=list(token_counts.values()))]
        layout = go.Layout(title="Content Tokens Distribution", xaxis=dict(title="Content Tokens"), yaxis=dict(title="Count"))
        chart_fig = go.Figure(data=chart_data, layout=layout)
        chart_div = chart_fig.to_html(full_html=False)

        return render(request, 'core/chart.html', {'chart_div': chart_div})



def stackedchart(request):
    with open('updated_file.json') as f:
        data = json.load(f)
        # Count occurrences of SSL tokens (true/false) for each content token category
    ssl_token_counts = {"True": {}, "False": {}}
    for url, info in data.items():
        content_token = info["content_token"]
        ssl_token = str(info["ssl_token"])  # Convert boolean to string
        if content_token not in ssl_token_counts["True"]:
            ssl_token_counts["True"][content_token] = 0
            ssl_token_counts["False"][content_token] = 0
        ssl_token_counts[ssl_token][content_token] += 1

    # Prepare data for the stacked bar chart
    content_tokens = list(ssl_token_counts["True"].keys())
    true_counts = list(ssl_token_counts["True"].values())
    false_counts = list(ssl_token_counts["False"].values())

    # Create the stacked bar chart
    fig = go.Figure(data=[
        go.Bar(name='SSL True', x=content_tokens, y=true_counts),
        go.Bar(name='SSL False', x=content_tokens, y=false_counts)
    ])
    # Update layout
    fig.update_layout(barmode='stack', title="SSL Token Distribution by Content Token",
                      xaxis_title="Content Token", yaxis_title="Count")

    # Convert the plotly figure to HTML
    chart_div = fig.to_html(full_html=False)
    return render(request, 'core/stackedchart.html', {'chart_div': chart_div})

def piechart(request):
    with open('updated_file.json') as f:
        data = json.load(f)
       
        #chart for showing number of working urls and not working urls 
        # Count the number of working and not working URLs
        working_urls_count = sum(1 for url_info in data.values() if url_info.get("domain_token", False))
        not_working_urls_count = sum(1 for url_info in data.values() if not url_info.get("domain_token", False))

        # Create pie chart
        fig = go.Figure(data=[go.Pie(labels=["Working URLs", "Not Working URLs"], values=[working_urls_count, not_working_urls_count])])

        # Update layout
        fig.update_layout(title="Distribution of Working and Not Working URLs")


        # Convert the plotly figure to HTML
        chart_div = fig.to_html(full_html=False)

    return render(request, 'core/piechart.html', {'chart_div': chart_div})



def display_table(request):
    with open('updated_file.json') as f:
        Tabledata = json.load(f)

    with open('updated_file.json') as f:
        data = json.load(f)
       
        #chart for showing number of working urls and not working urls 
        # Count the number of working and not working URLs
        working_urls_count = sum(1 for url_info in data.values() if url_info.get("domain_token", False))
        not_working_urls_count = sum(1 for url_info in data.values() if not url_info.get("domain_token", False))

        # Create pie chart
        fig = go.Figure(data=[go.Pie(labels=["Working URLs", "Not Working URLs"], values=[working_urls_count, not_working_urls_count])])

        # Update layout
        fig.update_layout(title="Distribution of Working and Not Working URLs")


        # Convert the plotly figure to HTML
        chart_div = fig.to_html(full_html=False)


        # NUMBER OF FUNCTIONAL DOMAINS AND NON FUNCTIONAL DOMIANS
        with open('updated_file.json') as f:
            data = json.load(f)

            # Count the number of functional and non-functional domains
            functional_domains_count = sum(1 for url_info in data.values() if url_info.get("domain_token", False))
            non_functional_domains_count = sum(1 for url_info in data.values() if not url_info.get("domain_token", False))

            # Create pie chart
            fig = go.Figure(data=[go.Pie(labels=["Functional Domains", "Non-functional Domains"], 
                                        values=[functional_domains_count, non_functional_domains_count])])

            # Update layout
            fig.update_layout(title="Distribution of Functional and Non-functional Domains")

            # Convert the plotly figure to HTML
            chart_div2 = fig.to_html(full_html=False)    


        ## BUBBLE CHART 
        # Load JSON data from file
        with open('updated_file.json') as f:
            data = json.load(f)

            # Initialize lists to store data for bubble chart
            urls = []
            x_values = []
            y_values = []
            bubble_sizes = []

            # Assign unique x-coordinate for each URL
            x_counter = 1

            # Convert domain functionality, SSL validity, and content localization to numerical values
            for url, info in data.items():
                urls.append(url)
                x_values.append(x_counter)
                y_values.append(1 if info.get('domain_token', False) else 0)  # 1 for True, 0 for False
                bubble_sizes.append(5 if info.get('ssl_token', False) else 0)  # Bubble size based on SSL validity
                x_counter += 1

            # Create bubble trace
            bubble_trace = go.Scatter(
                x=x_values,
                y=y_values,
                mode='markers',
                marker=dict(
                    size=bubble_sizes,
                    sizemode='area',
                    sizeref=2.0 * max(bubble_sizes) / (40 ** 2),
                    sizemin=4
                ),
                text=urls
            )

            # Create layout
            layout = go.Layout(
                title='Bubble Chart of Domain Functionality and SSL Validity',
                xaxis=dict(title='URL'),
                yaxis=dict(title='Domain Functionality'),
            )

            # Create figure
            fig = go.Figure(data=[bubble_trace], layout=layout)

            # Convert the plotly figure to HTML
            chart_div3 = fig.to_html(full_html=False)    

    return render(request, 'core/table.html', {'Tabledata': Tabledata,'chart_div':chart_div,'chart_div2':chart_div2,'chart_div3':chart_div3})






def display_table2(request):
    with open('updated_file.json') as f:
        Tabledata = json.load(f)

    with open('updated_file.json') as f:
        data = json.load(f)
       
        #chart for showing number of working urls and not working urls 
        # Count the number of working and not working URLs
        working_urls_count = sum(1 for url_info in data.values() if url_info.get("domain_token", False))
        not_working_urls_count = sum(1 for url_info in data.values() if not url_info.get("domain_token", False))

        # Create pie chart
        fig = go.Figure(data=[go.Pie(labels=["Working URLs", "Not Working URLs"], values=[working_urls_count, not_working_urls_count])])

        # Update layout
        fig.update_layout(title="Distribution of Working and Not Working URLs")


        # Convert the plotly figure to HTML
        chart_div = fig.to_html(full_html=False)


        # NUMBER OF FUNCTIONAL DOMAINS AND NON FUNCTIONAL DOMIANS
        with open('updated_file.json') as f:
            data = json.load(f)

            # Count the number of functional and non-functional domains
            functional_domains_count = sum(1 for url_info in data.values() if url_info.get("domain_token", False))
            non_functional_domains_count = sum(1 for url_info in data.values() if not url_info.get("domain_token", False))

            # Create pie chart
            fig = go.Figure(data=[go.Pie(labels=["Functional Domains", "Non-functional Domains"], 
                                        values=[functional_domains_count, non_functional_domains_count])])

            # Update layout
            fig.update_layout(title="Distribution of Functional and Non-functional Domains")

            # Convert the plotly figure to HTML
            chart_div2 = fig.to_html(full_html=False)    


        ## BUBBLE CHART 
        # Load JSON data from file
        with open('updated_file.json') as f:
            data = json.load(f)

            # Initialize lists to store data for bubble chart
            urls = []
            x_values = []
            y_values = []
            bubble_sizes = []

            # Assign unique x-coordinate for each URL
            x_counter = 1

            # Convert domain functionality, SSL validity, and content localization to numerical values
            for url, info in data.items():
                urls.append(url)
                x_values.append(x_counter)
                y_values.append(1 if info.get('domain_token', False) else 0)  # 1 for True, 0 for False
                bubble_sizes.append(5 if info.get('ssl_token', False) else 0)  # Bubble size based on SSL validity
                x_counter += 1

            # Create bubble trace
            bubble_trace = go.Scatter(
                x=x_values,
                y=y_values,
                mode='markers',
                marker=dict(
                    size=bubble_sizes,
                    sizemode='area',
                    sizeref=2.0 * max(bubble_sizes) / (40 ** 2),
                    sizemin=4
                ),
                text=urls
            )

            # Create layout
            layout = go.Layout(
                title='Bubble Chart of Domain Functionality and SSL Validity',
                xaxis=dict(title='URL'),
                yaxis=dict(title='Domain Functionality'),
            )

            # Create figure
            fig = go.Figure(data=[bubble_trace], layout=layout)

            # Convert the plotly figure to HTML
            chart_div3 = fig.to_html(full_html=False)    

    return render(request, 'core/table2.html', {'Tabledata': Tabledata,'chart_div':chart_div,'chart_div2':chart_div2,'chart_div3':chart_div3})



def converturl(request):
    unicode_string = "डीपीई.सरकार.भारत"
    punycode_string = idna.encode(unicode_string)
    print('punycode_string',punycode_string)

    punycode_string = "https://xn--p5by0ags3b6blfceb.xn--45brj9c"
    unicode_string = idna.decode(unicode_string)
    print('unicode_string',unicode_string)
    

    return render(request, 'core/convertedurl.html', {'punycode_string':punycode_string,'unicode_string':unicode_string})

import requests
import csv
import os
import datetime
import json
import argparse

argparser = argparse.ArgumentParser(description='Europeana API data extraction')

argparser.add_argument('-s', '--search_term', type=str, default='airplane', help='Search term', required=True)
argparser.add_argument('-n', '--number_of_iterations', type=int, default=10, help='Number of iterations to run', required=True)
argparser.add_argument('-o', '--output_csv', type=str, default='europeana.csv', help='Output CSV file', required=False)
argparser.add_argument('-m', '--metadata_folder', type=str, default='metadata_dump', help='Metadata dump folder', required=False)
argparser.add_argument('-cursor', '--nextcursor', type=str, help='Next cursor', required=False)


args = argparser.parse_args()

number_of_iterations = args.number_of_iterations
search_term = args.search_term
output_csv = args.output_csv
metadata_folder = args.metadata_folder
nextcursor = args.nextcursor

cursorselected = False
if not nextcursor:
    print("No nextcursor provided. Starting from the beginning.")
    nextcursor = "*"
else:
    print(f"Starting from the provided nextcursor: {nextcursor}")
    cursorselected = True


def timestamp_to_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')


def write_to_csv(json_response, filename):
    custom_headers = ['url','title', 'provider', 'year', 'copyrights', 'country', 'description', 'language', 'creation_date', 'europeana_url']
    
    file_exists = os.path.exists(filename)
    
    with open(filename, 'a+', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=custom_headers)
        if not file_exists:
            writer.writeheader()
        
        for item in json_response["items"]:
            row_data = {}
            
            for header in custom_headers:
                if header == 'url':
                    row_data['url'] = ", ".join(item.get("edmIsShownBy", ""))
                    row_data['url'] = f'"{row_data["url"]}"' 
                elif header == 'description':
                    row_data['description'] = ", ".join(item.get("dcDescription", ""))
                    row_data['description'] = f'"{row_data["description"]}"' 
            
                elif header == 'provider':
                    row_data['provider'] = ", ".join(item.get("provider", ""))
                elif header == 'year': 
                    year_value = item.get("year", []) 
                    row_data['year'] = str(year_value[0]) if year_value else ""
                elif header == 'copyrights':
                    row_data['copyrights'] = ", ".join(item.get("rights", ""))
                elif header == 'country':
                    row_data['country'] = ", ".join(item.get("country", ""))
                elif header == 'title':
                    row_data['title'] = ", ".join(item.get("title", ""))
                    row_data['title'] = f'"{row_data["title"]}"' 
                elif header == 'language':
                    row_data['language'] = ", ".join(item.get("language", ""))
                elif header == 'creation_date':
                    row_data['creation_date'] = timestamp_to_date(item.get("timestamp", 0))
                elif header == 'europeana_url':
                    row_data['europeana_url'] = ", ".join(item.get("edmIsShownAt", ""))
         

            
            writer.writerow(row_data)

def get_config_path(file_path):
    script_dir = os.path.dirname(os.path.abspath(file_path))
    config_path = os.path.join(script_dir, 'config.properties')
    return config_path

def get_api_value(file_path):
    config_path = get_config_path(file_path)
    api_value = None
    with open(config_path, 'r') as file:
        for line in file:
            if line.strip().startswith('api: '):
                api_value = line.strip()[len('api: '):].strip()
                break
    return api_value


def europeana_json(term, api, nextcursor="*"):
    DEFAULT_QUERY_PARAMS = {
    'wskey': api, 
    'query': term,
    'profile': 'standard',
    'reusability': ['open', 'restricted'],
    'sort': ['europeana_id+desc', 'timestamp_created_epoch+desc'],
    'cursor': nextcursor,
    'rows': 100,
    'media': 'true',
    'qf': ['TYPE:IMAGE'],
    'languageCodes': 'en',
    }
    base_url = 'https://api.europeana.eu/record/v2/'
    json_url = f"{base_url}search.json"
    json_params = DEFAULT_QUERY_PARAMS
    json_params['thumbnail'] = 'true'
    json_response = requests.get(json_url, params=json_params, headers={'accept': 'application/json'})
    json_response = json_response.json()
    return json_response, json_response['nextCursor']

def json_dump(json_response, folder, filename):

    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename + '.json')    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(json_response, f, indent=4, ensure_ascii=False)


config_file_path = 'config.properties'
api = get_api_value(config_file_path)

#initial iteration
json_response, nextcursor = europeana_json(search_term, api, "*")
write_to_csv(json_response, output_csv)
if cursorselected:
    json_dump(json_response, metadata_folder, f"cursored_{search_term}_step_0")
else: 
    json_dump(json_response, metadata_folder, f"{search_term}_step_0")


for i in range(number_of_iterations-1):
    json_response, nextcursor = europeana_json(search_term, api, nextcursor)
    write_to_csv(json_response, output_csv)
    if cursorselected:
        json_dump(json_response, metadata_folder, f"cursored_{search_term}_step_{i+1}")
    else:
        json_dump(json_response, metadata_folder, f"{search_term}_step_{i+1}")
    if json_response["itemsCount"] < 100:
        print("This is the last iteration. No more items to fetch.")
        break
if json_response["itemsCount"] < 100:
    print(f"Iteration number {i+1} is the last iteration. No more items to fetch.")
else: print(f"Done!\nYour nextcursor after your {number_of_iterations} iterations is: \n{nextcursor}")

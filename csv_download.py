import os
import csv
import requests
import argparse

argparser = argparse.ArgumentParser(description='Europeana API data download')

argparser.add_argument('-i', '--input_csv', type=str, default='europeana.csv', help='Input CSV file', required=False)
argparser.add_argument('-o', '--output_folder', type=str, default='images', help='Output folder', required=False)   

args = argparser.parse_args()



def download_file(url, output_folder, timeout=20):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            filename = os.path.join(output_folder, os.path.basename(url))
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {url}")
        else:
            print(f"Failed to download: {url}. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Failed to download: {url}. Exception: {e}")
        with open('failed_links.txt', 'a') as f:
            f.write(url + '\n')
        return False

    return True

input_csv = args.input_csv
output_folder = args.output_folder

with open(input_csv, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    i = 1
    for row in reader:
        url = row['url'].strip('"')
        print(f"Downloading image number: {i} - {url}")
        success = download_file(url, output_folder)
        i += 1

# Europeana search engine for images and metadata
This is a simple search engine for Europeana API to search for images and metadata. The search engine is implemented using Python.

<div style="text-align: center;">
    <img src="ressources/europeana.png" alt="Image 2" style="width: 200px; height: 200px;">
</div>

<!--

<div style="display: flex; justify-content: center;">
    <img src="ressources/europeana.png" alt="Image 1" style="width: 100px; height: 100px; margin-right: 10px;">
    <img src="ressources/fh.jpg" alt="Image 3" style="width: 100px; height: 100px; margin-right: 10px;">
    <img src="ressources/tu.png" alt="Image 4" style="width: 100px; height: 100px;">
</div>
-->

## Pre-requisites
Apply for the Europeana API key from [Europeana Pro](https://pro.europeana.eu/page/get-api) and add it in the `config.properties` file.

## How it works

The sript `fetch_europeana.py` takes the search query as input along with the number of iterations to fetch the lengthy, complicated response from the Europeana API and analyze it and take what's useful to be stored in an output csv file in which we store the information we redeem to be useful for us (See `example.csv`).
Note: if you would like to add more filters to the search query, you can suggest in the issues and we will try to implement it or you can implement it yourself and make a pull request.

## Other need-to-knows

The reason we use `number of iterations` is because the Europeana API returns a maximum of 100 results per request (see [europeana documentation](https://pro.europeana.eu/page/search#:~:text=of%20the%20response.-,rows,-Number)), so if you want to fetch more than 100 results, we need to repeat the request multiple times. So the number of outputs is `number of iterations * 100`.

at the end of an execution, the script will print the a string called `cursor` which is the next cursor to be used in the next iteration if you want to fetch more results. It refers to the next page of results of what you have previously searched. The usage of cursor is dectated by the Europeana API as it has been refer to in the [here](https://pro.europeana.eu/page/search#pagination-cursor).

In the metadata_dump folder after running the script you will find json files of the api response as it is (1 file per 100 items). In case you find something that is of interest and can be added to the output csv file, you can suggest it in the issues or implement it yourself and make a pull request.

## Content

The repository contains the following files:
1. `fetch_europeana.py`: The main script to fetch the data from Europeana API.
2. `config.properties`: The configuration file to store the API key.
3. `csv_downloader.py`: The script to download the images from the URLs in the output csv file.
4. `example.csv`: The example output file.

## Usage guide

1. Clone the repository.
2. Add the Europeana API key in the `config.properties` file.
3. Run the script `fetch_europeana.py` with the search query and number of iterations as arguments.

```bash
python fetch_europeana.py -s <search term> -n <number of iterations> -o <output file name> -m <metadata dump> -cursor <cursor>
```
The arguments are:
- -s: The search term.
- -n: The number of iterations.
- -o: The output file name.
- -m: The metadata dump file name.
- -cursor: The cursor to fetch the next page of results.

Note: 
The cursor, metadata dump, and output file name are optional arguments.


Example:

```bash
python fetch_europeana.py -s "airplane" -n 10 
```
Example with optional arguments:

```bash
python fetch_europeana.py -s "airplane" -n 10 -o "europeana.csv" -m "metadata_dump" -cursor "AoJ4cHJvZ  
```

4. The output will be stored in the `output.csv` file.
5. Run the script `csv_downloader.py` to download the images from the URLs in the output csv file.

## Contributors
- [Nidham Tekaya](https://www.nidham-tekaya.me/)

(Feel free to add your name if you have contributed to the project)



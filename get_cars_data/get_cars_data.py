import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
from datetime import datetime
import time
from random import randint
import csv

def log_event(log_message, log_type="INFO"):
    """
    Appends a log event to the log CSV file.

    Args:
    log_message (str): The message to log.
    log_type (str): The type of log message (e.g., INFO, ERROR). Defaults to "INFO".
    """
    log_filename = 'script_logs.csv'
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([now_str, log_type, log_message])

def get_soup(url_link):
    """
    Sends a request to the specified URL and returns a BeautifulSoup object for parsing.
    
    Args:
    url_link (str): The URL of the website to scrape.

    Returns:
    BeautifulSoup: A BeautifulSoup object to parse the HTML content.
    """
    log_event('Getting soup')
    url = url_link
    log_event(url)
    
    r = requests.get(url)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    return soup

def get_cars_data(soup):
    """
    Extracts car data from the JavaScript section of a webpage.

    Args:
    soup (BeautifulSoup): The BeautifulSoup object containing the HTML content.

    Returns:
    dict: A dictionary containing car data.
    """
    log_event('Getting car data')
    scripts = soup.find_all('script')
    for script in scripts:
        if 'window.__BONNET_DATA__' in script.text:
            start = script.string.find('window.__BONNET_DATA__') + len('window.__BONNET_DATA__=')
            json_str = script.string[start:].strip()
            end = json_str.rfind('}') + 1
            json_str = json_str[:end]
            data = json.loads(json_str)
            car_data = data['initialState']
    return car_data

def normalize_model(model):
    """
    Normalizes the 'model' field of the car data.

    Args:
    model: The model field value.

    Returns:
    str: Normalized model name.
    """
    log_event('Normalizing model')
    if isinstance(model, dict):
        return model['name']
    return model

def get_cars_dataframe(car_json, car_ids):
    log_event('Getting DataFrame')
    car_info_list = []
    car_json = car_json['inventory']
    
    for car_id in car_ids:
        car_id_str = str(car_id)
        if car_id_str in car_json:
            car_data = car_json[car_id_str]
            specifications = car_data.get('specifications', {})
            pricingDetail = car_data.get('pricingDetail', {})
            make = car_data.get('make', {})
            model = car_data.get('model', {})
            # Assuming 'vin' is directly available in car_data dictionary
            vin = car_data.get('vin', 'Not available')  # Add this line
            car_info = {
                'id': car_data.get('id', 'Not available'),
                'vin': vin,  # Include vin here
                'price': pricingDetail.get('salePrice', 'Not available'),
                'make': make.get('name', 'Not available'),
                'model': model.get('name', 'Not available'),
                'year': car_data.get('year', 'Not available'),
                'mileage': specifications.get('mileage', {}).get('value', 'Not available'),
                'fueltype': specifications.get('fuelType', {}).get('value', 'Not available'),
                'packages': car_data.get('packages', 'Not available'),
                'driveType': specifications.get('driveType', {}).get('value', 'Not available'),
                'engine': specifications.get('engine', {}).get('value', 'Not available'),
                'color_ext': specifications.get('color', {}).get('value', 'Not available'),
                'color_int': specifications.get('interiorColor', {}).get('value', 'Not available'),
                'transmission': specifications.get('transmission', {}).get('value', 'Not available'),
                'trim': car_data.get('trim', {}).get('name', 'Not available')  # Assuming trim is a dictionary with a name key
            }
            car_info_list.append(car_info)
    df = pd.DataFrame(car_info_list)
    return df

def replace_na_mileage(cars_df):
    """
    Processes the 'mileage' column in the DataFrame, replacing N/A with NaN and calculating averages.

    Args:
    cars_df (DataFrame): The DataFrame containing car data.

    Returns:
    DataFrame: The updated DataFrame with processed mileage values.
    """
    log_event('Replacing NA in mileage')
    cars_df['mileage'] = cars_df['mileage'].replace(['N/A', 'Not available'], np.nan)
    cars_df['mileage'] = cars_df['mileage'].apply(lambda x: float(x.replace(',', '')) if isinstance(x, str) else x)
    cars_df['mileage'] = cars_df['mileage'].fillna(0)
    cars_df['mileage'] = cars_df.groupby('year')['mileage'].transform(lambda x: x.fillna(x.mean()))
    return cars_df

def get_col_unique_values(df):
    """
    log_events unique values for each column in the DataFrame.

    Args:
    df (DataFrame): The DataFrame to be processed.
    """
    log_event('Getting unique columns')
    for column in df:
        log_event("---- %s ---" % column)
        log_event(df[column].unique())

def save_data_to_csv(data):
    """
    Saves the DataFrame to a CSV file.

    Args:
    data (DataFrame): The DataFrame to be saved.
    """
    log_event('Saving data to CSV')
    now = datetime.now()
    now_str = now.strftime('%Y%m%d_%H%M%S')
    filename = f'./cars_data/cars_{now_str}.csv'
    data.to_csv(filename, index=False)

def get_cars_pipeline(link):
    """
    Complete pipeline for extracting, processing, and saving car data.

    Args:
    link (str): The URL to scrape the car data from.

    Returns:
    dict: A dictionary of processed car data if successful, None if an error occurs.
    """
    log_event('Starting pipeline')
    log_event({'url - get_cars_pipeline': link})
    try:
        soup = get_soup(link)
        cars_json = get_cars_data(soup)

        # Check if 'car_ids' exists and has data
        if not cars_json.get('birf', {}).get('pageData', {}).get('page', {}).get('vehicle', {}).get('car_ids', []):
            log_event(f"No more data to process for link: {link}")
            return None
        
        cars_ids = cars_json['birf']['pageData']['page']['vehicle']['car_ids']
        if not cars_ids:
            log_event("Reached the end of records.")
            return None

        cars_ids = cars_json['birf']['pageData']['page']['vehicle']['car_ids']
        cars_data = get_cars_dataframe(cars_json, cars_ids)
        cars_data = replace_na_mileage(cars_data)
        cars_data = cars_data[cars_data['price'] != 0]
        cars_data = cars_data.sort_values('price', ascending=True)
        save_data_to_csv(cars_data)
        cars_final_data = cars_data.to_dict(orient='records')
        time.sleep(1)
        log_event('Ending pipeline')
        log_event({'cars pipeline return': cars_final_data})
        return cars_final_data
    
    except Exception as e:
        log_event(f"Error occurred while processing link: {link}")
        log_event(f"Error details: {str(e)}")
        return None

def process_links(links):
    num_records = 25
    for link in links:
        for batch in range(0, 1001, num_records):
            if batch == 0:
                modified_link = link + f'&newSearch=true&numRecords={num_records}&firstRecord={batch}'
                result = get_cars_pipeline(link)
            
            modified_link = link + f'&newSearch=false&numRecords={num_records}&firstRecord={batch}'

            try:
                result = get_cars_pipeline(modified_link)
                if not result:  # Assuming get_cars_pipeline returns None or an empty dict when no data
                    log_event(f"No more data to process or error occurred for link: {link}. Moving to the next link.")
                    break  # Exit the batch loop, move to the next link
                # Optional: Implement a wait time for pacing requests
                time.sleep(2)  # Example: Wait 2 seconds before the next request
            except Exception as e:
                log_event(f"Error occurred while processing link: {link}")
                log_event(f"Error details: {e}")
                break  # On error, immediately proceed to the next link

#The number of records is still not correct - FIX ME
links = [
    'https://www.autotrader.com/cars-for-sale/all-cars/mitsubishi/lancer-evolution/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/nissan/gt-r/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/toyota/supra/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/honda/s2000/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/subaru/wrx/sti/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/bmw/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/land-rover/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/acura/nsx/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/bugatti/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/alfa-romeo/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/bentley/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/ferrari/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/audi/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/mitsubishi/lancer-evolution/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/all-cars/maserati/denver-nc?searchRadius=0&zip=28037'
    'https://www.autotrader.com/cars-for-sale/all-cars/dodge/viper/denver-nc?searchRadius=0&zip=28037',
    'https://www.autotrader.com/cars-for-sale/porsche/denver-nc?searchRadius=0&zip=28037'

    
]

process_links(links)
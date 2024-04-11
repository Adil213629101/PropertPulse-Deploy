import os
from datetime import datetime
import json


def extract_property_details(data):
    details = {}

    details['property_id'] = data.get('property_id', '')
    details['list_price'] = data.get('list_price', '')
    details['status'] = data.get('status', '')
    details['listing_id'] = data.get('listing_id', '')
    details['permalink'] = "https://www.realtor.com/realestateandhomes-detail/"+ data.get('permalink', '')

    primary_photo = data.get('primary_photo')
    if primary_photo is not None:
        details['primary_photo'] = primary_photo.get('href', '')
    else:
        details['primary_photo'] = ''
    description = data.get('description', {})
    details['description'] = {
        'beds': description.get('beds', '0'),
        'baths': description.get('baths_consolidated', ''),
        'sqft': description.get('sqft', ''),
        'lot_sqft': description.get('lot_sqft', ''),
        'type': description.get('type', ''),
        'sold_price': description.get('sold_price', ''),
        'sold_date': description.get('sold_date', '')
    }

    details['location'] = data.get('location', {})

    flags = data.get('flags', {})
    details['flags'] = {
        'is_coming_soon': flags.get('is_coming_soon', False),
        'is_new_listing': flags.get('is_new_listing', False),
        'is_price_reduced': flags.get('is_price_reduced', False),
        'is_foreclosure': flags.get('is_foreclosure', False),
        'is_new_construction': flags.get('is_new_construction', False),
        'is_pending': flags.get('is_pending', False),
        'is_contingent': flags.get('is_contingent', False)
    }

    date_input = data.get('list_date', '')
    formatted_date = datetime.strptime(
        date_input, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
    details['list_date'] = formatted_date
    return details


def save_list_to_json(data_list, filename):
    try:
        with open(filename, 'w') as json_file:
            json.dump(data_list, json_file, indent=4)
        print("List saved to", filename)
    except Exception as e:
        print("An error occurred while saving the list to JSON:", str(e))


def append_list_to_json_file(data_list, filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            existing_data = json.load(file)
        existing_data.extend(data_list)
        with open(filename, 'w') as file:
            json.dump(existing_data, file, indent=4)
    else:
        with open(filename, 'w') as file:
            json.dump(data_list, file, indent=4)

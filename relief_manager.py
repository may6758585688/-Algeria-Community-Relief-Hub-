import csv
import os
import requests

def update_or_add_resource(city_name, item_name, category, quantity, urgency):
    """
    Updates an existing resource or adds a new one to the CSV database.
    Automatically flags items as 'Resolved' if quantity drops to 0.
    """
    rows = []
    file_exists = os.path.exists('resources.csv')
    updated = False

    if quantity == 0:
        urgency = "Resolved"

    if file_exists:
        with open('resources.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['City'] == city_name and row['Item'] == item_name:
                    row['Quantity'] = str(quantity)
                    row['Urgency'] = urgency
                    updated = True
                rows.append(row)

    if not updated:
        rows.append({
            'City': city_name,
            'Item': item_name,
            'Category': category,
            'Quantity': str(quantity),
            'Urgency': urgency
        })

    with open('resources.csv', mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['City', 'Item', 'Category', 'Quantity', 'Urgency']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def check_real_wildfire_risks():
    """
    Queries the Open-Meteo API with real geographic coordinates for high-risk 
    regions in Algeria to monitor live temperatures and auto-dispatch emergency resources.
    """
    # Dictionary mapping high-risk Algerian cities to their GPS coordinates
    target_regions = {
        "Annaba": {"lat": 36.9, "lon": 7.7},
        "Bejaia": {"lat": 36.75, "lon": 5.08},
        "Tizi Ouzou": {"lat": 36.71, "lon": 4.04},
        "Chlef": {"lat": 36.16, "lon": 1.33}
    }

    print("Scanning live meteorological data across high-risk Algerian regions...")

    for city, coords in target_regions.items():
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m"
        
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                current_temp = data.get("current", {}).get("temperature_2m", 0)
                
                print(f"-> {city}: Current temperature is {current_temp}°C")
                
                # If the temperature hits a dangerous threshold (e.g., > 35°C indicating high wildfire risk)
                if current_temp > 35:
                    print(f"⚠️ Critical heat threshold reached in {city}! Auto-dispatching emergency supplies.")
                    update_or_add_resource(city, "Firefighting & Medical Kits", "Emergency", 100, "Critical")
                else:
                    print(f"   {city}: Conditions stable.")
            else:
                print(f"Failed to fetch data for {city}.")
        except Exception as error:
            print(f"Error connecting to API for {city}: {error}")

if __name__ == "__main__":
    check_real_wildfire_risks()

import csv
import os

def update_or_add_resource(city_name, item, category, quantity, urgency="High"):
    rows = []
    file_exists = os.path.exists('resources.csv')
    updated = False
    
    # If quantity drops to 0, automatically mark it as Resolved
    if quantity == 0:
        urgency = "Resolved"

    if file_exists:
        with open('resources.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                # If the city and item match, update its quantity and urgency
                if row['city'].lower() == city_name.lower() and row['item_name'].lower() == item.lower():
                    row['quantity_needed'] = str(quantity)
                    row['urgency_level'] = urgency
                    updated = True
                rows.append(row)
                
    # If the city/item didn't exist yet, add it as a new entry
    if not updated:
        new_row = {
            'city': city_name,
            'item_name': item,
            'category': category,
            'quantity_needed': str(quantity),
            'urgency_level': urgency
        }
        rows.append(new_row)
        fieldnames = ['city', 'item_name', 'category', 'quantity_needed', 'urgency_level']

    # Rewrite the CSV file cleanly
    with open('resources.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    if quantity == 0:
        print(f"Notice: Need for {item} in {city_name} has been fully met and marked as Resolved.")
    else:
        print(f"Successfully updated {city_name}: {quantity} units of {item} (Urgency: {urgency}).")

# --- EXAMPLES OF USAGE ---

# 1. Update Annaba as needs change (e.g., dropping down to 6 units)
update_or_add_resource("Annaba", "Underwear", "Supplies", 6, "Critical")

# 2. Update when the need is completely met (drops to 0 -> automatically becomes "Resolved")
update_or_add_resource("Annaba", "Underwear", "Supplies", 0)

# 3. Add a brand new city dynamically on the fly
update_or_add_resource("Guelma", "Bottled Water", "Hydration", 500, "High")

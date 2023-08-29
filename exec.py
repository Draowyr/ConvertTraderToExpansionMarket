import os
import json
import shutil

current_directory = os.path.dirname(__file__)
file_path = os.path.join(current_directory, "trader.txt")

# Asks the user for the name of the mod
mod_name = input("Enter the name of the mod : ")
mod_name = mod_name.strip()

# Asks the user if they want to add the name of the mod to the DisplayName
add_mod_name = input("Do you want to add the mod name to the DisplayName (yes/no) : ").lower()
if add_mod_name == "yes":
    add_mod_name = True
else:
    add_mod_name = False

# Transformation of the mod name for use in file names
mod_name_title_case = mod_name.title().replace(" ", "")
output_folder = os.path.join(current_directory, "output", mod_name_title_case)

# Deletes the output folder if it already exists
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)

# Create the output folder
os.makedirs(output_folder)

# Function to generate the JSON file
def generate_json(category, items):
    display_name = category.replace(" ", "")
    if add_mod_name:
        display_name = f"{mod_name} - {display_name}"
    json_data = {
        "m_Version": 12,
        "DisplayName": display_name,
        "Icon": "Deliver",
        "Color": "FBFCFEFF",
        "IsExchange": 0,
        "InitStockPercent": 75,
        "Items": items
    }
    
    category_name = category.replace(" ", "").title()
    output_file_path = os.path.join(output_folder, f"{mod_name_title_case}_{category_name}.json")
    with open(output_file_path, "w") as output_file:
        json.dump(json_data, output_file, indent=2)

# Reading and converting data
current_category = None
items = []

with open(file_path, "r") as file:
    for line in file:
        line = line.strip()
        if line.startswith("<Category>"):
            if current_category and items:
                generate_json(current_category, items)
            current_category = line.replace("<Category>", "").strip()
            items = []
        else:
            parts = line.split(",")
            if len(parts) == 4:
                class_name, _, max_price, min_price = parts
                if int(max_price) == -1:
                    max_price = min_price
                items.append({
                    "ClassName": class_name,
                    "MaxPriceThreshold": int(max_price),
                    "MinPriceThreshold": int(max_price),
                    "SellPricePercent": -1,
                    "MaxStockThreshold": 100,
                    "MinStockThreshold": 1,
                    "QuantityPercent": -1,
                    "SpawnAttachments": [],
                    "Variants": []
                })

# Generate JSON for the last category
if current_category or items:
    if current_category and items:
        generate_json(current_category, items)
    else:
        generate_json("Items", items)

print("Conversion complete. JSON files generated for each category in the output folder.")
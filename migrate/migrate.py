import json

filename = input("Enter the filename (e.g., data.json): ")

try:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        output_data = {key: {"devices": []} for key in data}
        print("Converted list to dictionary.")
    elif isinstance(data, dict):
        output_data = list(data.keys())
        print("Converted dictionary to list.")
    else:
        print("Error: The file contains an unsupported format.")
        exit()

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"File {filename} has been successfully updated.")

except FileNotFoundError:
    print(f"Error: File {filename} not found.")
except json.JSONDecodeError:
    print(f"Error: File {filename} does not contain valid JSON.")
except Exception as e:
    print(f"An error occurred: {e}")

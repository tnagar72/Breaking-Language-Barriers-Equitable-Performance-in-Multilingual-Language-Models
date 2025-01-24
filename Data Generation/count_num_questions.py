import json

json_file_path = "/Users/XXXX/Desktop/XXXX's XXXX XXXX/Five-Fold Cross-Validation/cmi2_train_dev_combined.json"

with open(json_file_path, "r") as file:
        json_list = json.load(file)

print(len(json_list))

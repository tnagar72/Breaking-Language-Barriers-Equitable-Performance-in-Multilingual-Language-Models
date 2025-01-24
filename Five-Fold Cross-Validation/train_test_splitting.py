import numpy as np
from sklearn.model_selection import KFold
import json

# Load CS JSON file
with open("/Users/XXXX/Desktop/XXXX's XXXX XXXX/Five-Fold Cross-Validation/cmi3_train_dev_combined.json") as f:
    data = json.load(f)
# Convert JSON objects to list
json_list = list(data)    

# Load the English JSON file
with open("/Users/XXXX/Desktop/XXXX's XXXX XXXX/Five-Fold Cross-Validation/train_dev_english_combined.json") as f:
    english_data = json.load(f)
# Convert JSON objects to list
json_list_english = list(english_data)   


# Load the Hindi JSON file    
with open("/Users/XXXX/Desktop/XXXX's XXXX XXXX/Five-Fold Cross-Validation/train_dev_hindi_combined.json") as f:
    hindi_data = json.load(f)
# Convert JSON objects to list
json_list_hindi = list(hindi_data)

# Convert data to an array of indices
indices = np.arange(len(json_list))

# Initialize KFold with 5 splits
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Split the data
for fold, (train_index, test_index) in enumerate(kf.split(indices)):
    train_data = [data[i] for i in train_index]
    test_data = [data[i] for i in test_index]
    test_data_english = [english_data[i] for i in test_index]
    test_data_hindi = [hindi_data[i] for i in test_index]
    print(f"Fold {fold + 1}")
    # Open a new JSON file for train data
    train_file = f"train_data_fold_{fold + 1}.json"
    with open(train_file, 'w') as train_f:
        json.dump(train_data, train_f, indent=2, ensure_ascii=False)
    print(f"Train Data {fold + 1} saved to {train_file}")
    # Open a new JSON file for test data
    test_file = f"test_data_fold_{fold + 1}.json"
    with open(test_file, 'w') as test_f:
        json.dump(test_data, test_f, indent=2, ensure_ascii=False)
    print(f"Test Data {fold + 1} saved to {test_file}")

    # Open a new JSON file for test data (English)
    test_file_english = f"test_data_fold_{fold + 1}_english.json"
    with open(test_file_english, 'w') as test_f:
        json.dump(test_data_english, test_f, indent=2, ensure_ascii=False)

    # Open a new JSON file for test data (Hindi)
    test_file_hindi = f"test_data_fold_{fold + 1}_hindi.json"
    with open(test_file_hindi, 'w') as test_f:
        json.dump(test_data_hindi, test_f, indent=2, ensure_ascii=False)
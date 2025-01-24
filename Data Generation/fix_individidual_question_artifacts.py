import os
import traceback
from openai import OpenAI
import lang_detect
import hinglishTest
import json
import All_Questions_through_GPT

from lingua import Language, LanguageDetectorBuilder
from tqdm import tqdm
import logging

languages = [Language.ENGLISH, Language.HINDI]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

# Set up logging
logging.basicConfig(filename='logger.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Log a message
logging.info('Logging system initialized')

# Create a specific logger for the OpenAI library
openai_logger = logging.getLogger('openai')
openai_logger.setLevel(logging.WARNING)
openai_logger.propagate = False

# # Log an error
# logging.error('An error occurred')

# # Log a warning
# logging.warning('This is a warning')

# Load the API key from the environment variable
# XXXX-6 = os.getenv('OPENAI_API_KEY_GPT3.5').strip()
XXXX-6 = '--READACTED API KEY--'

if XXXX-6 is None:
    raise ValueError("API key not found. Make sure the environment variable OPENAI_default_proj is set correctly.")

client = OpenAI(XXXX-6=XXXX-6)
logging.info('OpenAI client initialized')

prompt = "Please convert this question into Hinglish (code-mixed) with Devanagari script for Hindi: {}"

def print_eachQ(json_dict: dict, counter: int):
    return json_dict["question"]['stem']

#Cycling through all the questions
json_file_path = "test modified_dev_rand_split copy 2.json"
json_file_path_1 = "modified_train_rand_split copy.json"
json_file_path_2 = "modified_dev_rand_split copy.json"
json_file_path_3 = "modified_test_rand_split_no_answers copy.json"
counter = 0

for json_file_path in tqdm([json_file_path, json_file_path_2, json_file_path_3, json_file_path_1]):
    counter = 0
    # Open the JSON file
    with open(json_file_path) as f:
        # Read the contents of the file
        data = json.load(f)

    logging.info("Loaded {} questions from {} file".format(len(data),json_file_path))
    logging.info("Processing questions...")

    # Iterate through the list of JSON objects
    for json_obj in tqdm(data):
        # Access the question field in each object
        try:
            prettified_json = All_Questions_through_GPT.prettify_json(json.dumps(json_obj))
            question= print_eachQ(prettified_json, 5)
            confidence_values = detector.compute_language_confidence_values(question)
            if not lang_detect.is_mixed_language(question):
                counter += 1
                hinglish_question = hinglishTest.generate_hinglish_questions(prompt, question)
                json_obj["question"]['stem'] = hinglish_question
            else:
                continue
        except Exception as e:
            print(f"Error occurred: {e}")
            traceback.print_exc()
            continue
            
    logging.info("Processed {counter} questions")
    logging.info("Saving the modified JSON file...")

    # Save the modified JSON file
    output_file_path = "updated_" + json_file_path
    with open(output_file_path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
import json
import traceback

import os
from openai import OpenAI
import tqdm

# Load the API key from the environment variable
# print(os.getenv('OPENAI_API_KEY'))
XXXX-6 = os.getenv('OPENAI_API_KEY_GPT3.5')

if XXXX-6 is None:
    raise ValueError("API key not found. Make sure the environment variable OPENAI_default_proj is set correctly.")

client = OpenAI(XXXX-6=XXXX-6)

prompt3 = """
**Review the Examples below**: Understand how Hinglish combines Hindi (in Devanagari script) and English (in English script).

Examples:
"मेरे घर पर today, एक party है। Do you think कि तुम अपने friends के साथ आ सकते हो?"
"Also, तान्या को भी लेते आना। खाने as in dinner में 2 सब्जी, naan, दाल और rice हैं."
"Sweets में हम ice-cream और गुलाबजामुन खा सकते हैं। मेरे कुछ American दोस्त भी आएंगे।"
"I hope that's fine with you. There will be music and दारू, बहुत मजा आएगा और हम खूब enjoy करेंगे।"

Task Instructions:
1. **Transform into Hinglish**: Convert the given English questions into Hinglish, ensuring each sentence contains at least 60% English in it. Do not simply translate the English into Hindi but try to blend both languages naturally within same sentences. 
2. **Maintain Clarity**: Ensure that the sentences are clear, maintain the original meaning, and use a mix of both languages (English and Hindi).
3. **Note**: Keep the answer choices in English. Make sure that the question ID for each question is maintained.

Here are more examples to demonstrate what steps 1-3 require you to do:

English Question: "What is the capital of India?"
ID: 075e483d21c29a511267ef62bedc0461
Answer Choices: A) Mumbai, B) Delhi, C) Kolkata **Example

Hinglish Output: "What is India की capital?"
ID: 075e483d21c29a511267ef62bedc0461
Answer Choices: A) Mumbai, B) Delhi, C) Kolkata


English Question: "Do you know the way home?"
ID: 02e821a3e53cb320790950aab4489e85
Answer Choices: A) yes, B) no

Hinglish Output: "Do you know घर का रास्ता ?"
ID: 02e821a3e53cb320790950aab4489e85
Answer Choices: A) yes, B) no


English Question: “What is a student about to do if they are sitting in front of a number of black and white keys?”
ID: 4c1cb0e95b99f72d55c068ba0255c54d
Answer Choices: A) Talk, B) Read book, C) Play piano, D) Study book, E) Study engineering

Hinglish Output: "Student क्या करने वाला है अगर उनके सामने कई black और white keys हैं?"
ID: 4c1cb0e95b99f72d55c068ba0255c54d
Answer Choices: A) Talk, B) Read book, C) Play piano, D) Study book, E) Study engineering


English Question: "Sarah filled the thing with peanuts. What did she fill with peanuts?"
ID: e8a8b3a2061aa0e6d7c6b522e9612824
Answer Choices: A) Ballpark, B) Box, C) Container, D) Carnival, E) Jar

Hinglish Output: "Sarah ने उस चीज़ को peanuts से भर दिया। उसने क्या peanuts से भरा?"
ID: e8a8b3a2061aa0e6d7c6b522e9612824
Answer Choices: A) Ballpark, B) Box, C) Container, D) Carnival, E) Jar


English Question: "What's the current weather condition in Arizona?"
ID: 86c59f14af97b33ec13edc6ec4389e31
Answer Choices: A) Humid, B) Hot, C) Rainy, D) Stormy, E) Cloudly

Hinglish Output: "Arizona में current मौसम का हाल क्या है?"
ID: 86c59f14af97b33ec13edc6ec4389e31
Answer Choices: A) Humid, B) Hot, C) Rainy, D) Stormy, E) Cloudly

Replicate the above mentioned task for the Questions below:

{}
"""

prompt3_only_questions = """
**Review the Examples below**: Understand how Hinglish combines Hindi (in Devanagari script) and English (in English script).

Examples:
"मेरे घर पर today, एक party है। Do you think कि तुम अपने friends के साथ आ सकते हो?"
"Also, तान्या को भी लेते आना। खाने as in dinner में 2 सब्जी, naan, दाल और rice हैं."
"Sweets में हम ice-cream और गुलाबजामुन खा सकते हैं। मेरे कुछ American दोस्त भी आएंगे।"
"I hope that's fine with you. There will be music and दारू, बहुत मजा आएगा और हम खूब enjoy करेंगे।"

Task Instructions:
1. **Transform into Hinglish**: Convert the given English questions into Hinglish, ensuring each sentence contains at least 60% English in it. Do not simply translate the English into Hindi but try to blend both languages naturally within same sentences. 
2. **Maintain Clarity**: Ensure that the sentences are clear, maintain the original meaning, and use a mix of both languages (English and Hindi).
3. **Note**: Keep the answer choices in English. Make sure that the question ID for each question is maintained.

Here are more examples to demonstrate what steps 1-3 require you to do:

English Question: "What is the capital of India?"
ID: 075e483d21c29a511267ef62bedc0461
Answer Choices: A) Mumbai, B) Delhi, C) Kolkata

Hinglish Output: "What is India की capital?"
ID: 075e483d21c29a511267ef62bedc0461


English Question: "Do you know the way home?"
ID: 02e821a3e53cb320790950aab4489e85
Answer Choices: A) yes, B) no

Hinglish Output: "Do you know घर का रास्ता ?"
ID: 02e821a3e53cb320790950aab4489e85


English Question: “What is a student about to do if they are sitting in front of a number of black and white keys?”
ID: 4c1cb0e95b99f72d55c068ba0255c54d
Answer Choices: A) Talk, B) Read book, C) Play piano, D) Study book, E) Study engineering

Hinglish Output: "Student क्या करने वाला है अगर उनके सामने कई black और white keys हैं?"
ID: 4c1cb0e95b99f72d55c068ba0255c54d


English Question: "Sarah filled the thing with peanuts. What did she fill with peanuts?"
ID: e8a8b3a2061aa0e6d7c6b522e9612824
Answer Choices: A) Ballpark, B) Box, C) Container, D) Carnival, E) Jar

Hinglish Output: "Sarah ने उस चीज़ को peanuts से भर दिया। उसने क्या peanuts से भरा?"
ID: e8a8b3a2061aa0e6d7c6b522e9612824


English Question: "What's the current weather condition in Arizona?"
ID: 86c59f14af97b33ec13edc6ec4389e31
Answer Choices: A) Humid, B) Hot, C) Rainy, D) Stormy, E) Cloudly

Hinglish Output: "Arizona में current मौसम का हाल क्या है?"
ID: 86c59f14af97b33ec13edc6ec4389e31

Replicate the above mentioned task for the Questions below:
{}
"""

# Function to call the API and process the response
def generate_hinglish_questions(prompt, questions):
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a compound bilingual speaker who reads and understand both English and Hindi. You can also effectively code-switch English and Hindi and use them in the same sentence."},
        {"role": "user", "content": str.format(prompt3, questions)}
    ],
    temperature=1,
    # max_tokens=1000, 
    top_p=1)

    return response.choices[0].message.content

Num_Questions = 9741
Num_Partitions = 265
Num_Questions_in_Partition = 9741 // 265

def prettify_json(json_str):
    try:
        json_dict = json.loads(json_str)
        return json_dict
    except json.JSONDecodeError:
        raise Exception("Invalid JSON format")
    
def print_eachQ(json_dict: dict, counter: int):
    output = ""
    output += str.format("Question {}: ", counter) + json_dict["question"]['stem'] + "\n"
    output += str.format("ID: {}", json_dict['id']) + "\n\n"
    for label in json_dict['question']["choices"]:
        output += label['label'] + ": " + label['text'] + "\n"
    output += "\n"
    return output

i = 0
counter = 1

if __name__ == "__main__":
    # Your code here
    with open("/Users/XXXX/Desktop/XXXX's XXXX XXXX/Chat-GPT CS Text Synthesis/test_rand_split_no_answers.jsonl", "r") as file:
        json_list = json.load(file)

    print("file opened")

    partitioned_questions_output = ""

    for json_obj in tqdm.tqdm(json_list):
        try:
            prettified_json = prettify_json(json.dumps(json_obj))
            partitioned_questions_output += print_eachQ(prettified_json, counter)
            counter += 1
            i = i + 1

            if i == Num_Questions_in_Partition:
                i = 0
                print("parition Done")
                print("API call sent")
                cs_question_output = generate_hinglish_questions(prompt3_only_questions, partitioned_questions_output)
                print(str.format(prompt3, partitioned_questions_output))
                print("API call returned. Writing to file")
                with open("/Users/XXXX/Desktop/XXXX's XXXX XXXX/Chat-GPT CS Text Synthesis/CSEngQuestionsAll(test).txt", "a") as file:
                    file.write(cs_question_output)
                partitioned_questions_output = ""
                print("Written to file. Reached Question: " + str(counter))

        except Exception as e:
            print(f"Error occurred: {e}")
            traceback.print_exc()

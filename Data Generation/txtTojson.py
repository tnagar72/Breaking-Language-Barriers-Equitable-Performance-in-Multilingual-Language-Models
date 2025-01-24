import json
import re
import traceback

def txt_to_json(txt_file):
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    questions = []
    current_question = None
    question_flag = False
    id_flag = False
    Answer_Choice_Flag = False
    
    for line in lines:
        line = line.strip()

        # Check if line starts with 'Question' or 'question'
        if line.startswith(('Question', 'question')):
            try:
                questions.append(current_question)
                # re-initialize the current question
                current_question = {'question': '', 'id': '', 'Answer Choices': ''}
                current_question['question'] = line.split(':', 1)[1].strip('"')
                question_flag = True
                id_flag = False
                Answer_Choice_Flag = False
            except Exception as e:
                print(f"Error processing line: {line}")
                print(f"Error message: {str(e)}")
                traceback.print_exc()  # Print the traceback
        elif line.strip() == '':
            continue
        elif line.startswith(('ID:','id:')):
            question_flag = False
            Answer_Choice_Flag = False
            id_flag = True
            try:
                current_question['id'] = line.split(':', 1)[1].strip()
            except Exception as e:
                print(f"Error processing line: {line}")
                print(f"Error message: {str(e)}")

        elif line.startswith(('Answer Choices:', 'answer choices:', "A:", "A)")):
            question_flag = False
            id_flag = False
            Answer_Choice_Flag = True
            current_question['Answer Choices'] += line
        elif question_flag:
            current_question['question'] += line
        elif id_flag:
            try:
                current_question['id'] += line
            except Exception as e:
                
                print(f"Error processing line: {line}")
                print(f"Error message: {str(e)}")
                traceback.print_exc()  # Print the traceback
        elif Answer_Choice_Flag:
            current_question['Answer Choices'] += line
        else:
            print("How did we get here?")
            print(line)
    
    # Add the last question to the list
    if current_question:
        questions.append(current_question)
    
    # Write to JSON file
    with open('questions(test).json', 'w', encoding='utf-8') as json_file:
        json.dump(questions, json_file, ensure_ascii=False, indent=4)

# Define the input file
txt_file = 'fixed_fixed_CSEngQuestionsAll(test) copy.txt'

# Convert the text file to JSON
txt_to_json(txt_file)
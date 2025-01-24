from tqdm import tqdm
from lingua import Language, LanguageDetectorBuilder

languages = [Language.ENGLISH, Language.HINDI]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

def fix_question_spacing(file_path):
    # Reading the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Removing asterisks
    content = content.replace('**', '').replace('*', '')

    # Writing cleaned content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    # Reading the file again after cleaning
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    fixed_lines = []
    for line in tqdm(lines, desc="Processing lines", unit="line"):
        if line.strip():  # Ignore empty lines
            fixed_lines.append(line.strip())
    
    formatted_lines = []
    for line in tqdm(fixed_lines, desc="Formatting lines", unit="line"):
        if line.startswith('Question'):
            
            formatted_lines.append('\n' + line)
        elif line.startswith("Hinglish Output"):
            formatted_lines.append(line.replace('Hinglish Output', 'Question'))
        elif ('Question' in line or "Hinglish Output" in line):
            if 'Question' in line:
                question, rest = line.split('Question', 1)
                formatted_lines.append(question)
                rest = rest.strip()
                formatted_lines.append('\n' + 'Question ' + rest)
            if 'Hinglish Output' in line:
                question, rest = line.split('Hinglish Output', 1)
                formatted_lines.append(question)
                rest = rest.strip()
                formatted_lines.append('\n' + 'Question ' + rest)
        else:
            formatted_lines.append(line)

    # Removing 'Hinglish' and avoiding duplicate empty lines
    cleaned_lines = []
    for line in tqdm(formatted_lines, desc="Cleaning lines", unit="line"):
        line = line.replace('Hinglish', '')
        cleaned_lines.append(line)
        if line.strip() == '' and cleaned_lines[-1].strip() == '':  # Ignore consecutive empty lines
            cleaned_lines.pop()

    # Writing the final formatted content to a new file
    with open('fixed_' + file_path, 'w', encoding='utf-8') as file:
        for line in tqdm(cleaned_lines, desc="Writing to file", unit="line"):
            file.write(line + '\n')

# Replace 'your_file.txt' with the path to your file
fix_question_spacing('fixed_CSEngQuestionsAll(test) copy.txt')
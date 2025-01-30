# Breaking Language Barriers: Equitable Performance in Multilingual Language Models

ACL Anonymous Review Repo for the paper `Breaking Language Barriers: Equitable Performance in Multilingual Language Models

[GPT-3.5 Prompt Structure](GPT-3.5%20Prompt%20Structure.md) | [Requirements.txt](requirements.txt) python packages for Data Generation and Fine-Tuning | [Datasets](#Datasets) | [Data Generation](#Data%20Generation) | [Processing and Additional Functionality](###Processing%20and%20Additional%20Functionality) | [Testing and Translation scripts](#Testing%20and%20Translation%20scripts)
### Repo Structure:

```
Breaking-Language-Barriers-Equitable-Performance-in-Multilingual-Language-Models/
├── Data Generation/                               # Folder for scripts and info related to data generation
│   ├── All_Questions_through_GPT.py               # Script to generate all questions using GPT-based code-switching
│   ├── CMI Dataset Info.md                        # Information about the CMI-based datasets and their properties
│   ├── count_num_questions.py                     # Script to count the number of questions in each dataset
│   ├── fix_individual_question_artifacts.py       # Script to fix any artifacts in individual code-switched questions
│   ├── fix_question_spacing.py                    # Script to correct spacing issues in the questions
│   ├── translator.py                              # Script to translate questions into Hindi for fine-tuned model eval
│   ├── txtToJson.py                               # Script to convert question datasets from .txt to .json format
│
├── Datasets/                                      # Folder containing the datasets used for fine-tuning
│   ├── CMI 1/                                     # Low-level code-mixed dataset
│   ├── CMI 2/                                     # Medium-level code-mixed dataset
│   ├── CMI 3/                                     # High-level code-mixed dataset
│   ├── GPTgen/                                    # GPT-3.5 generated code-switched dataset
│
├── Five-Fold Cross-Validation/                    # Folder for cross-validation testing
│   ├── cmi3_train_dev_combined.json               # Combined train/dev dataset for CMI 3
│   ├── GPTgen_train_dev_combined.json             # Combined train/dev dataset for GPTgen
│   ├── train_dev_english_combined.json            # Combined train/dev dataset for English
│   ├── train_dev_hindi_combined.json              # Combined train/dev dataset for Hindi
│   ├── train_test_splitting.py                    # Script to split data for training/testing
│
├── GPT-3.5 Prompt Structure.md                    # Markdown file containing the structure of prompts used for GPT-3.5 generation
├── README.md                                      # This README file explaining the project, setup, and usage
├── requirements.txt                               # List of dependencies needed for the project
```

### Datasets

The Datasets folder contains 4 sub-folders:

1. `CMI 1`: contains the dataset with a low level of code-switching between Hindi and English. The mixing ratio is minimal, with mostly Hindi or English dominating each sentence. The Controlled Mixing Index (CMI) is kept between 0% and 16.7%. This dataset helps us evaluate the impact of low levels of code-switching on LLM performance.
2. `CMI 2`: Contains the dataset with a medium level of code-switching, where both languages (Hindi and English) are more evenly mixed, with the CMI set between 16.7% and 30%. This dataset allows us to test how moderate language mixing improves the model’s performance on both HRLs and LRLs.
3. `CMI 3`: This dataset has the highest degree of code-switching, with a nearly equal blend of Hindi and English (CMI between 30% and 50%). The higher level of code-mixing helps us examine the effects of intense language alternation on model performance.
4. `GPTgen`: Contains a dataset generated using GPT-3.5 based on prompts designed to create code-switched text in Hindi and English.

Each sub-folder contains three files: `_dev_rand_split.jsonl`, `_train_rand_split.jsonl`, `_test_rand_split_no_answers.jsonl`. Each file corresponds to a code-switched version of the [CommonSenseQA dataset](https://www.tau-nlp.sites.tau.ac.il/commonsenseqa) ([Talmor et al; 2023](https://arxiv.org/abs/1811.00937)).


### Data Generation

1. `All_Questions_through_GPT.py`: Contains code to call the open-ai API with the prompt and the system role message. The script partitions questions to make sure API requests stay within context window for 3.5, and then appends all responses to a .txt file.
2. `CMI Dataset Info`: Contains information on the code + paper used to generate CMI datasets


### Processing and Additional Functionality

`Data Generation/count_num_questions.py`: Allows user to count number of questions in any file.

 The Open-AI API JSON mode did not give us the expected organization. As a result, we resorted to using the text output. The `Data Generation/fix_question_spacing.py` file allows us to fix question-spacing in case of varying new line spaces between questions. The `Data Generation/fix_individidual_question_artifacts.py` allows the fixing of individual question output formatting problems and contains a number of rule-based methods and code to fix question inputs or possible ad-hoc solutions to organizational problems in the question output.

`Data Generation/txtTojson.py`: allows conversion of text output from the GPT-3.5 API to json format.

### Testing and Translation scripts

To test our fine-tuned models, we use five-fold validation testing.

`*_combined.json` combines all questions generated using each of the four data generation methods into one JSON document for each method. 
`Five-Fold Cross-Validation/train_test_splitting.py`: splits the combined files into five folds, which will be used for model eval based on the commonSenseQA dataset. Uses a set seed to maintain reproducibility.

To evaluate our models, we translate the English questions into Hindi, too, to evaluate and compare performance accuracy for each model across the two languages.

`Data Generation/translator.py`: Allows translation of each question from English to Hindi using the Google Cloud API. Can be used for translation across any two languages.

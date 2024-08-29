import os
import re
from transformers import RagTokenizer, RagSequenceForGeneration, DPRQuestionEncoderTokenizerFast, BartTokenizerFast, pipeline
from autocorrect import Speller
from textblob import TextBlob
from spellchecker import SpellChecker

# Initialize spell checkers
spell = Speller()
spell_checker = SpellChecker()

# Initialize the appropriate tokenizers
dpr_tokenizer = DPRQuestionEncoderTokenizerFast.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
bart_tokenizer = BartTokenizerFast.from_pretrained("facebook/bart-large")
rag_tokenizer = RagTokenizer.from_pretrained("facebook/rag-sequence-nq")

# Initialize the RAG model for text generation
model_name = "facebook/rag-sequence-nq"
model = RagSequenceForGeneration.from_pretrained(model_name)
generator = pipeline("text2text-generation", model=model, tokenizer=rag_tokenizer)

# Load known words from a file
def load_known_words(file_path):
    try:
        with open(file_path, 'r') as file:
            words = file.read().splitlines()
        return set(word.lower() for word in words)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return set()

# Preprocess the word by normalizing and cleaning it
def preprocess_word(word):
    word = word.lower()  # Convert to lowercase
    word = re.sub(r'[^\w\s]', '', word)  # Remove punctuation
    return word

# Correct the word using various techniques
def correct_word(word, known_words, incorrect_letter_counts):
    original_word = preprocess_word(word)
    
    if original_word in known_words:
        return word  # Return as is if the word is already known
    
    # Spell checking with various tools
    spellchecked_word = spell_checker.correction(original_word) or original_word
    autocorrected_word = spell(spellchecked_word)
    blob_corrected_word = str(TextBlob(autocorrected_word).correct())
    
    corrected_word = blob_corrected_word
    
    # Track incorrect letters and their counts
    if corrected_word.lower() != original_word.lower():
        for original_letter, corrected_letter in zip(original_word, corrected_word):
            if original_letter != corrected_letter:
                incorrect_letter_counts[original_letter] = incorrect_letter_counts.get(original_letter, 0) + 1

    # Use RAG model to improve semantic accuracy
    rag_input = f"Correct the following word: {corrected_word}"
    rag_output = generator(rag_input)[0]['generated_text'].strip()
    
    return rag_output or corrected_word

# Read and process words from a text file
def read_words_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            words = re.findall(r'\w+', file.read())  # Extract words using regex
        return words
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []

# Analyze text files in the specified directory
def analyze_text_files(output_dir, known_words):
    incorrect_letter_counts = {}
    
    for filename in os.listdir(output_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(output_dir, filename)
            words = read_words_from_file(file_path)
            print(f"\nProcessing file: {filename}")
            for word in words:
                corrected_word = correct_word(word, known_words, incorrect_letter_counts)
                print(f"Original: {word}, Corrected: {corrected_word}")

    # Print incorrect letters and their counts
    print("\nIncorrect letters and their counts:")
    for letter, count in sorted(incorrect_letter_counts.items()):
        print(f"'{letter}': {count} times")

# Example usage
known_words_file = 'data/words_alpha.txt'  # Replace with the correct path
known_words = load_known_words(known_words_file)
output_dir = 'output/'  # Replace with the correct directory
analyze_text_files(output_dir, known_words)


# import nltk
# from transformers import T5ForConditionalGeneration, T5Tokenizer
# import re
# import warnings

# # Suppress warnings related to transformers and PyTorch
# warnings.filterwarnings("ignore", category=UserWarning)

# # Download NLTK data if not already present
# nltk.download('words')

# # Load known words
# def load_known_words(filename):
#     """Load known words from a text file."""
#     with open(filename, 'r') as file:
#         words = set(file.read().split())
#     return words

# # Define a function to correct the text using NLTK and transformers
# def correct_text(text, tokenizer, model):
#     """Correct the given text using T5 model."""
#     input_text = f"correct this: {text}"
#     inputs = tokenizer.encode(input_text, return_tensors="pt")
#     outputs = model.generate(inputs, max_length=512, num_beams=4, early_stopping=True)
#     corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return corrected_text

# # Initialize T5 tokenizer and model
# tokenizer = T5Tokenizer.from_pretrained("t5-small")
# model = T5ForConditionalGeneration.from_pretrained("t5-small")

# # Load known words
# known_words = load_known_words('data/words_alpha.txt')

# # Define a function to process text lines
# def process_text_line(line):
#     """Process and correct a single line of text."""
#     original_text = line.strip()
    
#     # Use the T5 model for text correction
#     corrected_text = correct_text(original_text, tokenizer, model)
    
#     return original_text, corrected_text

# # Read and process the text file
# text_file = 'output/sample_1.png.txt'
# with open(text_file, 'r') as file:
#     lines = file.readlines()

# for line in lines:
#     original, corrected = process_text_line(line)
#     print(f"Original: {original}\nCorrected: {corrected}\n")

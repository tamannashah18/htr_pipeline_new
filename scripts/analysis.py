# # import os
# # import re
# # from autocorrect import Speller
# # from textblob import TextBlob
# # from spellchecker import SpellChecker

# # # Initialize spell checkers
# # spell = Speller()
# # spell_checker = SpellChecker()

# # # Function to load known words from a file
# # def load_known_words(file_path):
# #     with open(file_path, 'r') as file:
# #         words = file.read().splitlines()
# #     return set(word.lower() for word in words)

# # # Load known words
# # known_words_file = 'data/words_alpha.txt'  # Replace with the path to your known words file
# # known_words = load_known_words(known_words_file)
# # spell_checker.word_frequency.load_words(known_words)

# # # Dictionary to store incorrect letter counts
# # incorrect_letter_counts = {}

# # def preprocess_word(word):
# #     """Normalize and preprocess the word."""
# #     word = word.lower()  # Convert to lowercase
# #     word = re.sub(r'[^\w\s]', '', word)  # Remove punctuation
# #     return word

# # def read_words_from_file(file_path):
# #     with open(file_path, 'r') as file:
# #         words = re.findall(r'\w+', file.read())  # Extract words using regex
# #     return words

# # def correct_word(word):
# #     original_word = preprocess_word(word)
    
# #     # If the word is in the known words set, return it as is
# #     if original_word in known_words:
# #         return word
    
# #     # Use spellchecker
# #     spellchecked_word = spell_checker.candidates(original_word)
# #     if spellchecked_word:
# #         spellchecked_word = spell_checker.candidates(original_word).pop()
# #     else:
# #         spellchecked_word = original_word
    
# #     # Use both autocorrect and TextBlob for additional spell checking
# #     autocorrected_word = spell(spellchecked_word)
# #     blob_corrected_word = str(TextBlob(autocorrected_word).correct())
    
# #     # Use the TextBlob corrected word as final
# #     corrected_word = blob_corrected_word
    
# #     if corrected_word.lower() != original_word.lower():
# #         # Track incorrect letters and their counts
# #         for original_letter, corrected_letter in zip(original_word, corrected_word):
# #             if original_letter != corrected_letter:
# #                 if original_letter in incorrect_letter_counts:
# #                     incorrect_letter_counts[original_letter] += 1
# #                 else:
# #                     incorrect_letter_counts[original_letter] = 1
# #     return corrected_word

# # def analyze_text_files(output_dir):
# #     for filename in os.listdir(output_dir):
# #         if filename.endswith('.txt'):
# #             file_path = os.path.join(output_dir, filename)
# #             words = read_words_from_file(file_path)
# #             print(f"\nProcessing file: {filename}")
# #             for word in words:
# #                 corrected_word = correct_word(word)
# #                 print(f"Original: {word}, Corrected: {corrected_word}")

# #     # Print the incorrect letters and their counts
# #     print("\nIncorrect letters and their counts:")
# #     for incorrect_letter, count in incorrect_letter_counts.items():
# #         print(f"'{incorrect_letter}' incorrect {count} times")

# # # Example usage:
# # output_dir = 'output/'
# # analyze_text_files(output_dir)


# ### access token for hugging face: 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
# import time
# import os
# import re
# from autocorrect import Speller
# from textblob import TextBlob
# from spellchecker import SpellChecker

# # Initialize spell checkers
# spell = Speller()
# spell_checker = SpellChecker()

# # Function to load known words from a file
# def load_known_words(file_path):
#     with open(file_path, 'r') as file:
#         words = file.read().splitlines()
#     return set(word.lower() for word in words)

# # Load known words
# known_words_file = 'data/words_alpha.txt'  # Replace with the path to your known words file
# known_words = load_known_words(known_words_file)
# spell_checker.word_frequency.load_words(known_words)

# # Dictionary to store incorrect letter counts
# incorrect_letter_counts = {}

# def preprocess_word(word):
#     """Normalize and preprocess the word."""
#     word = word.lower()  # Convert to lowercase
#     word = re.sub(r'[^\w\s]', '', word)  # Remove punctuation
#     return word

# def read_words_from_file(file_path):
#     with open(file_path, 'r') as file:
#         words = re.findall(r'\w+', file.read())  # Extract words using regex
#     return words

# def correct_word(word):
#     original_word = preprocess_word(word)
    
#     # If the word is in the known words set, return it as is
#     if original_word in known_words:
#         return word
    
#     # Use spellchecker
#     spellchecked_word = spell_checker.candidates(original_word)
#     if spellchecked_word:
#         spellchecked_word = spell_checker.candidates(original_word).pop()
#     else:
#         spellchecked_word = original_word
    
#     # Use both autocorrect and TextBlob for additional spell checking
#     autocorrected_word = spell(spellchecked_word)
#     blob_corrected_word = str(TextBlob(autocorrected_word).correct())
    
#     # Use the TextBlob corrected word as final
#     corrected_word = blob_corrected_word
    
#     if corrected_word.lower() != original_word.lower():
#         # Track incorrect letters and their counts
#         for original_letter, corrected_letter in zip(original_word, corrected_word):
#             if original_letter != corrected_letter:
#                 if original_letter in incorrect_letter_counts:
#                     incorrect_letter_counts[original_letter] += 1
#                 else:
#                     incorrect_letter_counts[original_letter] = 1
#     return corrected_word

# def analyze_text_files(output_dir):
#     for filename in os.listdir(output_dir):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(output_dir, filename)
#             words = read_words_from_file(file_path)
#             print(f"\nProcessing file: {filename}")
#             for word in words:
#                 corrected_word = correct_word(word)
#                 print(f"Original: {word}, Corrected: {corrected_word}")

#     # Print the incorrect letters and their counts
#     print("\nIncorrect letters and their counts:")
#     for incorrect_letter, count in incorrect_letter_counts.items():
#         print(f"'{incorrect_letter}' incorrect {count} times")

# # Example usage:
# output_dir = 'output/'
# analyze_text_files(output_dir)
import nltk
from transformers import T5ForConditionalGeneration, T5Tokenizer
import re
import warnings

# Suppress warnings related to transformers and PyTorch
warnings.filterwarnings("ignore", category=UserWarning)

# Download NLTK data if not already present
nltk.download('words')

# Load known words
def load_known_words(filename):
    """Load known words from a text file."""
    with open(filename, 'r') as file:
        words = set(file.read().split())
    return words

# Define a function to correct the text using NLTK and transformers
def correct_text(text, tokenizer, model):
    """Correct the given text using T5 model."""
    input_text = f"correct this: {text}"
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(inputs, max_length=512, num_beams=4, early_stopping=True)
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected_text

# Initialize T5 tokenizer and model
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Load known words
known_words = load_known_words('data/words_alpha.txt')

# Define a function to process text lines
def process_text_line(line):
    """Process and correct a single line of text."""
    original_text = line.strip()
    
    # Use the T5 model for text correction
    corrected_text = correct_text(original_text, tokenizer, model)
    
    return original_text, corrected_text

# Read and process the text file
text_file = 'output/sample_1.png.txt'
with open(text_file, 'r') as file:
    lines = file.readlines()

for line in lines:
    original, corrected = process_text_line(line)
    print(f"Original: {original}\nCorrected: {corrected}\n")

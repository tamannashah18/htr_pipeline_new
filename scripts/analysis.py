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
# import difflib
# from typing import List, Dict, Set
# from collections import Counter
# from transformers import pipeline
# from autocorrect import Speller
# from textblob import TextBlob
# from spellchecker import SpellChecker

# # Initialize components
# spell = Speller()
# spell_checker = SpellChecker()
# HF_TOKEN = "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"

# def load_model(model_name: str):
#     """Load a Hugging Face model."""
#     return pipeline("text2text-generation", model=model_name, token=HF_TOKEN)

# def load_known_words(file_path: str) -> Set[str]:
#     """Load known words from a file."""
#     with open(file_path, 'r') as file:
#         return set(word.lower() for word in file.read().splitlines())

# known_words = load_known_words('data/words_alpha.txt')
# spell_checker.word_frequency.load_words(known_words)

# def preprocess_word(word: str) -> str:
#     """Normalize and preprocess the word."""
#     return re.sub(r'[^\w\s]', '', word.lower())

# def read_words_from_file(file_path: str) -> List[str]:
#     """Read words from a file."""
#     with open(file_path, 'r') as file:
#         return re.findall(r'\w+', file.read())

# def correct_word(word: str, incorrect_letter_counts: Counter) -> str:
#     """Correct a single word using multiple methods."""
#     original_word = preprocess_word(word)
    
#     if original_word in known_words:
#         return word
    
#     spellchecked_word = str(spell_checker.correction(original_word))
#     autocorrected_word = spell(spellchecked_word)
    
#     try:
#         blob_corrected_word = str(TextBlob(autocorrected_word).correct())
#     except:
#         blob_corrected_word = autocorrected_word
    
#     corrected_word = blob_corrected_word
    
#     if corrected_word.lower() != original_word:
#         for orig, corr in zip(original_word, corrected_word.lower()):
#             if orig != corr:
#                 incorrect_letter_counts[orig] += 1
    
#     return corrected_word

# def query_hf_api(model, sentence: str) -> str:
#     """Send a query to the Hugging Face API."""
#     try:
#         response = model(sentence)
#         generated_text = response[0]['generated_text']
#         return generated_text.strip()
#     except Exception as e:
#         print(f"Error in Hugging Face API call: {e}")
#         return sentence

# def correct_sentence_with_model(sentence: str, model) -> str:
#     """Correct a sentence using a Hugging Face model."""
#     try:
#         corrected_text = query_hf_api(model, f"Correct the spelling and grammar in this sentence: {sentence}")
#         return corrected_text if corrected_text else sentence
#     except Exception as e:
#         print(f"Error in model correction: {e}")
#         return sentence

# def get_sentence_similarity(sentence1: str, sentence2: str, model) -> float:
#     """Calculate similarity between two sentences."""
#     try:
#         response = model([sentence1, sentence2])
#         similarity = response[0]['score'] if 'score' in response[0] else 0
#     except Exception as e:
#         print(f"Error in similarity calculation: {e}")
#         similarity = 0
    
#     if similarity == 0:
#         # Fallback to a simple ratio-based similarity
#         similarity = difflib.SequenceMatcher(None, sentence1, sentence2).ratio()
    
#     return similarity

# def analyze_text_file(file_path: str, correction_model, similarity_model) -> Dict:
#     """Analyze a single text file."""
#     words = read_words_from_file(file_path)
#     original_sentence = ' '.join(words)
    
#     # Model-based correction
#     model_corrected_sentence = correct_sentence_with_model(original_sentence, correction_model)
    
#     # Rule-based word-by-word correction
#     incorrect_letter_counts = Counter()
#     rule_corrected_words = [correct_word(word, incorrect_letter_counts) for word in words]
#     rule_corrected_sentence = ' '.join(rule_corrected_words)
    
#     # Calculate similarities
#     model_similarity = get_sentence_similarity(original_sentence, model_corrected_sentence, similarity_model)
#     rule_similarity = get_sentence_similarity(original_sentence, rule_corrected_sentence, similarity_model)
    
#     # Choose the correction with higher similarity
#     final_correction = model_corrected_sentence if model_similarity > rule_similarity else rule_corrected_sentence
    
#     # Word-level changes
#     word_changes = [(original, corrected) for original, corrected in zip(words, rule_corrected_words) if original != corrected]
    
#     return {
#         "original": original_sentence,
#         "model_corrected": model_corrected_sentence,
#         "rule_corrected": rule_corrected_sentence,
#         "final_correction": final_correction,
#         "model_similarity": model_similarity,
#         "rule_similarity": rule_similarity,
#         "word_changes": word_changes,
#         "incorrect_letters": dict(incorrect_letter_counts)
#     }

# def analyze_text_files(output_dir: str, correction_model_name: str, similarity_model_name: str) -> None:
#     """Analyze all text files in a directory."""
#     correction_model = load_model(correction_model_name)
#     similarity_model = load_model(similarity_model_name)
    
#     all_incorrect_letters = Counter()
    
#     for filename in os.listdir(output_dir):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(output_dir, filename)
#             results = analyze_text_file(file_path, correction_model, similarity_model)
            
#             print(f"\nAnalysis for {filename}:")
#             print(f"Original: {results['original']}")
#             print(f"Model Corrected: {results['model_corrected']}")
#             print(f"Rule Corrected: {results['rule_corrected']}")
#             print(f"Final Correction: {results['final_correction']}")
#             print(f"Model Similarity: {results['model_similarity']:.4f}")
#             print(f"Rule Similarity: {results['rule_similarity']:.4f}")
            
#             print("Word-level changes:")
#             for original, corrected in results['word_changes']:
#                 print(f"  '{original}' -> '{corrected}'")
            
#             all_incorrect_letters.update(results['incorrect_letters'])
    
#     print("\nOverall incorrect letters and their counts:")
#     for letter, count in all_incorrect_letters.most_common():
#         print(f"'{letter}': {count}")

# if __name__ == "__main__":
#     output_dir = 'output/'
#     correction_model_name = "facebook/bart-large-cnn"
#     similarity_model_name = "sentence-transformers/all-MiniLM-L6-v2"
#     analyze_text_files(output_dir, correction_model_name, similarity_model_name)
import requests
import time
API_URL = "https://api-inference.huggingface.co/models/llava-hf/llava-v1.6-mistral-7b-hf"
API_TOKEN = "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"

def query(image_path, prompt):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    # Open the image file
    with open(image_path, "rb") as image_file:
        # Build the payload
        files = {
            "file": image_file
        }
        data = {
            "prompt": prompt
        }
        
        while True:
            response = requests.post(API_URL, headers=headers, files=files, data=data)
            result = response.json()
            
            # Check if the model is still loading
            if "estimated_time" in result:
                print(f"Model is still loading, estimated time: {result['estimated_time']} seconds")
                time.sleep(result['estimated_time'])  # Wait for the estimated time before retrying
            else:
                return result

# Example usage
image_path = "data/images/sample_1.png"
prompt = "Read the content of the image."
output = query(image_path, prompt)
print(output)

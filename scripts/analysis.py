import os
from autocorrect import Speller

# Initialize the spell checker
spell = Speller()

# Dictionary to store incorrect letter counts
incorrect_letter_counts = {}

def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = file.read().split()
    return words

def correct_word(word):
    corrected_word = spell(word)
    if corrected_word != word:
        # Track incorrect letters and their counts
        for original_letter, corrected_letter in zip(word, corrected_word):
            if original_letter != corrected_letter:
                if original_letter in incorrect_letter_counts:
                    incorrect_letter_counts[original_letter] += 1
                else:
                    incorrect_letter_counts[original_letter] = 1
    return corrected_word

def analyze_text_files(output_dir):
    for filename in os.listdir(output_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(output_dir, filename)
            words = read_words_from_file(file_path)
            for word in words:
                correct_word(word)

    # Print the incorrect letters and their counts
    print("Incorrect letters and their counts:")
    for incorrect_letter, count in incorrect_letter_counts.items():
        print(f"'{incorrect_letter}' incorrect {count} times")

# Example usage:
analyze_text_files(output_dir)

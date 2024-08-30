import time
import os
import cv2
import htr_pipeline
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from htr_pipeline import read_page, DetectorConfig, LineClusteringConfig
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# Assuming genai is the correct library
genai.configure(api_key="AIzaSyBPhRoY7S2I35q460jQTcbLVYcxccPB2Go")
# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Dictionaries to store letter counts
incorrect_letter_counts = {}
total_letter_counts = {}

# Initialize Excel file path
excel_file = 'output/letter_incorrect_percentage.xlsx'

def compare_and_track_incorrect_letters(extracted_sentence, corrected_sentence):
    global total_letter_counts

    # Compare letters between the extracted and corrected sentences
    for original_letter, corrected_letter in zip(extracted_sentence, corrected_sentence):
        if original_letter.isalpha():  # Ensure the character is a letter
            total_letter_counts[original_letter] = total_letter_counts.get(original_letter, 0) + 1
            if original_letter != corrected_letter:
                incorrect_letter_counts[original_letter] = incorrect_letter_counts.get(original_letter, 0) + 1

def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Define the directory to monitor for new images
image_dir = 'data/images'
output_dir = 'output/'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define the event handler for newly created image files
class NewImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        global total_letter_counts  # Declare as global to access the global variable

        # Ignore directories and non-image files
        if event.is_directory or not (event.src_path.endswith('.png') or event.src_path.endswith('.jpg')):
            return

        print(f"New image detected: {event.src_path}")

        # Read the image as grayscale
        img = cv2.imread(event.src_path, cv2.IMREAD_GRAYSCALE)

        # Check if the image was loaded successfully
        if img is None:
            print(f"Failed to load image: {event.src_path}. Please check the file path or image integrity.")
            return

        # Perform text recognition on the image
        read_lines = read_page(img, DetectorConfig(scale=0.4, margin=5), 
                               line_clustering_config=LineClusteringConfig(min_words_per_line=1))

        # Save the recognized text to a .txt file
        filename = os.path.basename(event.src_path)
        txt_file_path = os.path.join(output_dir, filename + '.txt')
        with open(txt_file_path, 'w') as f:
            for read_line in read_lines:
                line_text = ' '.join(read_word.text for read_word in read_line)
                f.write(line_text + '\n')

        print(f"Text saved to {txt_file_path}")

        # Read the recognized text
        extracted_sentence = read_text_from_file(txt_file_path).replace('\n', ' ')

        # Get the corrected sentence from Gemini
        response = model.generate_content("Guess the correct sentence and just give me the corrected sentence as the response: " + extracted_sentence)
        corrected_sentence = response.text.strip()

        print(f"Extracted Sentence: {extracted_sentence}")
        print(f"Corrected Sentence: {corrected_sentence}")

        # Compare the extracted sentence with the corrected sentence and track incorrect letters
        compare_and_track_incorrect_letters(extracted_sentence.lower(), corrected_sentence.lower())

        # Create a dictionary to hold the percentages for each letter
        letter_percentages = {letter: 0 for letter in 'abcdefghijklmnopqrstuvwxyz'}
        for letter, total_count in total_letter_counts.items():
            incorrect_count = incorrect_letter_counts.get(letter, 0)
            letter_percentages[letter] = (incorrect_count / total_count) * 100 if total_count > 0 else 0

        # Add the current timestamp
        letter_percentages['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Load existing data if the Excel file exists, otherwise create a new DataFrame
        if os.path.exists(excel_file):
            df = pd.read_excel(excel_file)
        else:
            df = pd.DataFrame(columns=['timestamp'] + list('abcdefghijklmnopqrstuvwxyz'))

        # Create a new DataFrame for the current row
        new_row = pd.DataFrame([letter_percentages])

        # Concatenate the new row to the existing DataFrame
        df = pd.concat([df, new_row], ignore_index=True)

        # Save the updated DataFrame to the Excel file
        df.to_excel(excel_file, index=False)

        print(f"Data saved to {excel_file}")

        # Reset the incorrect letter counts and total letters count for the next image
        incorrect_letter_counts.clear()
        total_letter_counts.clear()

# Start monitoring the image directory for new files
event_handler = NewImageHandler()
observer = Observer()
observer.schedule(event_handler, path=image_dir, recursive=False)

# Start the observer
observer.start()
print(f"Monitoring directory: {image_dir}")

try:
    while True:
        time.sleep(1)  # Keep the script running
except KeyboardInterrupt:
    observer.stop()

observer.join()

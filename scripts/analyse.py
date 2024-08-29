import time
import os
import cv2
import htr_pipeline
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from htr_pipeline import read_page, DetectorConfig, LineClusteringConfig
import google.generativeai as genai  
# Assuming genai is the correct library
genai.configure(api_key="AIzaSyBPhRoY7S2I35q460jQTcbLVYcxccPB2Go")
# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Dictionary to store incorrect letter counts
incorrect_letter_counts = {}

def compare_and_track_incorrect_letters(extracted_sentence, corrected_sentence):
    # Compare letters between the extracted and corrected sentences
    for original_letter, corrected_letter in zip(extracted_sentence, corrected_sentence):
        if original_letter !=corrected_letter:
            if original_letter in incorrect_letter_counts:
                incorrect_letter_counts[original_letter] += 1
            else:
                incorrect_letter_counts[original_letter] = 1

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
        # Ignore directories and non-image files
        if event.is_directory or not (event.src_path.endswith('.png') or event.src_path.endswith('.jpg')):
            return

        print(f"New image detected: {event.src_path}")

        # Read the image as grayscale
        img = cv2.imread(event.src_path, cv2.IMREAD_GRAYSCALE)

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

        # Print the incorrect letters and their counts
        print("Incorrect letters and their counts:")
        for incorrect_letter, count in incorrect_letter_counts.items():
            print(f"'{incorrect_letter}' incorrect {count} times")
        incorrect_letter={}

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

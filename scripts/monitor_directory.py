import time
import os
import cv2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from htr_pipeline import read_page, DetectorConfig, LineClusteringConfig

# Define the directory to monitor
image_dir = 'data/images'
output_dir = 'output/'

# Create output directory if not exists
os.makedirs(output_dir, exist_ok=True)

# Define the event handler
class NewImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Check if the created file is an image
        if event.is_directory:
            return
        if event.src_path.endswith('.png') or event.src_path.endswith('.jpg'):
            print(f"New image detected: {event.src_path}")

            # Read the image
            img = cv2.imread(event.src_path, cv2.IMREAD_GRAYSCALE)

            # Perform text recognition
            #pass para
            read_lines = read_page(img, DetectorConfig(scale=0.4, margin=5), 
                                   line_clustering_config=LineClusteringConfig(min_words_per_line=1))

            # Save recognized text
            filename = os.path.basename(event.src_path)
            with open(os.path.join(output_dir, filename + '.txt'), 'w') as f:
                for read_line in read_lines:
                    line_text = ' '.join(read_word.text for read_word in read_line)
                    f.write(line_text + '\n')

            print(f"Text saved to {os.path.join(output_dir, filename + '.txt')}")

# Start monitoring the directory
event_handler = NewImageHandler()
observer = Observer()
observer.schedule(event_handler, path=image_dir, recursive=False)

# Start the observer
observer.start()
print(f"Monitoring directory: {image_dir}")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()

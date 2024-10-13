from concrete_loaders import PDFLoader, DOCXLoader, PPTLoader  # Make sure to use PPTLoader
from data_extractor import DataExtractor
from concrete_storage import FileStorage, SQLStorage
import os

# Create output directory if it doesn't exist
output_directory = 'output_directory'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Specify the file path
file_path = '/home/shtlp_0064/Desktop/Assignment_4 Python/somatosensory.pdf'  # Change this to your target file

# Determine the file type and load the appropriate loader
if file_path.endswith('.pdf'):
    loader = PDFLoader(file_path)
elif file_path.endswith('.docx'):
    loader = DOCXLoader(file_path)  # Make sure you have this class defined
elif file_path.endswith('.pptx'):
    loader = PPTLoader(file_path)  # Ensure PPTLoader is properly defined
else:
    raise ValueError("Unsupported file format")

# Initialize the DataExtractor
extractor = DataExtractor(loader)

# Extract data
text_data = extractor.extract_text()
links_data = extractor.extract_links()
images_data = extractor.extract_images()
tables_data = extractor.extract_tables()

# Save extracted data
file_storage = FileStorage(output_directory)
file_storage.save_text_data(text_data, "extracted_text.csv")
file_storage.save_links_data(links_data, "extracted_links.csv")
file_storage.save_images(images_data)
file_storage.save_tables(tables_data)

# Save extracted data to SQL database
sql_storage = SQLStorage('output.db')
sql_storage.save_text_data(text_data)
sql_storage.save_links_data(links_data)
sql_storage.save_images(images_data)

# Close the database connection
sql_storage.close()

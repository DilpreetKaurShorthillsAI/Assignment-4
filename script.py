from loaders.concrete_loaders import PDFLoader, DOCXLoader, PPTLoader  # Make sure to use PPTLoader
from extractor.data_extractor import DataExtractor
from storage.concrete_storage import FileStorage, SQLStorage
import os
 
# Create output directory if it doesn't exist
output_directory = 'output_directory'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
 
# Specify the file path
file_path = '/home/shtlp_0064/Desktop/Assignment_4 Python/samples/somatosensory.pdf'  # Change this to your target file
 
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
 
# Extract data with error handling
try:
    text_data = extractor.extract_text()
    links_data = extractor.extract_links()
    images_data = extractor.extract_images()
    tables_data = extractor.extract_tables()
except Exception as e:
    print(f"Error during data extraction: {e}")
    exit(1)  # Exit the program if extraction fails
 
# Save extracted data
file_storage = FileStorage(output_directory)
 
# Save extracted text data
try:
    file_storage.save_text_data(text_data, "extracted_text.txt")
except Exception as e:
    print(f"Error saving text data: {e}")
 
# Save extracted links data
try:
    file_storage.save_links_data(links_data, "extracted_links.csv")
except Exception as e:
    print(f"Error saving links data: {e}")
 
# Save extracted images data
try:
    file_storage.save_images(images_data)
except Exception as e:
    print(f"Error saving images: {e}")
 
# Save extracted tables data
try:
    file_storage.save_tables(tables_data)
except Exception as e:
    print(f"Error saving tables data: {e}")
 
# Save extracted data to SQL database
sql_storage = SQLStorage('output.db')
 
try:
    sql_storage.save_text_data(text_data)
    sql_storage.save_links_data(links_data)
    sql_storage.save_images(images_data)
except Exception as e:
    print(f"Error saving data to SQL database: {e}")
 
# Close the database connection
sql_storage.close()
 
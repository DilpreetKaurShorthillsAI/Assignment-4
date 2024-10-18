from loaders.concrete_loaders import PDFLoader, DOCXLoader, PPTLoader  # Ensure these classes are defined
from extractor.data_extractor import DataExtractor
from storage.concrete_storage import FileStorage, SQLStorage  # type: ignore
import os
 
# Create output directory if it doesn't exist
output_directory = 'output_directory'
os.makedirs(output_directory, exist_ok=True)
 
# Specify the file path
file_path = '/home/shtlp_0064/Desktop/Assignment_4 Python/samples/somatosensory.pdf'  # Change this to your target file
 
# Determine the file type and load the appropriate loader
loaders = {
    '.pdf': PDFLoader,
    '.docx': DOCXLoader,
    '.pptx': PPTLoader
}
file_extension = os.path.splitext(file_path)[1]
 
if file_extension in loaders:
    loader = loaders[file_extension](file_path)
else:
    raise ValueError("Unsupported file format")
 
# Initialize the DataExtractor
extractor = DataExtractor(loader)
 
# Function to extract data with error handling
def extract_data():
    try:
        return {
            'text': extractor.extract_text(),
            'links': extractor.extract_links(),
            'images': extractor.extract_images(),
            'tables': extractor.extract_tables()
        }
    except Exception as e:
        print(f"Error during data extraction: {e}")
        exit(1)
 
# Extract data
extracted_data = extract_data()
 
# Save data with error handling
def save_to_file(file_storage, data_type, data, file_name):
    try:
        if data_type == 'text':
            file_storage.save_text_data(data, file_name)
        elif data_type == 'links':
            file_storage.save_links_data(data, file_name)
        elif data_type == 'images':
            file_storage.save_images(data)
        elif data_type == 'tables':
            file_storage.save_tables(data)
    except Exception as e:
        print(f"Error saving {data_type} data: {e}")
 
# Initialize file storage
file_storage = FileStorage(output_directory)
 
# Save extracted data to files
save_to_file(file_storage, 'text', extracted_data['text'], "extracted_text.txt")
save_to_file(file_storage, 'links', extracted_data['links'], "extracted_links.csv")
save_to_file(file_storage, 'images', extracted_data['images'], None)  # Assuming no file name needed for images
save_to_file(file_storage, 'tables', extracted_data['tables'], None)
 
# Function to save data to SQL with error handling
def save_to_sql(sql_storage, extracted_data):
    try:
        sql_storage.save_text_data(extracted_data['text'])
        sql_storage.save_links_data(extracted_data['links'])
        sql_storage.save_images(extracted_data['images'])
        sql_storage.save_tables(extracted_data['tables'])
    except Exception as e:
        print(f"Error saving data to SQL database: {e}")
 
# Initialize SQL storage and save extracted data to the database
sql_storage = SQLStorage('output.db')
save_to_sql(sql_storage, extracted_data)
 
# Close the database connection
sql_storage.close()
 
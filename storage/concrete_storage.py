import os
import csv
import sqlite3
import fitz  # PyMuPDF for PDF handling
import docx
from pptx import Presentation
 
# File and SQL Storage Classes
class FileStorage:
    def __init__(self, directory):
        """Initialize storage directory."""
        self.directory = directory
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
 
    def save_text_data(self, text_data, filename):
        """Save extracted text data to a TXT file."""
        file_path = os.path.join(self.directory, filename)
        try:
            with open(file_path, mode='w', encoding='utf-8') as file:
                # Handle lists of strings (e.g., text)
                if isinstance(text_data, list):
                    for row in text_data:
                        file.write(row + '\n')  # Write each row followed by a newline
            print(f"Text data saved successfully to {filename}")
        except Exception as e:
            print(f"Error saving text data to {filename}: {e}")
 
    def save_links_data(self, links_data, filename):
        """Save extracted links data to CSV."""
        file_path = os.path.join(self.directory, filename)
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
 
                # Handle dictionaries (e.g., links)
                if isinstance(links_data, list) and len(links_data) > 0 and isinstance(links_data[0], dict):
                    # Write header row based on the keys of the first dict
                    writer.writerow(links_data[0].keys())
                    for item in links_data:
                        writer.writerow(item.values())
            print(f"Links data saved successfully to {filename}")
        except Exception as e:
            print(f"Error saving links data to {filename}: {e}")
 
    def save_images(self, images_data):
        """Save extracted images to disk with metadata."""
        images_dir = os.path.join(self.directory, 'images')
        os.makedirs(images_dir, exist_ok=True)
 
        for i, img_data in enumerate(images_data):
            image_format = img_data.get('image_format', 'png')  # Default to 'png'
            file_path = os.path.join(images_dir, f'image_{i + 1}.{image_format}')
            try:
                with open(file_path, "wb") as img_file:
                    img_file.write(img_data['image_bytes'])
                print(f"Image saved successfully: {file_path}")
 
                # Save metadata
                metadata_path = os.path.join(images_dir, f'image_{i + 1}_metadata.csv')
                with open(metadata_path, mode='w', newline='', encoding='utf-8') as meta_file:
                    writer = csv.writer(meta_file)
                    writer.writerow(img_data['metadata'].keys())  # Write header
                    writer.writerow(img_data['metadata'].values())  # Write values
                print(f"Metadata for image saved successfully: {metadata_path}")
 
            except Exception as e:
                print(f"Error saving image {file_path}: {e}")
 
    def save_tables(self, tables_data):
        """Save extracted tables to separate CSV files with metadata."""
        tables_dir = os.path.join(self.directory, 'tables')
        os.makedirs(tables_dir, exist_ok=True)
 
        for i, table_data in enumerate(tables_data):
            file_path = os.path.join(tables_dir, f'table_{i + 1}.csv')
 
            # Check if table_data is in expected format and extract content
            if 'content' in table_data:
                content = table_data['content']
                # Ensure each cell is converted to a string, and handle NaN values
                modified_table = [
                    [str(cell) if cell is not None and str(cell) != 'nan' else '' for cell in row] for row in content
                ]
            else:
                print(f"Unexpected table format for table {i + 1}: {table_data}")
                continue
 
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(modified_table)
                print(f"Table {i + 1} saved successfully.")
 
                # Save metadata
                metadata_path = os.path.join(tables_dir, f'table_{i + 1}_metadata.csv')
                with open(metadata_path, mode='w', newline='', encoding='utf-8') as meta_file:
                    writer = csv.writer(meta_file)
                    writer.writerow(table_data['metadata'].keys())  # Write header
                    writer.writerow(table_data['metadata'].values())  # Write values
                print(f"Metadata for table saved successfully: {metadata_path}")
 
            except Exception as e:
                print(f"Error saving table {file_path}: {e}")
 
 
class SQLStorage:
    def __init__(self, db_name):
        """Initialize SQL storage with a database."""
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
 
        # Create tables if they do not exist
        self.create_tables()
 
    def create_tables(self):
        """Create necessary tables in the database."""
        # Drop tables if they exist to avoid conflicts
        self.cursor.execute('DROP TABLE IF EXISTS text_data')
        self.cursor.execute('DROP TABLE IF EXISTS links_data')
        self.cursor.execute('DROP TABLE IF EXISTS images_data')
        self.cursor.execute('DROP TABLE IF EXISTS tables_data')
 
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS text_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT
            )
        ''')
 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS links_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                url TEXT
            )
        ''')
 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image BLOB,
                format TEXT,
                source TEXT,
                page_number INTEGER,
                description TEXT
            )
        ''')
 
        # Create the tables_data table for saving table rows
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tables_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_id INTEGER,
                row_number INTEGER,
                content TEXT,
                source TEXT,
                description TEXT
            )
        ''')
 
        self.connection.commit()
 
    def save_text_data(self, text_data):
        """Save text data to SQL database."""
        if not isinstance(text_data, list):
            print("Error: text_data should be a list.")
            return
 
        try:
            for item in text_data:
                self.cursor.execute('INSERT INTO text_data (content) VALUES (?)', (item,))
            self.connection.commit()
            print(f"Saved {len(text_data)} text items to the database.")
        except Exception as e:
            print(f"Error saving text data: {e}")
 
    def save_links_data(self, links_data):
        """Save links data to SQL database."""
        if not isinstance(links_data, list):
            print("Error: links_data should be a list.")
            return
 
        try:
            for item in links_data:
                if 'text' in item and 'url' in item:
                    self.cursor.execute('INSERT INTO links_data (text, url) VALUES (?, ?)', (item['text'], item['url']))
                else:
                    print("Error: Each item in links_data must contain 'text' and 'url' keys.")
            self.connection.commit()
            print(f"Saved {len(links_data)} links to the database.")
        except Exception as e:
            print(f"Error saving links data: {e}")
 
    def save_images(self, images_data):
        """Save images data to SQL database with metadata."""
        if not isinstance(images_data, list):
            print("Error: images_data should be a list.")
            return
 
        try:
            for img_data in images_data:
                if 'image_bytes' in img_data and 'image_format' in img_data and 'metadata' in img_data:
                    # Ensure metadata keys exist
                    source = img_data['metadata'].get('source', '')
                    page_number = img_data['metadata'].get('page_number', None)
                    description = img_data['metadata'].get('description', '')
 
                    self.cursor.execute('INSERT INTO images_data (image, format, source, page_number, description) VALUES (?, ?, ?, ?, ?)',
                                        (sqlite3.Binary(img_data['image_bytes']), img_data['image_format'],
                                         source, page_number, description))
                else:
                    print("Error: Each item in images_data must contain 'image_bytes', 'image_format', and 'metadata' keys.")
            self.connection.commit()
            print(f"Saved {len(images_data)} images to the database.")
        except Exception as e:
            print(f"Error saving images data: {e}")
 
    def save_tables(self, tables_data):
        """Save table data to SQL database as rows with metadata."""
        if not isinstance(tables_data, list):
            print("Error: tables_data should be a list.")
            return
 
        try:
            for table_id, table in enumerate(tables_data, start=1):
                if 'content' in table and 'metadata' in table:
                    source = table['metadata'].get('source', '')
                    description = table['metadata'].get('description', '')
 
                    # Save each row of the table separately
                    for row_number, row in enumerate(table['content'], start=1):
                        # Convert each cell to string, handling None or NaN values
                        row_content = ','.join([str(cell) if cell is not None and str(cell) != 'nan' else '' for cell in row])
                        self.cursor.execute('INSERT INTO tables_data (table_id, row_number, content, source, description) VALUES (?, ?, ?, ?, ?)',
                                            (table_id, row_number, row_content, source, description))
                else:
                    print(f"Unexpected table format for table: {table}")
            self.connection.commit()
            print(f"Saved {len(tables_data)} tables to the database.")
        except Exception as e:
            print(f"Error saving tables data: {e}")
 
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
import os
import csv
import sqlite3
import fitz  # PyMuPDF for PDF handling
import docx
from pptx import Presentation
from PIL import Image
import io
 
class FileStorage:
    def __init__(self, directory):
        """Initialize storage directory."""
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)
 
    def _save_file(self, file_path, content, write_mode='w', is_binary=False):
        """Helper method to save text or binary data to a file."""
        open_mode = f'{write_mode}b' if is_binary else write_mode
        try:
            with open(file_path, open_mode, encoding=None if is_binary else 'utf-8') as file:
                if isinstance(content, list):
                    if is_binary:
                        file.write(content)
                    else:
                        for row in content:
                            file.write(row + '\n')
            print(f"Data saved successfully to {file_path}")
        except Exception as e:
            print(f"Error saving data to {file_path}: {e}")
 
    def _save_metadata(self, directory, filename, metadata):
        """Helper method to save metadata."""
        metadata_path = os.path.join(directory, f'{filename}_metadata.csv')
        try:
            with open(metadata_path, mode='w', newline='', encoding='utf-8') as meta_file:
                writer = csv.writer(meta_file)
                writer.writerow(metadata.keys())
                writer.writerow(metadata.values())
            print(f"Metadata saved successfully: {metadata_path}")
        except Exception as e:
            print(f"Error saving metadata for {filename}: {e}")
 
    def save_text_data(self, text_data, filename):
        """Save extracted text data to a TXT file."""
        file_path = os.path.join(self.directory, filename)
        self._save_file(file_path, text_data)
 
    def save_links_data(self, links_data, filename):
        """Save extracted links data to CSV."""
        file_path = os.path.join(self.directory, filename)
        if links_data:
            header = links_data[0].keys()
            rows = [item.values() for item in links_data]
            self._save_file(file_path, [','.join(header)] + [','.join(map(str, row)) for row in rows])
 
    def save_images(self, images_data):
        """Save extracted images to disk with metadata."""
        images_dir = os.path.join(self.directory, 'images')
        os.makedirs(images_dir, exist_ok=True)
 
        for i, img_data in enumerate(images_data, start=1):
            image_format = img_data.get('image_format', 'png').lower()
 
            if image_format in ['jpeg', 'jpg', 'png']:
                file_path = os.path.join(images_dir, f'image_{i}.{image_format}')
 
                # Convert image bytes to an image and save it in the appropriate format
                try:
                    image = Image.open(io.BytesIO(img_data['image_bytes']))
                    image.save(file_path, format=image_format.upper())
                    print(f"Image saved successfully: {file_path}")
                except Exception as e:
                    print(f"Error saving image {file_path}: {e}")
 
                # Save metadata
                self._save_metadata(images_dir, f'image_{i}', img_data['metadata'])
 
            else:
                print(f"Unsupported image format: {image_format}")
 
    def save_tables(self, tables_data):
        """Save extracted tables to separate CSV files with metadata."""
        tables_dir = os.path.join(self.directory, 'tables')
        os.makedirs(tables_dir, exist_ok=True)
 
        for i, table_data in enumerate(tables_data, start=1):
            file_path = os.path.join(tables_dir, f'table_{i}.csv')
            content = table_data.get('content', [])
            formatted_content = [[str(cell) if cell else '' for cell in row] for row in content]
            self._save_file(file_path, [','.join(row) for row in formatted_content])
            self._save_metadata(tables_dir, f'table_{i}', table_data['metadata'])
 
 
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
        table_definitions = {
            'text_data': 'id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT',
            'links_data': 'id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, url TEXT',
            'images_data': 'id INTEGER PRIMARY KEY AUTOINCREMENT, image BLOB, format TEXT, source TEXT, page_number INTEGER, description TEXT',
            'tables_data': 'id INTEGER PRIMARY KEY AUTOINCREMENT, table_id INTEGER, row_number INTEGER, content TEXT, source TEXT, description TEXT'
        }
        for table, schema in table_definitions.items():
            self.cursor.execute(f'DROP TABLE IF EXISTS {table}')
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table} ({schema})')
        self.connection.commit()
 
    def _save_to_table(self, table, columns, values_list):
        """Helper method to insert multiple rows into a table."""
        placeholders = ', '.join(['?' for _ in columns])
        insert_query = f'INSERT INTO {table} ({", ".join(columns)}) VALUES ({placeholders})'
        try:
            self.cursor.executemany(insert_query, values_list)
            self.connection.commit()
            print(f"Saved {len(values_list)} records to {table}.")
        except Exception as e:
            print(f"Error saving to {table}: {e}")
 
    def save_text_data(self, text_data):
        """Save text data to SQL database."""
        if isinstance(text_data, list):
            self._save_to_table('text_data', ['content'], [(item,) for item in text_data])
 
    def save_links_data(self, links_data):
        """Save links data to SQL database."""
        if isinstance(links_data, list):
            values_list = [(item['text'], item['url']) for item in links_data if 'text' in item and 'url' in item]
            self._save_to_table('links_data', ['text', 'url'], values_list)
 
    def save_images(self, images_data):
        """Save images data to SQL database with metadata."""
        if isinstance(images_data, list):
            values_list = [(sqlite3.Binary(img['image_bytes']), img['image_format'],
                            img['metadata'].get('source', ''), img['metadata'].get('page_number', None),
                            img['metadata'].get('description', ''))
                           for img in images_data]
            self._save_to_table('images_data', ['image', 'format', 'source', 'page_number', 'description'], values_list)
 
    def save_tables(self, tables_data):
        """Save table data to SQL database as rows with metadata."""
        if isinstance(tables_data, list):
            for table_id, table in enumerate(tables_data, start=1):
                rows = [(table_id, row_num, ','.join([str(cell) for cell in row]),
                         table['metadata'].get('source', ''), table['metadata'].get('description', ''))
                        for row_num, row in enumerate(table.get('content', []), start=1)]
                self._save_to_table('tables_data', ['table_id', 'row_number', 'content', 'source', 'description'], rows)
 
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
 
# Assignment-4 File Extraction

## Overview

This project implements a modular Python class structure to extract text, hyperlinks, images, and tables from PDF, DOCX, and PPT files while capturing relevant metadata. The design utilizes abstract classes for flexibility, enabling concrete implementations tailored for each file type and storage method.

## Class Structure

### Abstract Class: FileLoader

- **Purpose**: Defines a blueprint for loading and validating various file types.
- **Methods**: Abstract methods for loading and processing files.

### Concrete Classes

- **PDFLoader**: Implements loading and processing logic specific to PDF files.
- **DOCXLoader**: Implements loading and processing logic specific to DOCX files.
- **PPTLoader**: Implements loading and processing logic specific to PPT files.

### Class: DataExtractor

- **Purpose**: Takes an instance of FileLoader and provides methods for extracting data.
- **Methods**:
  - extract_text(): Extracts text and associated metadata.
  - extract_links(): Extracts hyperlinks and metadata.
  - extract_images(): Extracts images and metadata.
  - extract_tables(): Extracts tables and metadata.

### Abstract Class: Storage

- **Purpose**: Defines a blueprint for storing extracted data.
  
### Concrete Classes

- **FileStorage**: Saves extracted data to files (e.g., images to directories, tables to CSV).
- **SQLStorage**: Stores extracted data in an SQL database.

## Testing

- Implement unit tests to validate each class and method.
- Test with various file types (PDF, DOCX, PPT) to ensure accurate data extraction and storage.
- To run the tests:
  
  ```
  python3 -m unittest test_suite.py

### Deliverables

- A modular class design with abstract and concrete classes for file loading and data storage.
- A testing suite to validate functionality across multiple file types and storage methods.

### Usage

To use this package, instantiate the appropriate FileLoader, pass it to the DataExtractor, and choose a Storage implementation to save the extracted data.

---

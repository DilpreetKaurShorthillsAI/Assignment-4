import fitz  # PyMuPDF for PDF handling
import tabula  # For PDF table extraction
import docx  # For DOCX handling
from pptx import Presentation  # For PPTX handling

class DataExtractor:
    def __init__(self, loader):
        self.loader = loader
        self.file_path = loader.file_path

    def extract_text(self):
        """Extract text from the file."""
        text_data = []

        if self.file_path.endswith('.pdf'):
            pdf_document = fitz.open(self.file_path)
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text_data.append(page.get_text() or "")
            pdf_document.close()
            return text_data

        elif self.file_path.endswith('.docx'):
            doc = self.loader.load_file()
            for paragraph in doc.paragraphs:
                text_data.append(paragraph.text + "\n")
            return text_data

        elif self.file_path.endswith('.pptx'):
            ppt = self.loader.load_file()
            for slide in ppt.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text_data.append(shape.text + "\n")
            return text_data

        else:
            raise ValueError("Unsupported file format for text extraction.")

    def extract_images(self):
        """Extract images from the file, including metadata."""
        images_data = []

        if self.file_path.endswith('.pdf'):
            pdf_document = fitz.open(self.file_path)
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                image_list = page.get_images(full=True)
                for img in image_list:
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    width, height = base_image["width"], base_image["height"]
                    images_data.append({
                        "image_bytes": image_bytes,
                        "image_format": image_ext,
                        "page": page_num + 1,
                        "dimensions": (width, height),
                        "metadata": {
                            "source": self.file_path,
                            "page_number": page_num + 1,
                            "description": f"Image from page {page_num + 1} of {self.file_path}"
                        }
                    })
            pdf_document.close()

        elif self.file_path.endswith('.docx'):
            doc = self.loader.load_file()
            for rel in doc.part.rels:
                if "image" in doc.part.rels[rel].target_ref:
                    image = doc.part.rels[rel].target_part.blob
                    images_data.append({
                        "image_bytes": image,
                        "image_format": "png",  # or "jpeg" based on the image
                        "metadata": {
                            "source": self.file_path,
                            "description": "Image from DOCX file"
                        }
                    })

        elif self.file_path.endswith('.pptx'):
            ppt = self.loader.load_file()
            for slide_num, slide in enumerate(ppt.slides):
                for shape in slide.shapes:
                    if hasattr(shape, "image"):
                        images_data.append({
                            "image_bytes": shape.image.blob,
                            "image_format": shape.image.ext,
                            "metadata": {
                                "source": self.file_path,
                                "slide_number": slide_num + 1,
                                "description": "Image from PPTX file"
                            }
                        })

        return images_data

    def extract_links(self):
        """Extract hyperlinks from the file, including metadata."""
        links_data = []

        if self.file_path.endswith('.pdf'):
            pdf_document = fitz.open(self.file_path)
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                links = page.get_links()
                for link in links:
                    if "uri" in link:
                        url = link["uri"]
                        text = link.get("title", url)
                        rect = link["from"]
                        links_data.append({
                            "text": text,
                            "url": url,
                            "page": page_num + 1,
                            "position": {
                                "x0": rect.x0,
                                "y0": rect.y0,
                                "x1": rect.x1,
                                "y1": rect.y1
                            },
                            "metadata": {
                                "source": self.file_path,
                                "description": f"Link from page {page_num + 1}"
                            }
                        })
            pdf_document.close()

        elif self.file_path.endswith('.docx'):
            doc = self.loader.load_file()
            for rel in doc.part.rels.values():
                if "hyperlink" in rel.target_ref:
                    # Getting the text associated with the hyperlink
                    hyperlink = rel.target_part
                    links_data.append({
                        "text": hyperlink.text or rel.target_ref,  # Use the text if available
                        "url": rel.target_ref,
                        "metadata": {
                            "source": self.file_path,
                            "description": "Hyperlink from DOCX file"
                        }
                    })

        elif self.file_path.endswith('.pptx'):
            ppt = self.loader.load_file()
            for slide_num, slide in enumerate(ppt.slides):
                for shape in slide.shapes:
                    if hasattr(shape, "text_frame"):
                        for paragraph in shape.text_frame.paragraphs:
                            for run in paragraph.runs:
                                if run.hyperlink:
                                    links_data.append({
                                        "text": run.text,
                                        "url": run.hyperlink.address,
                                        "metadata": {
                                            "source": self.file_path,
                                            "slide_number": slide_num + 1,
                                            "description": "Hyperlink from PPTX file"
                                        }
                                    })

        return links_data

    def extract_tables(self):
        """Extract tables from the file, including metadata."""
        tables_data = []

        if self.file_path.endswith('.pdf'):
            # Extract tables from PDF using Tabula
            try:
                # Ensure that 'tabula' is installed and properly configured
                tables = tabula.read_pdf(self.file_path, pages='all', multiple_tables=True)
                for table_index, table in enumerate(tables):
                    tables_data.append({
                        "content": table.values.tolist(),  # Convert DataFrame to list of lists
                        "metadata": {
                            "source": self.file_path,
                            "description": f"Table extracted from PDF, Table {table_index + 1}"
                        }
                    })
            except Exception as e:
                print(f"Error extracting tables from PDF: {e}")
            return tables_data

        elif self.file_path.endswith('.docx'):
            doc = self.loader.load_file()
            for table_index, table in enumerate(doc.tables):
                table_content = [[cell.text.strip() for cell in row.cells] for row in table.rows]
                tables_data.append({
                    "content": table_content,
                    "metadata": {
                        "source": self.file_path,
                        "description": f"Table extracted from DOCX, Table {table_index + 1}"
                    }
                })
            return tables_data

        elif self.file_path.endswith('.pptx'):
            ppt = self.loader.load_file()
            for slide_num, slide in enumerate(ppt.slides):
                for shape in slide.shapes:
                    if hasattr(shape, "table"):
                        table = shape.table
                        table_content = [[cell.text.strip() for cell in row.cells] for row in table.rows]
                        tables_data.append({
                            "content": table_content,
                            "metadata": {
                                "source": self.file_path,
                                "description": f"Table extracted from PPTX, Slide {slide_num + 1}"
                            }
                        })

        return tables_data

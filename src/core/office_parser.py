from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from docx import Document
from openpyxl import load_workbook
from pptx import Presentation


@dataclass
class OfficeMetadata:
    author: Optional[str] = None
    title: Optional[str] = None
    created: Optional[str] = None


class OfficeParser:
    """Parse Microsoft Office documents for text and metadata."""

    def parse_docx(self, file_path: Path) -> Dict[str, object]:
        doc = Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text]
        headings = [
            p.text for p in doc.paragraphs if p.style.name.startswith("Heading")
        ]
        metadata = self.get_document_metadata_docx(doc)
        return {
            "paragraphs": paragraphs,
            "headings": headings,
            "metadata": metadata.__dict__,
        }

    def parse_xlsx(self, file_path: Path) -> Dict[str, object]:
        wb = load_workbook(file_path, data_only=True)
        sheets: Dict[str, List[List[object]]] = {}
        for sheet in wb.worksheets:
            rows = []
            for row in sheet.iter_rows(values_only=True):
                rows.append(list(row))
            sheets[sheet.title] = rows
        metadata = OfficeMetadata()
        return {"sheets": sheets, "metadata": metadata.__dict__}

    def parse_pptx(self, file_path: Path) -> Dict[str, object]:
        pres = Presentation(file_path)
        slides = []
        for slide in pres.slides:
            texts = []
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    if shape.text:
                        texts.append(shape.text)
            slides.append(texts)
        metadata = OfficeMetadata()
        return {"slides": slides, "metadata": metadata.__dict__}

    def extract_images(self, file_path: Path, output_dir: Path) -> List[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        if file_path.suffix.lower() == ".pptx":
            pres = Presentation(file_path)
            images = []
            for slide in pres.slides:
                for shape in slide.shapes:
                    if shape.shape_type == 13:  # picture
                        image = shape.image
                        fname = output_dir / image.filename
                        with open(fname, "wb") as f:
                            f.write(image.blob)
                        images.append(fname)
            return images
        if file_path.suffix.lower() == ".docx":
            doc = Document(file_path)
            images = []
            rels = doc.part._rels
            for rel in rels.values():
                if "image" in rel.reltype:
                    image_data = rel.target_part.blob
                    fname = output_dir / Path(rel.target_ref).name
                    with open(fname, "wb") as f:
                        f.write(image_data)
                    images.append(fname)
            return images
        return []

    def get_document_metadata_docx(self, doc: Document) -> OfficeMetadata:
        props = doc.core_properties
        return OfficeMetadata(
            author=props.author,
            title=props.title,
            created=str(props.created) if props.created else None,
        )

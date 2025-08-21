

import os
import re
import glob
from typing import List, Tuple
from PyPDF2 import PdfMerger

class PDFSorterMerger:
    DATE_PATTERN = re.compile(r'(\d{4}-\d{2}-\d{2}T\d{2}_?\d{2,4}_?\d{2,4}[+-]\d{2}_\d{2})')

    def __init__(self, input_path: str):
        self.input_path = input_path
        self.pdf_files = self._get_pdf_files()

    def _get_pdf_files(self) -> List[str]:
        if os.path.isdir(self.input_path):
            pdfs = glob.glob(os.path.join(self.input_path, "*.pdf"))
        else:
            # Assume input_path is a list of files separated by comma
            pdfs = [f.strip() for f in self.input_path.split(",") if f.strip().lower().endswith(".pdf")]
        return pdfs

    def _extract_date_from_filename(self, filename: str) -> str:
        match = self.DATE_PATTERN.search(filename)
        if not match:
            return ""
        
        date_str = match.group(1)
        # Normalize the date format by ensuring proper underscores
        time_part = date_str.split('T')[1].split('+')[0].split('-')[0]
        
        if '_' not in time_part:
            if len(time_part) == 6:  # HHMMSS format
                date_str = date_str.replace(time_part, f"{time_part[:4]}_{time_part[4:]}")
        elif time_part.count('_') == 1:
            parts = time_part.split('_')
            if len(parts[1]) == 4:  # MMSS format like "0256"
                date_str = date_str.replace(time_part, f"{parts[0]}_{parts[1][:2]}_{parts[1][2:]}")
            elif len(parts[0]) == 2 and len(parts[1]) == 4:  # HH_MMSS format like "06_0256"
                date_str = date_str.replace(time_part, f"{parts[0]}_{parts[1][:2]}_{parts[1][2:]}")
        
        return date_str

    def _sort_pdfs_by_date(self) -> List[Tuple[str, str]]:
        pdfs_with_dates = []
        for pdf in self.pdf_files:
            date_str = self._extract_date_from_filename(os.path.basename(pdf))
            pdfs_with_dates.append((pdf, date_str))
        
        print(f"\nFound {len(pdfs_with_dates)} PDF files:")
        for pdf, date_str in pdfs_with_dates:
            filename = os.path.basename(pdf)
            print(f"  {filename} -> Date: {date_str if date_str else 'NO DATE'}")
        
        # Sort by date string, empty dates go first
        pdfs_with_dates.sort(key=lambda x: (x[1] == "", x[1]))
        
        print(f"\nSorted order:")
        for i, (pdf, date_str) in enumerate(pdfs_with_dates, 1):
            filename = os.path.basename(pdf)
            print(f"  {i:2d}. {filename} -> Date: {date_str if date_str else 'NO DATE'}")
        
        return pdfs_with_dates

    def merge_pdfs(self, output_path: str):
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # If output_path is a directory, create a default filename
        if os.path.isdir(output_path) or output_path.endswith(os.sep):
            output_path = os.path.join(output_path, "merged_emails.pdf")
        
        sorted_pdfs = self._sort_pdfs_by_date()
        merger = PdfMerger()
        
        print(f"\nMerging PDFs in order:")
        for i, (pdf, date_str) in enumerate(sorted_pdfs, 1):
            filename = os.path.basename(pdf)
            print(f"  {i:2d}. Adding: {filename}")
            merger.append(pdf)
        
        merger.write(output_path)
        merger.close()
        print(f"\nSuccessfully merged {len(sorted_pdfs)} PDFs into {output_path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sort and merge PDF files by date in filename.")
    parser.add_argument("--input", required=True, help="Input folder or comma-separated list of PDF files")
    parser.add_argument("--output", required=True, help="Output merged PDF file path")
    args = parser.parse_args()

    pdf_merger = PDFSorterMerger(args.input)
    pdf_merger.merge_pdfs(args.output)

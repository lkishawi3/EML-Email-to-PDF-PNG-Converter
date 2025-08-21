# EML to PDF Converter

This tool converts all `.eml` files in the current directory into a single PDF file.

## Features

- Converts all `.eml` files to a single PDF
- Preserves email metadata (From, To, Subject, Date)
- Handles both plain text and HTML email content
- Creates a well-formatted PDF with proper styling
- Includes a title page with summary information

## Requirements

- Python 3.6 or higher
- Required packages: `reportlab`, `html2text`

## Quick Start

### Option 1: Using the batch file (Windows)
1. Double-click `run_converter.bat`
2. The script will automatically install dependencies and run the converter
3. Your PDF will be saved as `combined_emails.pdf`

### Option 2: Manual installation
1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the converter:
   ```bash
   python eml_to_pdf_converter.py
   ```

## Output

The converter will create a file called `combined_emails.pdf` containing:
- A title page with generation date and email count
- All emails formatted with headers, metadata, and content
- Clear separators between emails
- Page breaks every 5 emails for better organization

## File Structure

- `eml_to_pdf_converter.py` - Main conversion script
- `requirements.txt` - Python dependencies
- `run_converter.bat` - Windows batch file for easy execution
- `README.md` - This file

## Troubleshooting

If you encounter any issues:
1. Make sure Python is installed and in your PATH
2. Ensure you have write permissions in the current directory
3. Check that the `.eml` files are valid email files
4. Try running the script manually to see detailed error messages

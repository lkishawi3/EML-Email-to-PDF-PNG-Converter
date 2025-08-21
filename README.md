# EML to PDF/HTML/PNG Converter

This tool converts individual `.eml` files or batches of `.eml` files to HTML, PDF, or PNG formats with browser-like rendering quality.

## Features

- Converts individual `.eml` files to HTML, PDF, or PNG formats
- **NEW**: Batch processing of entire folders containing multiple `.eml` files
- Uses Playwright for browser-like rendering (Edge/Chrome quality)
- Supports both light and dark mode themes
- Preserves email formatting and styling
- Handles HTML email content with proper rendering
- Creates high-quality output files

## Requirements

- Python 3.6 or higher
- Required packages: `playwright` (automatically installed if missing)

## Installation

1. Install the required packages:
   ```bash
   pip install playwright
   playwright install chromium
   ```

## Usage

The script supports both single file and batch processing:

### Single File Processing

#### Convert to HTML
```bash
python eml-to-pdf-render.py --html "your_email.eml"
python eml-to-pdf-render.py --html "your_email.eml" --output-dir "output_folder"
```

#### Convert to PDF
```bash
# Light mode (default)
python eml-to-pdf-render.py --pdf "your_email.eml"
python eml-to-pdf-render.py --pdf "your_email.eml" --output-dir "output_folder"

# Dark mode
python eml-to-pdf-render.py --pdf "your_email.eml" --dark
python eml-to-pdf-render.py --pdf "your_email.eml" --dark --output-dir "output_folder"
```

#### Convert to PNG Screenshot
```bash
# Light mode (default)
python eml-to-pdf-render.py --png "your_email.eml"
python eml-to-pdf-render.py --png "your_email.eml" --output-dir "output_folder"

# Dark mode
python eml-to-pdf-render.py --png "your_email.eml" --dark
python eml-to-pdf-render.py --png "your_email.eml" --dark --output-dir "output_folder"
```

### Batch Processing

#### Convert all EML files in a folder to HTML
```bash
python eml-to-pdf-render.py --batch-html "path/to/eml/folder"
python eml-to-pdf-render.py --batch-html "path/to/eml/folder" --output-dir "output_folder"
```

#### Convert all EML files in a folder to PDF
```bash
# Light mode (default)
python eml-to-pdf-render.py --batch-pdf "path/to/eml/folder"
python eml-to-pdf-render.py --batch-pdf "path/to/eml/folder" --output-dir "output_folder"

# Dark mode
python eml-to-pdf-render.py --batch-pdf "path/to/eml/folder" --dark
python eml-to-pdf-render.py --batch-pdf "path/to/eml/folder" --dark --output-dir "output_folder"
```

#### Convert all EML files in a folder to PNG
```bash
# Light mode (default)
python eml-to-pdf-render.py --batch-png "path/to/eml/folder"
python eml-to-pdf-render.py --batch-png "path/to/eml/folder" --output-dir "output_folder"

# Dark mode
python eml-to-pdf-render.py --batch-png "path/to/eml/folder" --dark
python eml-to-pdf-render.py --batch-png "path/to/eml/folder" --dark --output-dir "output_folder"
```

## Output

### Single File Processing
The converter creates output files in the same directory as the input `.eml` file (or in the specified output directory):
- **HTML**: `email_name.html` - Extracted HTML content
- **PDF**: `email_name.pdf` - High-quality PDF with proper formatting
- **PNG**: `email_name.png` - Full-page screenshot

### Batch Processing
The converter processes all `.eml` files in the specified folder and creates corresponding output files:
- **HTML**: `email1.html`, `email2.html`, etc.
- **PDF**: `email1.pdf`, `email2.pdf`, etc.
- **PNG**: `email1.png`, `email2.png`, etc.

Files are processed in alphabetical order for consistent results.

### Output Directory Option
Use the `--output-dir` parameter to specify a custom output directory:
- Creates the directory if it doesn't exist
- All converted files will be saved to the specified directory
- Useful for organizing output files separately from input files

## Dark Mode Support

When using the `--dark` flag:
- PDFs and PNGs are rendered with a dark theme
- Uses CSS filters and Dark Reader-like styling
- Maintains readability while providing a dark appearance
- Images are properly inverted to maintain visibility

## Technical Details

- Uses Playwright for browser automation
- Extracts HTML content from multipart email messages
- Renders emails using Chromium browser engine
- Supports complex email layouts and styling
- Handles both simple and multipart email formats
- Batch processing includes progress indicators and error handling

## File Structure

- `eml-to-pdf-render.py` - Main conversion script
- `requirements.txt` - Python dependencies (legacy)
- `README.md` - This file

## Troubleshooting

If you encounter any issues:
1. Make sure Python is installed and in your PATH
2. Ensure you have write permissions in the current directory
3. Check that the `.eml` file(s) are valid and contain HTML content
4. For dark mode, ensure the script has access to create temporary files
5. If Playwright isn't installed, the script will attempt to install it automatically
6. For batch processing, ensure the folder path is correct and contains `.eml` files

## Notes

- Single file processing handles one email file at a time
- Batch processing automatically finds all `.eml` files in the specified folder
- HTML output is extracted directly from the email content
- PDF and PNG outputs use browser rendering for best quality
- Dark mode requires additional processing time for theme application
- Batch processing shows progress (e.g., "Processing 3/10: email.eml")

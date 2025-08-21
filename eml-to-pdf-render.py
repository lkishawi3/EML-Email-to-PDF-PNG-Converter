import sys
import os
import glob
from email import policy
from email.parser import BytesParser

def extract_html_from_eml(eml_file):
    """Extract HTML content from .eml file"""
    with open(eml_file, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    html_content = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                break
    else:
        if msg.get_content_type() == 'text/html':
            html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
    
    return html_content

def get_eml_files_from_folder(folder_path):
    """Get all .eml files from a folder"""
    if os.path.isfile(folder_path):
        # If it's a single file, return it
        return [folder_path] if folder_path.lower().endswith('.eml') else []
    
    # If it's a folder, get all .eml files
    pattern = os.path.join(folder_path, "*.eml")
    eml_files = glob.glob(pattern)
    return sorted(eml_files)  # Sort for consistent processing order

def batch_convert_to_html(folder_path, dark_mode=False, output_dir=None):
    """Convert all .eml files in a folder to HTML"""
    eml_files = get_eml_files_from_folder(folder_path)
    
    if not eml_files:
        print(f"No .eml files found in {folder_path}")
        return []
    
    print(f"Found {len(eml_files)} .eml files to convert to HTML")
    converted_files = []
    
    for i, eml_file in enumerate(eml_files, 1):
        print(f"Processing {i}/{len(eml_files)}: {os.path.basename(eml_file)}")
        result = convert_to_html(eml_file, dark_mode, output_dir)
        if result:
            converted_files.append(result)
    
    print(f"Successfully converted {len(converted_files)} files to HTML")
    return converted_files

def batch_convert_to_pdf(folder_path, dark_mode=False, output_dir=None):
    """Convert all .eml files in a folder to PDF"""
    eml_files = get_eml_files_from_folder(folder_path)
    
    if not eml_files:
        print(f"No .eml files found in {folder_path}")
        return []
    
    print(f"Found {len(eml_files)} .eml files to convert to PDF")
    converted_files = []
    
    # Start shared HTTP server for dark mode if needed
    server_thread = None
    if dark_mode:
        import http.server
        import socketserver
        import threading
        import time
        
        def start_server():
            PORT = 8000
            Handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                httpd.serve_forever()
        
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        time.sleep(2)
    
    try:
        for i, eml_file in enumerate(eml_files, 1):
            print(f"Processing {i}/{len(eml_files)}: {os.path.basename(eml_file)}")
            result = convert_to_pdf(eml_file, dark_mode, output_dir, shared_server=dark_mode)
            if result:
                converted_files.append(result)
    finally:
        # Clean up server if it was started
        if server_thread and server_thread.is_alive():
            # The server will be cleaned up when the thread ends
            pass
    
    print(f"Successfully converted {len(converted_files)} files to PDF")
    return converted_files

def batch_convert_to_png(folder_path, dark_mode=False, output_dir=None):
    """Convert all .eml files in a folder to PNG"""
    eml_files = get_eml_files_from_folder(folder_path)
    
    if not eml_files:
        print(f"No .eml files found in {folder_path}")
        return []
    
    print(f"Found {len(eml_files)} .eml files to convert to PNG")
    converted_files = []
    
    # Start shared HTTP server for dark mode if needed
    server_thread = None
    if dark_mode:
        import http.server
        import socketserver
        import threading
        import time
        
        def start_server():
            PORT = 8000
            Handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                httpd.serve_forever()
        
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        time.sleep(2)
    
    try:
        for i, eml_file in enumerate(eml_files, 1):
            print(f"Processing {i}/{len(eml_files)}: {os.path.basename(eml_file)}")
            result = convert_to_png(eml_file, dark_mode, output_dir, shared_server=dark_mode)
            if result:
                converted_files.append(result)
    finally:
        # Clean up server if it was started
        if server_thread and server_thread.is_alive():
            # The server will be cleaned up when the thread ends
            pass
    
    print(f"Successfully converted {len(converted_files)} files to PNG")
    return converted_files

def convert_to_html(eml_file, dark_mode=False, output_dir=None):
    """Convert .eml to HTML file"""
    html_content = extract_html_from_eml(eml_file)
    
    if html_content:
        # Get just the filename without path
        eml_filename = os.path.basename(eml_file)
        output_filename = eml_filename.replace('.eml', '.html')
        
        # Use output directory if specified
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            output_filename = os.path.join(output_dir, output_filename)
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Converted {eml_file} to {output_filename}")
        return output_filename
    else:
        print(f"No HTML content found in {eml_file}")
        return None

def convert_to_pdf(eml_file, dark_mode=False, output_dir=None, shared_server=False):
    """Convert .eml to PDF using browser rendering (Edge-like)"""
    try:
        from playwright.sync_api import sync_playwright
        import tempfile
        
        # Extract HTML content and create temporary HTML file
        html_content = extract_html_from_eml(eml_file)
        if not html_content:
            print(f"No HTML content found in {eml_file}")
            return None
        
        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_html:
            temp_html.write(html_content)
            temp_html_path = temp_html.name
        
        # For dark mode, copy the temp file to current directory so HTTP server can serve it
        if dark_mode:
            import shutil
            local_temp_path = os.path.join(os.getcwd(), f"temp_{os.path.basename(temp_html_path)}")
            shutil.copy2(temp_html_path, local_temp_path)
            temp_html_path = local_temp_path
        
        # Use Playwright to render like Edge and save as PDF
        with sync_playwright() as p:
            if dark_mode and not shared_server:
                # Use Chrome with Dark Reader extension and local server
                import http.server
                import socketserver
                import threading
                import time
                
                # Start local server for Dark Reader
                def start_server():
                    PORT = 8000
                    Handler = http.server.SimpleHTTPRequestHandler
                    with socketserver.TCPServer(("", PORT), Handler) as httpd:
                        httpd.serve_forever()
                
                server_thread = threading.Thread(target=start_server, daemon=True)
                server_thread.start()
                time.sleep(2)
                
                extension_path = os.path.abspath("./extensions/dark-reader")
                browser = p.chromium.launch_persistent_context(
                    user_data_dir="./browser_data",
                    headless=True,
                    args=[
                        f"--load-extension={extension_path}",
                        f"--disable-extensions-except={extension_path}",
                        "--allow-running-insecure-content",
                        "--disable-web-security"
                    ]
                )
                page = browser.new_page()
            else:
                # Regular browser for light mode
                browser = p.chromium.launch()
                page = browser.new_page()
            
            # Load the HTML file
            if dark_mode:
                # Use HTTP server for Dark Reader - only use the filename, not the full path
                page.goto(f'http://localhost:8000/{os.path.basename(temp_html_path)}', wait_until='domcontentloaded')
            else:
                # Use file:// for regular mode
                page.goto(f'file://{os.path.abspath(temp_html_path)}', wait_until='domcontentloaded')
            
            # Wait for content to load with shorter timeout and fallback
            try:
                page.wait_for_load_state('networkidle', timeout=10000)
            except:
                # If networkidle times out, try domcontentloaded instead
                try:
                    page.wait_for_load_state('domcontentloaded', timeout=5000)
                except:
                    # If that also fails, just wait a bit and continue
                    page.wait_for_timeout(2000)
            
            # Enable Dark Reader if requested
            if dark_mode:
                page.evaluate("""
                    // Force enable Dark Reader and keep it enabled
                    function enableDarkReader() {
                        if (window.DarkReader && window.DarkReader.enable) {
                            window.DarkReader.enable({
                                brightness: 100,
                                contrast: 100,
                                sepia: 0
                            });
                            console.log('Dark Reader enabled with settings!');
                            return true;
                        } else {
                            console.log('Dark Reader not found, using CSS fallback');
                            const style = document.createElement('style');
                            style.id = 'force-dark-mode';
                            style.textContent = `
                                html { filter: invert(1) hue-rotate(180deg) !important; }
                                img, video, picture, svg { filter: invert(1) hue-rotate(180deg) !important; }
                                [style*="background"] { filter: invert(1) hue-rotate(180deg) !important; }
                            `;
                            document.head.appendChild(style);
                            return false;
                        }
                    }
                    
                    // Try multiple times to ensure it sticks
                    setTimeout(enableDarkReader, 500);
                    setTimeout(enableDarkReader, 1500);
                    setTimeout(enableDarkReader, 3000);
                    
                    // Monitor for changes and re-enable if needed
                    setInterval(() => {
                        if (window.DarkReader && !window.DarkReader.isEnabled()) {
                            enableDarkReader();
                            console.log('Re-enabled Dark Reader');
                        }
                    }, 1000);
                """)
                # Wait for Dark Reader to apply
                page.wait_for_timeout(5000)
                
                # Before PDF generation, inject print-friendly dark CSS
                # This works around Chrome disabling extensions during print/PDF
                page.evaluate("""
                    console.log('Adding print-friendly dark mode CSS...');
                    
                    // Remove any conflicting styles
                    const existingStyles = document.querySelectorAll('#force-dark-mode, #dark-mode-fallback');
                    existingStyles.forEach(style => style.remove());
                    
                    // Add CSS that works specifically for print/PDF
                    const printStyle = document.createElement('style');
                    printStyle.id = 'print-dark-mode';
                    printStyle.textContent = `
                        @media screen, print {
                            html, body {
                                background-color: #1a1a1a !important;
                                color: #ffffff !important;
                                filter: invert(1) hue-rotate(180deg) !important;
                            }
                            
                            /* Force all text to be white */
                            *, p, span, div, td, th, h1, h2, h3, h4, h5, h6 {
                                color: #ffffff !important;
                                background-color: transparent !important;
                            }
                            
                            /* Keep images normal - don't invert them */
                            img, video, picture, svg, canvas {
                                filter: none !important;
                            }
                            
                            /* Force browsers to print background colors */
                            * {
                                -webkit-print-color-adjust: exact !important;
                                color-adjust: exact !important;
                                print-color-adjust: exact !important;
                            }
                        }
                    `;
                    document.head.appendChild(printStyle);
                    console.log('Print-friendly dark mode CSS added');
                """)
                page.wait_for_timeout(2000)
            
            # Generate PDF with Edge-like settings
            eml_filename = os.path.basename(eml_file)
            pdf_filename = eml_filename.replace('.eml', '.pdf')
            
            # Use output directory if specified
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                pdf_filename = os.path.join(output_dir, pdf_filename)
            
            page.pdf(
                path=pdf_filename,
                format='A4',
                print_background=True,
                prefer_css_page_size=False
            )
            
            browser.close()
            
        # Clean up temporary HTML file
        try:
            os.unlink(temp_html_path)
            # Also clean up the local copy if it was created
            if dark_mode and temp_html_path != temp_html.name:
                try:
                    os.unlink(temp_html.name)
                except:
                    pass
        except:
            pass
            
        print(f"Converted {eml_file} to {pdf_filename}")
        return pdf_filename
        
    except ImportError:
        print("Playwright not installed. Installing...")
        os.system("pip install playwright")
        os.system("playwright install chromium")
        print("Please run the script again.")
        return None
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return None

def convert_to_png(eml_file, dark_mode=False, output_dir=None, shared_server=False):
    """Convert .eml to PNG screenshot using browser rendering"""
    try:
        from playwright.sync_api import sync_playwright
        import tempfile
        
        # Extract HTML content and create temporary HTML file
        html_content = extract_html_from_eml(eml_file)
        if not html_content:
            print(f"No HTML content found in {eml_file}")
            return None
        
        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_html:
            temp_html.write(html_content)
            temp_html_path = temp_html.name
        
        # For dark mode, copy the temp file to current directory so HTTP server can serve it
        if dark_mode:
            import shutil
            local_temp_path = os.path.join(os.getcwd(), f"temp_{os.path.basename(temp_html_path)}")
            shutil.copy2(temp_html_path, local_temp_path)
            temp_html_path = local_temp_path
        
        # Use Playwright to render like Edge and save as PNG
        with sync_playwright() as p:
            if dark_mode and not shared_server:
                # Use Chrome with Dark Reader extension and local server
                import http.server
                import socketserver
                import threading
                import time
                
                # Start local server for Dark Reader
                def start_server():
                    PORT = 8000
                    Handler = http.server.SimpleHTTPRequestHandler
                    with socketserver.TCPServer(("", PORT), Handler) as httpd:
                        httpd.serve_forever()
                
                server_thread = threading.Thread(target=start_server, daemon=True)
                server_thread.start()
                time.sleep(2)
                
                extension_path = os.path.abspath("./extensions/dark-reader")
                browser = p.chromium.launch_persistent_context(
                    user_data_dir="./browser_data",
                    headless=True,
                    args=[
                        f"--load-extension={extension_path}",
                        f"--disable-extensions-except={extension_path}",
                        "--allow-running-insecure-content",
                        "--disable-web-security"
                    ]
                )
                page = browser.new_page()
            else:
                # Regular browser for light mode
                browser = p.chromium.launch()
                page = browser.new_page()
            
            # Load the HTML file
            if dark_mode:
                # Use HTTP server for Dark Reader - only use the filename, not the full path
                page.goto(f'http://localhost:8000/{os.path.basename(temp_html_path)}', wait_until='domcontentloaded')
            else:
                # Use file:// for regular mode
                page.goto(f'file://{os.path.abspath(temp_html_path)}', wait_until='domcontentloaded')
            
            # Wait for content to load with shorter timeout and fallback
            try:
                page.wait_for_load_state('networkidle', timeout=10000)
            except:
                # If networkidle times out, try domcontentloaded instead
                try:
                    page.wait_for_load_state('domcontentloaded', timeout=5000)
                except:
                    # If that also fails, just wait a bit and continue
                    page.wait_for_timeout(2000)
            
            # Enable Dark Reader if requested
            if dark_mode:
                page.evaluate("""
                    // Force enable Dark Reader and keep it enabled
                    function enableDarkReader() {
                        if (window.DarkReader && window.DarkReader.enable) {
                            window.DarkReader.enable({
                                brightness: 100,
                                contrast: 100,
                                sepia: 0
                            });
                            console.log('Dark Reader enabled with settings!');
                            return true;
                        } else {
                            console.log('Dark Reader not found, using CSS fallback');
                            const style = document.createElement('style');
                            style.id = 'force-dark-mode';
                            style.textContent = `
                                html { filter: invert(1) hue-rotate(180deg) !important; }
                                img, video, picture, svg { filter: invert(1) hue-rotate(180deg) !important; }
                                [style*="background"] { filter: invert(1) hue-rotate(180deg) !important; }
                            `;
                            document.head.appendChild(style);
                            return false;
                        }
                    }
                    
                    // Try multiple times to ensure it sticks
                    setTimeout(enableDarkReader, 500);
                    setTimeout(enableDarkReader, 1500);
                    setTimeout(enableDarkReader, 3000);
                    
                    // Monitor for changes and re-enable if needed
                    setInterval(() => {
                        if (window.DarkReader && !window.DarkReader.isEnabled()) {
                            enableDarkReader();
                            console.log('Re-enabled Dark Reader');
                        }
                    }, 1000);
                """)
                # Wait for Dark Reader to apply
                page.wait_for_timeout(5000)
                
                # Before screenshot, inject print-friendly dark CSS
                # This ensures the screenshot captures the dark mode
                page.evaluate("""
                    console.log('Adding print-friendly dark mode CSS for screenshot...');
                    
                    // Remove any conflicting styles
                    const existingStyles = document.querySelectorAll('#force-dark-mode, #dark-mode-fallback');
                    existingStyles.forEach(style => style.remove());
                    
                    // Add CSS that works specifically for screenshots
                    const printStyle = document.createElement('style');
                    printStyle.id = 'print-dark-mode';
                    printStyle.textContent = `
                        @media screen, print {
                            html, body {
                                background-color: #1a1a1a !important;
                                color: #ffffff !important;
                                filter: invert(1) hue-rotate(180deg) !important;
                            }
                            
                            /* Force all text to be white */
                            *, p, span, div, td, th, h1, h2, h3, h4, h5, h6 {
                                color: #ffffff !important;
                                background-color: transparent !important;
                            }
                            
                            /* Keep images normal - don't invert them */
                            img, video, picture, svg, canvas {
                                filter: none !important;
                            }
                            
                            /* Force browsers to print background colors */
                            * {
                                -webkit-print-color-adjust: exact !important;
                                color-adjust: exact !important;
                                print-color-adjust: exact !important;
                            }
                        }
                    `;
                    document.head.appendChild(printStyle);
                    console.log('Print-friendly dark mode CSS added for screenshot');
                """)
                page.wait_for_timeout(2000)
                
                # Set viewport to match content size (remove white borders)
                content_size = page.evaluate("""
                    ({
                        width: document.documentElement.scrollWidth,
                        height: document.documentElement.scrollHeight
                    })
                """)
                page.set_viewport_size({
                    'width': content_size['width'],
                    'height': content_size['height']
                })
                
                # Force dark background on body and html to eliminate any white borders
                page.evaluate("""
                    document.documentElement.style.margin = '0';
                    document.documentElement.style.padding = '0';
                    document.body.style.margin = '0';
                    document.body.style.padding = '0';
                    document.documentElement.style.backgroundColor = '#1a1a1a';
                    document.body.style.backgroundColor = '#1a1a1a';
                """)
            
            # Take screenshot
            eml_filename = os.path.basename(eml_file)
            png_filename = eml_filename.replace('.eml', '.png')
            
            # Use output directory if specified
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                png_filename = os.path.join(output_dir, png_filename)
            
            page.screenshot(path=png_filename, full_page=True)
            
            browser.close()
            
        # Clean up temporary HTML file
        try:
            os.unlink(temp_html_path)
            # Also clean up the local copy if it was created
            if dark_mode and temp_html_path != temp_html.name:
                try:
                    os.unlink(temp_html.name)
                except:
                    pass
        except:
            pass
            
        print(f"Converted {eml_file} to {png_filename}")
        return png_filename
        
    except ImportError:
        print("Playwright not installed. Installing...")
        os.system("pip install playwright")
        os.system("playwright install chromium")
        print("Please run the script again.")
        return None
    except Exception as e:
        print(f"Error creating PNG: {e}")
        return None

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Single file:")
        print("    python eml-to-pdf-render.py --html <eml_file> [--dark] [--output-dir <dir>]")
        print("    python eml-to-pdf-render.py --pdf <eml_file> [--dark] [--output-dir <dir>]")
        print("    python eml-to-pdf-render.py --png <eml_file> [--dark] [--output-dir <dir>]")
        print("  Batch processing:")
        print("    python eml-to-pdf-render.py --batch-html <folder_path> [--dark] [--output-dir <dir>]")
        print("    python eml-to-pdf-render.py --batch-pdf <folder_path> [--dark] [--output-dir <dir>]")
        print("    python eml-to-pdf-render.py --batch-png <folder_path> [--dark] [--output-dir <dir>]")
        return
    
    option = sys.argv[1]
    target_path = sys.argv[2]
    dark_mode = "--dark" in sys.argv
    
    # Parse output directory
    output_dir = None
    if "--output-dir" in sys.argv:
        try:
            output_dir_index = sys.argv.index("--output-dir")
            if output_dir_index + 1 < len(sys.argv):
                output_dir = sys.argv[output_dir_index + 1]
        except ValueError:
            pass
    
    if not os.path.exists(target_path):
        print(f"Path not found: {target_path}")
        return
    
    # Handle batch processing
    if option.startswith("--batch-"):
        if option == "--batch-html":
            batch_convert_to_html(target_path, dark_mode, output_dir)
        elif option == "--batch-pdf":
            batch_convert_to_pdf(target_path, dark_mode, output_dir)
        elif option == "--batch-png":
            batch_convert_to_png(target_path, dark_mode, output_dir)
        else:
            print("Invalid batch option. Use --batch-html, --batch-pdf, or --batch-png")
        return
    
    # Handle single file processing
    if option == "--html":
        convert_to_html(target_path, dark_mode, output_dir)
    elif option == "--pdf":
        convert_to_pdf(target_path, dark_mode, output_dir)
    elif option == "--png":
        convert_to_png(target_path, dark_mode, output_dir)
    else:
        print("Invalid option. Use --html, --pdf, --png, --batch-html, --batch-pdf, or --batch-png")

if __name__ == "__main__":
    main()

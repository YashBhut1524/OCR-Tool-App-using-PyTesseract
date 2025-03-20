**OCR Tool using Python**  

This project is a simple OCR (Optical Character Recognition) tool built using Python and `pytesseract`. It allows users to extract text from images using two different methods:  

1. **Custom Snipping Tool** – Users can select a specific area of the screen to capture and extract text.
2. **Upload from Device** – Users can upload an image from their local storage for text extraction.  

This tool provides an easy way to recognize and extract text from images efficiently.

## Installation Guide

### 1. Download Tesseract OCR
- Visit the official Tesseract OCR GitHub page: [Tesseract OCR Download](https://github.com/tesseract-ocr/tesseract)
- Download the latest Windows installer (e.g., `tesseract-ocr-w64-setup-5.x.x.exe`).

### 2. Install Tesseract OCR
- Run the installer and follow these steps:
  - Select Language Data (default is English, but you can add more).
  - Choose Installation Path (default: `C:\Program Files\Tesseract-OCR`).
  - Complete the installation.

### 3. Add Tesseract to System Path
1. Open the Start Menu and search for **Environment Variables**.
2. Open **Edit system environment variables**.
3. Under **System Properties**, click **Environment Variables**.
4. Find **Path** in **System Variables** → Click **Edit**.
5. Click **New** → Add the following path:
   ```
   C:\Program Files\Tesseract-OCR
   ```
6. Click **OK** to save changes.

### 4. Verify Installation
- Open **Command Prompt (cmd)** and run:
  ```sh
  tesseract --version
  ```
- If installed correctly, it should display the Tesseract version.

### 5. Project Folder Structure
    
```
    OCR-Tool/
    │── __init__.py          # Makes the folder a package
    │── OCR_TOOL.py          # Main script for the OCR tool
    │── requirements.txt        # Required dependencies  
    │── README.md               # Documentation  
```
### 5. Install Dependencies
Make sure you have Python installed, then install required dependencies using:
```sh
  pip install -r requirements.txt

```

### 6. Update Python Code for Tesseract Path
Modify your Python script to specify the Tesseract path manually:
```python
import pytesseract

# Set Tesseract OCR path manually
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
```

### 7. Run the Snipping Tool
Execute the script using:
```sh
  python snipping_ocr_tool.py
```

### 8. Final Steps
- Restart your PC if necessary.
- Run the OCR script again.

---

import os
import json

def update_pdfs_json():
    pdfs_folder = os.path.join('src', 'assets', 'pdfs')
    pdfs_json_path = os.path.join('src', 'assets', 'pdfs.json')
    
    # Ensure the pdfs folder exists
    if not os.path.exists(pdfs_folder):
        os.makedirs(pdfs_folder)
    
    # Get list of PDF files
    pdf_files = [f for f in os.listdir(pdfs_folder) if f.endswith('.pdf')]
    
    # Update pdfs.json
    with open(pdfs_json_path, 'w') as json_file:
        json.dump(pdf_files, json_file, indent=4)

if __name__ == "__main__":
    update_pdfs_json()

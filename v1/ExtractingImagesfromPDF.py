import fitz  
import os

def extract_images_from_pdf(pdf_path, output_folder):
    # Creating output folder 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Determining PDF name for creating a subfolder
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Creating a subfolder for the PDF
    pdf_folder = os.path.join(output_folder, pdf_name)
    os.makedirs(pdf_folder, exist_ok=True)

    # Iterating over pages
    for page_number, page in enumerate(pdf_document):
        page_number +=1

        # Naming for the image
        if page_number == 1:
            image_filename = "Key.jpg"
        else:
            image_filename = f"Image_{page_number-1}.jpg"

        pix = page.get_pixmap(matrix=fitz.Identity, dpi=None, 
                                colorspace=fitz.csRGB, clip=None, annots=True)
        
        # Saving the image
        image_path = os.path.join(pdf_folder, image_filename)
        pix.save(image_path)
   

    pdf_document.close()


if __name__ == "__main__":
    
    pdf_filename = 'exampleScans.pdf'
    pdf_path = os.path.join(os.getcwd(), pdf_filename)
    
    output_folder = os.getcwd()

    extract_images_from_pdf(pdf_path, output_folder)

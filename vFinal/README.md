# BubbleScan-AI
A python module that uses AI to scan the bubbled responses from a Scantron sheet 95945.

### Workflow of AI module
- Extracts images from PDF
- Template matching: Aligns all the images according to the template.
- Crop the ROIs for each Image.
- Extract the bubbled responses from each ROI
- Save the data to JSON

### How to use the AI module 
- Import the Bubble Scan AI module

``` python
from Bubble_Scan_AI import Scantron95945
```

- Create a constructor for the class **Scantron95945** and pass the PDF path as parameter to this constructor.

``` python
pdf_path = 'PDF/Super30.pdf'
Scantron95945(pdf_path)
```
- The output data is stored in **"result_data.json"** file

**Note:** Bubble Scan AI module requires **template.jpg** image to be available in the root folder of this module. 
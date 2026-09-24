📄 Document Scanner

A lightweight document-scanning application built with Python, OpenCV, and Streamlit.

The project uses classical computer vision techniques only — no deep learning or neural networks.

The goal is to take a photograph of a receipt or printed page, automatically detect the document, correct its perspective, and produce a clean black-and-white scanned version.

✨ Features

Upload JPG, JPEG, or PNG images

Detect document/page boundaries automatically

Detect page corners using OpenCV contours

Correct perspective using a homography transformation

Convert the document into a clean black-and-white scan

Adaptive thresholding for uneven lighting

Download the processed document as a PNG

Computer-vision debug views for troubleshooting

🧠 How It Works

The scanner follows a traditional computer-vision pipeline:

                    Input Image
                         │
                         ▼
                 Grayscale Image
                         │
                         ▼
                  Gaussian Blur
                         │
                         ▼
                   Edge Detection
                      (Canny)
                         │
                         ▼
                    Morphology
                         │
                         ▼
                    Contours
                         │
                         ▼
              Four-Corner Detection
                         │
                         ▼
              Perspective Transformation
                         │
                         ▼
                   Flattened Page
                         │
                         ▼
                Adaptive Thresholding
                         │
                         ▼
                  Final B&W Scan

📁 Project Structure
document-scanner/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── scanner/
    ├── __init__.py
    ├── preprocessing.py
    ├── detection.py
    ├── perspective.py
    └── thresholding.py

File Description
File	Purpose
app.py	Streamlit application and user interface
scanner/detection.py	Document/page detection
scanner/perspective.py	Perspective correction
scanner/thresholding.py	Black-and-white conversion
scanner/preprocessing.py	Image preprocessing utilities
requirements.txt	Python dependencies
README.md	Project documentation
🛠️ Technologies

Python

OpenCV

NumPy

Streamlit

No deep learning model is used.

⚙️ Installation
1. Clone or download the project

Open PowerShell in the project directory.

2. Create a virtual environment
python -m venv .venv


Activate it:

.venv\Scripts\Activate.ps1


If PowerShell blocks script execution, you can use:

.venv\Scripts\python.exe -m pip install -r requirements.txt

3. Install dependencies
python -m pip install -r requirements.txt


The required packages are:

streamlit
opencv-python
numpy

▶️ Running the Application

Start the Streamlit application with:

python -m streamlit run app.py


The application will open in your browser.

If it does not open automatically, Streamlit will provide a local URL in the terminal.

📷 Usage

Open the application.

Upload a photograph of a receipt or printed page.

The application detects the document boundary.

The detected corners are displayed.

The page is perspective-corrected.

The corrected page is converted into a black-and-white scan.

Download the resulting PNG.

🔍 Debugging

The application includes computer-vision debug images.

These can show:

Grayscale image

Canny edge image

Adaptive threshold

Otsu threshold

Detected page corners

This is useful when the page cannot be detected.

The detection pipeline can fail when:

The page blends into the background.

The page boundary is not visible.

The image is too dark or overexposed.

The page is heavily occluded.

One or more corners are outside the photograph.

Background objects create stronger contours than the page.

📐 Perspective Correction

After detecting four page corners, the scanner uses a perspective transformation.

The photographed page may look like:

       __________________
      /                 /
     /                 /
    /_________________/


The transformation maps it to:

    __________________
   |                  |
   |                  |
   |                  |
   |__________________|


This produces a flat, top-down representation of the document.

🖤 Binarization

The final document is converted to black and white using adaptive thresholding.

Adaptive thresholding is useful because photographs can contain:

Shadows

Uneven illumination

Bright spots

Dark edges

Instead of using one global threshold for the entire image, adaptive thresholding calculates a threshold locally.

🚫 No Deep Learning

This project intentionally avoids:

CNNs

YOLO

U-Net

Transformers

OCR models

Document segmentation models

The document detection is based entirely on traditional computer-vision techniques such as:

Grayscale conversion

Gaussian blur

Canny edge detection

Morphological operations

Contour detection

Polygon approximation

Homography/perspective transformation

Adaptive thresholding

🔮 Possible Improvements

Future versions could improve detection with additional classical computer-vision techniques:

Hough line detection

Line intersection

Better quadrilateral scoring

Automatic shadow removal

Contrast enhancement

Deskewing

Morphological noise removal

Multiple document detection

Receipt-specific detection

OCR integration

PDF export

📌 Limitations

The current scanner works best when:

The complete document is visible.

The document has a reasonably clear boundary.

There is contrast between the document and its background.

The document is approximately rectangular.

Very complex backgrounds or heavily folded/occluded documents may require additional detection logic.

📄 License

This project is intended for educational and experimental use.

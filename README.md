# AI-Based Pothole Detection Using YOLO — RoadSight AI

An automated pothole detection project that experimentally compares four Ultralytics YOLO configurations on a labelled road-surface dataset and integrates the best overall trained model (**YOLO26s at 640 resolution**) into **RoadSight AI**, a local Flask-based web application for interactive pothole detection and visualization.

---

## Project Objective

The objective of this project is to automatically detect potholes in road images using deep learning and computer vision. The local web application:
- Accepts road images via file upload or drag-and-drop.
- Runs inference using the trained **YOLO26s** model checkpoint (`best.pt`).
- Draws bounding boxes around detected potholes with confidence scores.
- Displays the total detection count, per-detection confidence breakdown, and inference/processing time.
- Allows users to download the annotated output image.

---

## Dataset Details

- **Original Dataset Archive:** `Pothole.v1-raw.yolov8.zip`
- **Colab Directory:** `/content/pothole_dataset`
- **Configuration File:** `/content/pothole_dataset/data.yaml`
- **Number of Classes:** `1` (`pothole`)

| Dataset Split | Number of Images |
| :--- | :---: |
| Training | 465 |
| Validation | 133 |
| Testing | 67 |
| **Total** | **665** |

> **Note:** Image counts and pothole object-instance (annotation) counts are different, as a single road image can contain multiple pothole annotations.

---

## Model Comparison & Experimental Results

Four YOLO configurations were trained and evaluated on the 67-image test split:

| Model Configuration | Precision | Recall | mAP@50 | mAP@50–95 | Inference Time |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **YOLOv8s (640)** | **83.77%** | 67.02% | 78.58% | 50.79% | **9.3 ms** |
| **YOLOv8s (800)** | 69.70% | 71.70% | 71.92% | 46.27% | 15.0 ms |
| **YOLO11s (640)** | 80.05% | 70.13% | 80.55% | 53.81% | 11.7 ms |
| **YOLO26s (640)** | 83.59% | **75.32%** | **83.08%** | **54.51%** | ~10.4 ms |

### Key Takeaways
- **YOLO26s (640)** achieved the highest **mAP@50 (83.08%)**, highest **mAP@50–95 (54.51%)**, and highest **Recall (75.32%)**, with an inference time of approximately **10.4 ms**.
- **YOLOv8s (640)** achieved the highest **Precision (83.77%)** and the lowest **Inference Time (9.3 ms)**.
- **YOLO26s (640)** was selected as the best overall model for the Flask web application based on the combined accuracy and recall metrics, though it did not lead in every individual metric.

> **Metric Clarification:** An mAP@50 of 83.08% summarizes the precision–recall curve at an IoU threshold of 0.50; it does not mean the model detects 83.08% of all potholes. Recall (75.32%) more directly represents the proportion of actual potholes detected. Inference times depend on the hardware and software environment.

### Recorded Training Configurations
- **YOLO26s (640):** Image size `640`, Epochs `100`, Batch size `16`, Patience `20`, Device `GPU 0`, Seed `42`.
- **YOLOv8s (800):** Max epochs `150`, Image size `800`, Batch size `8`, Optimizer `AdamW`, Learning rate `0.001`, Patience `30` (early stopping triggered at epoch `81`; best checkpoint at epoch `51`).

---

## Diagnostic Error Analysis & Threshold Selection

In addition to official Ultralytics evaluation metrics, a custom one-to-one matching diagnostic analysis was performed at **IoU 0.50**:

| Diagnostic Metric (Custom IoU 0.50 Matching) | Value |
| :--- | :---: |
| True Positives (TP) | 123 |
| False Positives (FP) | 41 |
| False Negatives (FN) | 31 |
| Custom Precision | 75.00% |
| Custom Recall | 79.87% |
| Custom F1-Score | 77.35% |

- These custom diagnostic values are distinct from the official Ultralytics metrics in the comparison table above.
- **Detection Coverage:** At confidence `0.25`, 65 out of 67 test images produced at least one predicted box. Two test images produced no predictions despite containing one ground-truth pothole each:
  - `img-264_jpg.rf.a98f3f39b1afdea9ce3155bbe107c6c1.jpg`
  - `img-343_jpg.rf.64b8e5ed7aa9153427c52de5812b3ab2.jpg`
- **Confidence Threshold Selection:** The F1-confidence curve peaked at approximately **0.80** at a confidence threshold of **0.499**. The Flask app uses `~0.499` as its operational filtering threshold (this is a score-filtering cutoff, not a calibrated probability guarantee).
- **Generated Diagnostic Outputs:** Confusion matrix, normalized confusion matrix, precision–recall curve, F1-confidence curve, and training results graphs.

---

## RoadSight AI — Flask Web Application

### Technology Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask, Werkzeug
- **AI & Image Processing:** YOLO26s, Ultralytics, OpenCV, Pillow, NumPy

### Implemented Features
1. Standard file upload and drag-and-drop image upload.
2. Support for `JPG`, `JPEG`, `PNG`, and `WEBP` formats (maximum file size: **12 MB**).
3. Trained YOLO26s inference loaded once at server startup (`imgsz=640`, confidence threshold `~0.499`).
4. Annotated bounding-box visualization with confidence scores.
5. Detection count, inference/processing time, and per-detection confidence breakdown.
6. One-click download of the annotated output image.
7. Responsive dark-themed web interface.

### Project Folder Structure

```text
Pothole_Detection_Flask/
│
├── app.py
├── best.pt
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    ├── uploads/
    └── results/
```

---

## Setup & Running Locally (Windows)

### 1. Place the Trained Model Checkpoint
Copy your trained YOLO26s checkpoint from Google Drive:
```text
/content/drive/MyDrive/Pothole_Research/Models/YOLO26s_640.pt
```
Paste it directly into the `Pothole_Detection_Flask/` root directory and rename it to **`best.pt`**.  
*(Do not place `best.pt` inside `static/` or `templates/`, and do not substitute a generic pretrained YOLO checkpoint.)*

### 2. Create and Activate a Virtual Environment
Open `Pothole_Detection_Flask/` in VS Code and run in the terminal:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Alternatively, using Command Prompt (`cmd`):
```cmd
venv\Scripts\activate.bat
```

### 3. Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the Flask Server
```powershell
python app.py
```

Open your browser and go to:
```text
[http://127.0.0.1:5000](http://127.0.0.1:5000)
```

---

## Limitations

- **Shared Test Split:** All four model configurations were evaluated on the same 67-image test split. An independent, untouched holdout test set would provide a less biased final generalization estimate.
- **Local Demonstration:** RoadSight AI is currently built and verified as a local Flask application, not a publicly deployed production web service.
- **Hardware Dependence:** Recorded inference latencies depend on the underlying GPU/CPU and software stack.

---

## Future Scope (Not Yet Implemented)

- GPS-based pothole location tagging.
- Real-time video and dashcam stream detection.
- Pothole severity classification.
- Database integration for storing inspection logs and history.
- Interactive road maintenance dashboard.
- Mobile application deployment.

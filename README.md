# RoadSight AI — YOLO26s Pothole Detection

A dark-themed local Flask application for your trained YOLO26s pothole detector.

## IMPORTANT: Add your trained model

The ZIP does not include `best.pt` because the trained checkpoint is in your Google Drive and is not accessible to this packaging environment.

1. Download `YOLO26s_640.pt` from Google Drive: `My Drive / Pothole_Research / Models / YOLO26s_640.pt`.
2. Copy it beside `app.py`.
3. Rename it exactly to `best.pt`.

Use your trained checkpoint, not the generic pretrained `yolo26s.pt`.

## Windows / VS Code setup

Open this folder in VS Code. In the terminal:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Or use Command Prompt: `venv\\Scripts\\activate.bat`

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run:

```powershell
python app.py
```

Open `http://127.0.0.1:5000`.

## Included features

- Dark responsive interface
- Image upload (JPG/JPEG/PNG/WEBP, max 12 MB)
- YOLO26s inference at image size 640
- Confidence threshold 0.499 (from your F1-confidence experiment)
- Annotated image with bounding boxes
- Pothole count, processing time and mean confidence
- Per-detection confidence breakdown
- Download annotated result

The model loads once when Flask starts. If you add or replace `best.pt`, restart the app. Uploaded images and results are stored in `static/uploads` and `static/results`.

This is a local demo. Do not expose Flask's development server directly to the public internet.

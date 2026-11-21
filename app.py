import os, time, uuid
from pathlib import Path
import cv2
from flask import Flask, render_template, request, send_from_directory, url_for, flash, redirect
from werkzeug.utils import secure_filename
from ultralytics import YOLO

BASE = Path(__file__).resolve().parent
UPLOADS, RESULTS = BASE/"static/uploads", BASE/"static/results"
MODEL_PATH = BASE/"best.pt"
UPLOADS.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "local-demo-change-me")
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024
ALLOWED = {"jpg", "jpeg", "png", "webp"}
CONF = 0.499
IMGSZ = 640

model, model_error = None, None
try:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Copy your trained YOLO26s_640.pt into this folder and rename it best.pt.")
    model = YOLO(str(MODEL_PATH))
except Exception as e:
    model_error = str(e)
    print("[MODEL ERROR]", model_error)

def allowed_file(name):
    return "." in name and name.rsplit(".", 1)[1].lower() in ALLOWED

@app.get("/")
def index():
    return render_template("index.html", model_ready=model is not None, model_error=model_error)

@app.post("/detect")
def detect():
    if model is None:
        flash("YOLO26s is not loaded. Add best.pt beside app.py and restart Flask.", "error")
        return redirect(url_for("index"))
    if "image" not in request.files or not request.files["image"].filename:
        flash("Please choose an image.", "error")
        return redirect(url_for("index"))
    f = request.files["image"]
    if not allowed_file(f.filename):
        flash("Upload JPG, JPEG, PNG or WEBP only.", "error")
        return redirect(url_for("index"))

    original = secure_filename(f.filename)
    uid = uuid.uuid4().hex[:10]
    stem, ext = Path(original).stem[:55], Path(original).suffix.lower()
    upload_name = f"{stem}_{uid}{ext}"
    result_name = f"detected_{stem}_{uid}.jpg"
    upload_path, result_path = UPLOADS/upload_name, RESULTS/result_name
    f.save(upload_path)

    try:
        start = time.perf_counter()
        prediction = model.predict(str(upload_path), imgsz=IMGSZ, conf=CONF, verbose=False)[0]
        elapsed = (time.perf_counter() - start) * 1000
        boxes = prediction.boxes
        count = len(boxes) if boxes is not None else 0
        confs = boxes.conf.tolist() if count else []
        annotated = prediction.plot()
        if not cv2.imwrite(str(result_path), annotated):
            raise RuntimeError("Could not save annotated image.")
        detections = []
        if boxes is not None:
            for box in boxes:
                cid = int(box.cls.item())
                name = model.names.get(cid, str(cid)) if isinstance(model.names, dict) else str(cid)
                detections.append({"name": name, "confidence": round(float(box.conf.item())*100, 1)})
        detections.sort(key=lambda x: x["confidence"], reverse=True)
        return render_template("index.html", model_ready=True, model_error=None,
            result_image=url_for("static", filename=f"results/{result_name}"),
            download_url=url_for("download", filename=result_name),
            original_name=original, pothole_count=count, processing_ms=round(elapsed,1),
            mean_confidence=round(sum(confs)/len(confs)*100,1) if confs else 0,
            detections=detections)
    except Exception as e:
        app.logger.exception("Detection failed")
        flash(f"Detection failed: {e}", "error")
        return redirect(url_for("index"))

@app.get("/download/<path:filename>")
def download(filename):
    return send_from_directory(RESULTS, filename, as_attachment=True)

@app.errorhandler(413)
def too_large(_):
    flash("Image is too large. Maximum size is 12 MB.", "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

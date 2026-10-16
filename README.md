# SchistoScan — Parasite Egg Detection

Decision-support tool that detects parasite eggs in microscopy images
using a trained YOLO11n object detection model. Detects 4 species:
*Schistosoma mansoni*, *Ascaris lumbricoides*, *Trichuris trichiura*,
and Hookworm.

## ⚠️ Scope

SchistoScan is a decision-support tool, not a diagnostic device.
All findings must be confirmed by a qualified microscopist before
any treatment decision. It is validated on stool microscopy for
intestinal schistosomiasis caused by S. mansoni.

## 📊 Model Performance

| Metric | Value |
|---|---|
| mAP50 (all species) | 0.973 |
| mAP50-95 (all species) | 0.927 |
| Precision (all) | 0.944 |
| Recall (all) | 0.928 |

Per-species performance:

| Species | Precision | Recall | mAP50 |
|---|---|---|---|
| S. mansoni | 0.945 | 0.881 | 0.961 |
| Ascaris lumbricoides | 0.964 | 0.962 | 0.984 |
| Trichuris trichiura | 0.963 | 0.952 | 0.987 |
| Hookworm | 0.906 | 0.917 | 0.960 |

## 🖥️ Features

- Clinical Assessment page with three-tier triage
- WHO intensity interpretation
- Species breakdown with full medical names
- Annotated microscopy image with bounding boxes
- Downloadable PDF clinical report
- 10 demo images per species for instant testing

## 🚀 Tech Stack

- YOLO11n object detection (2.59M params)
- Ultralytics + PyTorch
- Streamlit web interface
- Matplotlib PDF report generation
- Pillow / OpenCV image handling

## 📦 Installation

    git clone https://github.com/mrselemogo777-gif/schistoscan.git
    cd schistoscan
    pip install -r requirements.txt
    streamlit run app.py

## 🗂️ Project Structure

    schistoscan/
    ├── app.py                    # Home — Clinical Assessment
    ├── pages/                    # Additional pages
    ├── services/                 # Core logic
    │   ├── detector.py           # YOLO wrapper
    │   ├── risk.py               # Tier classification
    │   ├── report.py             # PDF report builder
    │   └── pipeline.py           # Orchestration
    ├── ui/                       # UI components
    ├── models/best.pt            # Trained YOLO11n weights
    └── data/demo/                # Demo samples per species

## 🔬 Future Work

- Extend to S. haematobium (urinary schistosomiasis)
- Field validation on Botswana microscopy samples
- Mobile-friendly inference for field deployment

## 👤 Author

Legakwa Selemogo · [GitHub](https://github.com/mrselemogo777-gif)

## License

MIT

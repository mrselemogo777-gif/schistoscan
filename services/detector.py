"""YOLO-based egg detector for microscopy images.

Wraps the trained YOLO11n model and returns structured detections.
"""
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
from ultralytics import YOLO

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "best.pt"

# Human-readable names for the class codes
SPECIES_NAMES = {
    "ASC.": "Ascaris lumbricoides",
    "TRI.": "Trichuris trichiura",
    "HKW.": "Hookworm",
    "SCH.": "Schistosoma mansoni",
}

# Short names for display
SHORT_NAMES = {
    "ASC.": "Ascaris",
    "TRI.": "Trichuris",
    "HKW.": "Hookworm",
    "SCH.": "S. mansoni",
}


class EggDetector:
    """Loads the YOLO model once and runs inference on demand."""

    def __init__(self):
        self.model = YOLO(str(MODEL_PATH))

    
    # Public API
    def detect(self, image_path: str, conf_threshold: float = 0.25) -> Dict[str, Any]:
        """Run detection on one image.

        Parameters
        ----------
        image_path : str
            Path to a PNG or JPG microscopy image.
        conf_threshold : float
            Minimum detection confidence (0-1).

        Returns
        -------
        dict with keys:
            detections  — list of {class_code, class_name, confidence, bbox}
            annotated   — the image with bounding boxes drawn (numpy array)
            count       — total number of detected eggs
        """
        results = self.model(image_path, conf=conf_threshold)
        result  = results[0]

        detections = []
        for box in result.boxes:
            cls_id  = int(box.cls[0])
            cls_code = self.model.names[cls_id]
            detections.append({
                "class_code": cls_code,
                "class_name": SPECIES_NAMES.get(cls_code, cls_code),
                "short_name": SHORT_NAMES.get(cls_code, cls_code),
                "confidence": float(box.conf[0]),
                "bbox":       box.xyxy[0].tolist(),  # [x1, y1, x2, y2]
            })

        return {
            "detections": detections,
            "annotated":  result.plot(),   # numpy array, already boxed
            "count":      len(detections),
        }

    
    # Convenience
    @staticmethod
    def species_summary(detections: List[Dict]) -> Dict[str, int]:
        """Count detections per species."""
        summary = {}
        for d in detections:
            key = d["short_name"]
            summary[key] = summary.get(key, 0) + 1
        return summary

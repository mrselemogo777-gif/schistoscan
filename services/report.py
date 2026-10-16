"""Generate a clinical PDF report using matplotlib's PDF backend.

Avoids installing reportlab — uses only matplotlib + Pillow, both
already installed.
"""
from datetime import datetime
from io import BytesIO
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image


class ClinicalReport:
    """Builds a single-page PDF clinical report."""

    def __init__(self, patient_id: str, sample_type: str, method: str):
        self.patient_id  = patient_id or "ANON"
        self.sample_type = sample_type
        self.method      = method
        self.timestamp   = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    
    # Public
    def build(self, infection, detections: List[Dict], annotated_image) -> bytes:
        """Return a PDF as bytes ready for st.download_button."""
        buf = BytesIO()
        with PdfPages(buf) as pdf:
            fig = plt.figure(figsize=(8.5, 11))
            fig.patch.set_facecolor("white")

            # Header
            self._draw_header(fig)

            # Patient info
            self._draw_patient_info(fig)

            # Result
            self._draw_result(fig, infection)

            # Species breakdown
            self._draw_species(fig, infection)

            # Annotated image
            self._draw_image(fig, annotated_image)

            # Recommended action
            self._draw_action(fig, infection)

            # Disclaimer
            self._draw_footer(fig)

            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

        buf.seek(0)
        return buf.getvalue()

    
    # Drawing helpers
    def _draw_header(self, fig) -> None:
        fig.text(0.5, 0.96, "SchistoScan — Clinical Report",
                 ha="center", va="top", fontsize=18, fontweight="bold",
                 color="#0e7490")
        fig.text(0.5, 0.935, "Parasite Egg Detection · Decision-Support Only",
                 ha="center", va="top", fontsize=10, color="#155e75")

        # Separator line
        fig.add_artist(plt.Line2D([0.08, 0.92], [0.92, 0.92],
                                   color="#0e7490", linewidth=1.5))

    def _draw_patient_info(self, fig) -> None:
        y = 0.88
        fig.text(0.08, y, "Patient Information", fontsize=12,
                 fontweight="bold", color="#155e75")
        y -= 0.025
        fig.text(0.08, y, f"Patient ID:      {self.patient_id}", fontsize=10)
        y -= 0.02
        fig.text(0.08, y, f"Sample type:     {self.sample_type}", fontsize=10)
        y -= 0.02
        fig.text(0.08, y, f"Method:          {self.method}", fontsize=10)
        y -= 0.02
        fig.text(0.08, y, f"Report time:     {self.timestamp}", fontsize=10)

    def _draw_result(self, fig, infection) -> None:
        y = 0.74
        fig.text(0.08, y, "Detection Result", fontsize=12,
                 fontweight="bold", color="#155e75")

        y -= 0.04
        if infection.tier == "POSITIVE":
            color, label = "#b91c1c", "POSITIVE — Eggs detected at high confidence"
        elif infection.tier == "SUSPECTED":
            color, label = "#b45309", "SUSPECTED — Low-confidence detections, review manually"
        else:
            color, label = "#15803d", "NEGATIVE — No eggs detected above threshold"

        fig.text(0.08, y, label, fontsize=11, fontweight="bold", color=color)

        y -= 0.035
        fig.text(0.08, y, f"Total eggs detected:     {infection.total_eggs}", fontsize=10)
        y -= 0.02
        fig.text(0.08, y, f"Max confidence:          {infection.max_confidence:.1%}", fontsize=10)
        y -= 0.02
        fig.text(0.08, y, f"S. mansoni detected:     "
                          f"{'Yes' if infection.has_schistosoma else 'No'}", fontsize=10)

    def _draw_species(self, fig, infection) -> None:
        y = 0.52
        fig.text(0.08, y, "Species Breakdown", fontsize=12,
                 fontweight="bold", color="#155e75")
        y -= 0.025

        if infection.per_species:
            for species, count in infection.per_species.items():
                fig.text(0.10, y, f"• {species}: {count} egg(s)",
                         fontsize=10)
                y -= 0.02
        else:
            fig.text(0.10, y, "No eggs detected.", fontsize=10)

    def _draw_image(self, fig, annotated_image) -> None:
        """Embed the annotated microscopy image."""
        try:
            img = Image.fromarray(annotated_image)
            ax = fig.add_axes([0.20, 0.20, 0.60, 0.24])
            ax.imshow(img)
            ax.axis("off")
            fig.text(0.5, 0.44, "Annotated microscopy image",
                     ha="center", fontsize=9, style="italic", color="#475569")
        except Exception as e:
            fig.text(0.5, 0.30, f"(image embed failed: {e})",
                     ha="center", fontsize=9, color="#b91c1c")

    def _draw_action(self, fig, infection) -> None:
        y = 0.16
        fig.text(0.08, y, "Recommended Action", fontsize=12,
                 fontweight="bold", color="#155e75")
        y -= 0.025

        if infection.tier == "POSITIVE":
            lines = [
                "• Confirm the detection under a calibrated microscope.",
                "• If confirmed, follow national schistosomiasis treatment guidelines.",
                "• Report per Botswana MoH surveillance protocol.",
            ]
        elif infection.tier == "SUSPECTED":
            lines = [
                "• Re-image the sample with better focus and lighting.",
                "• Re-run with a lower confidence threshold.",
                "• Submit for manual microscopist review.",
            ]
        else:
            lines = [
                "• No eggs detected above the threshold.",
                "• If clinical suspicion persists, repeat sampling on a different day.",
            ]

        for line in lines:
            fig.text(0.10, y, line, fontsize=9.5)
            y -= 0.018

    def _draw_footer(self, fig) -> None:
        fig.add_artist(plt.Line2D([0.08, 0.92], [0.055, 0.055],
                                   color="#94a3b8", linewidth=0.8))
        fig.text(0.5, 0.04,
                 "⚠️ Decision-support only. Not a diagnosis. "
                 "All findings require human confirmation.",
                 ha="center", fontsize=8.5, style="italic",
                 color="#b91c1c")
        fig.text(0.5, 0.02,
                 "SchistoScan · YOLO11n · mAP50 = 0.973 · MIT License",
                 ha="center", fontsize=7.5, color="#64748b")

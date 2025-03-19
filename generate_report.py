import os
import uuid
from fpdf import FPDF

def generate_report(detections, detected_image_path):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    report_path = f"reports/report_{uuid.uuid4()}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Pothole Detection Report", ln=True, align='C')

    # Add detections to the report
    for detection in detections:
        pdf.cell(200, 10, txt=f"Pothole detected at {detection.boxes.xyxy.tolist()}", ln=True)

    # Add detected image
    pdf.image(detected_image_path, x=10, y=50, w=180)

    pdf.output(report_path)
    return report_path

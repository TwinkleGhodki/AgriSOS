from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def generate_prediction_report(
    farmer_name,
    crop,
    district,
    risk_level,
    risk_score,
    rainfall_deviation,
    temperature_stress,
    recommendations,
):
    """
    Generates a PDF report for one farmer prediction.
    Returns PDF bytes.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AgriSOS</b>", styles["Title"]))
    story.append(Paragraph("Farmer Distress Assessment Report", styles["Heading2"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>Farmer Name:</b> {farmer_name}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Crop:</b> {crop}", styles["BodyText"]))
    story.append(Paragraph(f"<b>District:</b> {district}", styles["BodyText"]))
    story.append(Spacer(1, 15))

    story.append(Paragraph(f"<b>Risk Level:</b> {risk_level}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Risk Score:</b> {risk_score}%", styles["BodyText"]))
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Weather Summary</b>", styles["Heading3"]))
    story.append(
        Paragraph(
            f"Rainfall Deviation: {rainfall_deviation:.1f}%",
            styles["BodyText"],
        )
    )
    story.append(
        Paragraph(
            f"Temperature Stress: {temperature_stress:.1f}°C",
            styles["BodyText"],
        )
    )

    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Recommended Actions</b>", styles["Heading3"]))

    for rec in recommendations:
        story.append(Paragraph(f"• {rec}", styles["BodyText"]))

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Generated automatically by AgriSOS",
            styles["Italic"],
        )
    )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf
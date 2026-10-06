"""
PDF report generator for PackSmart AI recommendations.
Uses ReportLab to produce a professional multi-page PDF document.
Returns raw PDF bytes (not a file path).
"""
from __future__ import annotations

import json
from io import BytesIO
from typing import Any, Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ──────────────────────────────────────────────────────────────────────────────
# Brand colours
# ──────────────────────────────────────────────────────────────────────────────
PRIMARY_GREEN = colors.HexColor("#16a34a")    # Tailwind green-600
NAVY = colors.HexColor("#1e3a5f")             # custom navy
LIGHT_GREEN = colors.HexColor("#dcfce7")      # green-100
LIGHT_GREY = colors.HexColor("#f3f4f6")       # grey-100
DARK_TEXT = colors.HexColor("#111827")        # grey-900
MID_TEXT = colors.HexColor("#374151")         # grey-700


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def generate_recommendation_pdf(
    recommendation,  # Recommendation ORM row
    food_profile,    # FoodProfile ORM row (may be None)
    user,            # User ORM row
) -> bytes:
    """
    Build a PackSmart AI recommendation PDF and return raw bytes.

    Parameters
    ----------
    recommendation : Recommendation ORM row
    food_profile   : FoodProfile ORM row
    user           : User ORM row

    Returns
    -------
    bytes
        Valid PDF byte string.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=2.0 * cm,
        bottomMargin=2.0 * cm,
        title="PackSmart AI — Packaging Recommendation Report",
        author="PackSmart AI",
    )

    styles = _build_styles()
    story = []

    # ── Header ──────────────────────────────────────────────────────────────
    story += _header_block(styles, recommendation, food_profile, user)
    story.append(Spacer(1, 0.4 * cm))

    # ── Food summary card ───────────────────────────────────────────────────
    if food_profile is not None:
        story += _food_summary_block(styles, food_profile)
        story.append(Spacer(1, 0.4 * cm))

    # ── Primary recommendation ───────────────────────────────────────────────
    story += _primary_recommendation_block(styles, recommendation)
    story.append(Spacer(1, 0.4 * cm))

    # ── Scores table ────────────────────────────────────────────────────────
    story += _scores_table(styles, recommendation)
    story.append(Spacer(1, 0.4 * cm))

    # ── Barrier properties ───────────────────────────────────────────────────
    story += _barrier_properties_block(styles, recommendation)
    story.append(Spacer(1, 0.4 * cm))

    # ── Shelf life ───────────────────────────────────────────────────────────
    story += _shelf_life_block(styles, recommendation)
    story.append(Spacer(1, 0.4 * cm))

    # ── AI explanation ──────────────────────────────────────────────────────
    story += _explanation_block(styles, recommendation)
    story.append(Spacer(1, 0.4 * cm))

    # ── Risk factors ────────────────────────────────────────────────────────
    story += _risk_factors_block(styles, recommendation)
    story.append(Spacer(1, 0.4 * cm))

    # ── Storage conditions ───────────────────────────────────────────────────
    story += _storage_block(styles, recommendation)
    story.append(Spacer(1, 0.6 * cm))

    # ── Disclaimer + footer ─────────────────────────────────────────────────
    story += _footer_block(styles)

    doc.build(story)
    return buffer.getvalue()


# ──────────────────────────────────────────────────────────────────────────────
# Style factory
# ──────────────────────────────────────────────────────────────────────────────

def _build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            fontName="Helvetica-Bold",
            fontSize=20,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=2,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            fontName="Helvetica",
            fontSize=10,
            textColor=PRIMARY_GREEN,
            alignment=TA_LEFT,
            spaceAfter=4,
        ),
        "section_header": ParagraphStyle(
            "SectionHeader",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=NAVY,
            spaceBefore=6,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body",
            fontName="Helvetica",
            fontSize=9,
            textColor=MID_TEXT,
            leading=14,
        ),
        "body_bold": ParagraphStyle(
            "BodyBold",
            fontName="Helvetica-Bold",
            fontSize=9,
            textColor=DARK_TEXT,
        ),
        "small": ParagraphStyle(
            "Small",
            fontName="Helvetica",
            fontSize=8,
            textColor=colors.grey,
        ),
        "small_center": ParagraphStyle(
            "SmallCenter",
            fontName="Helvetica",
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER,
        ),
        "highlight": ParagraphStyle(
            "Highlight",
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=PRIMARY_GREEN,
        ),
        "right": ParagraphStyle(
            "Right",
            fontName="Helvetica",
            fontSize=9,
            textColor=MID_TEXT,
            alignment=TA_RIGHT,
        ),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Section builders
# ──────────────────────────────────────────────────────────────────────────────

def _header_block(styles, recommendation, food_profile, user) -> list:
    elements = []

    # Logo-style text
    elements.append(Paragraph("PackSmart AI", styles["title"]))
    elements.append(Paragraph("AI-Powered Food Packaging Recommendation System", styles["subtitle"]))
    elements.append(
        HRFlowable(width="100%", thickness=2, color=PRIMARY_GREEN, spaceAfter=4)
    )

    # Report metadata table
    food_name = food_profile.food_name if food_profile else "N/A"
    generated_at = recommendation.created_at.strftime("%d %B %Y, %H:%M UTC") if recommendation.created_at else "N/A"
    prepared_for = getattr(user, "full_name", "N/A")

    meta_data = [
        ["Report ID:", str(recommendation.id)[:18] + "…", "Prepared for:", prepared_for],
        ["Food Item:", food_name, "Generated:", generated_at],
    ]
    meta_table = Table(meta_data, colWidths=[3.2 * cm, 8.0 * cm, 3.2 * cm, 5.0 * cm])
    meta_table.setStyle(
        TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
            ("TEXTCOLOR", (2, 0), (2, -1), NAVY),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ])
    )
    elements.append(meta_table)
    return elements


def _food_summary_block(styles, food_profile) -> list:
    elements = [Paragraph("Food Profile Summary", styles["section_header"])]

    category = food_profile.category.value if hasattr(food_profile.category, "value") else str(food_profile.category)
    perishability = food_profile.perishability.value if food_profile.perishability and hasattr(food_profile.perishability, "value") else "N/A"

    rows = [
        ["Food Name", food_profile.food_name, "Category", category.title()],
        ["Moisture Content", _fmt_pct(food_profile.moisture_content), "pH", _fmt_val(food_profile.ph)],
        ["Fat Content", _fmt_pct(food_profile.fat_content), "Protein Content", _fmt_pct(food_profile.protein_content)],
        ["Water Activity (aw)", _fmt_val(food_profile.water_activity), "Perishability", perishability.title()],
        ["O₂ Sensitivity", _fmt_sensitivity(food_profile.oxygen_sensitivity), "Moisture Sensitivity", _fmt_sensitivity(food_profile.moisture_sensitivity)],
        ["Light Sensitivity", _fmt_sensitivity(food_profile.light_sensitivity), "Temp Sensitivity", _fmt_sensitivity(food_profile.temperature_sensitivity)],
    ]

    table = Table(rows, colWidths=[4.5 * cm, 5.5 * cm, 4.5 * cm, 5.0 * cm])
    table.setStyle(_detail_table_style())
    elements.append(table)
    return elements


def _primary_recommendation_block(styles, recommendation) -> list:
    elements = [Paragraph("Primary Recommendation", styles["section_header"])]

    # Big material name
    if recommendation.primary_material:
        mat_name = recommendation.primary_material.name
    else:
        mat_name = "See details below"

    elements.append(Paragraph(mat_name, styles["highlight"]))
    elements.append(Spacer(1, 0.2 * cm))

    if recommendation.packaging_structure:
        elements.append(
            Paragraph(
                f"<b>Packaging Structure:</b> {recommendation.packaging_structure}",
                styles["body"],
            )
        )

    if recommendation.recommended_thickness_um:
        elements.append(
            Paragraph(
                f"<b>Recommended Thickness:</b> {recommendation.recommended_thickness_um:.1f} µm",
                styles["body"],
            )
        )

    return elements


def _scores_table(styles, recommendation) -> list:
    elements = [Paragraph("Score Summary", styles["section_header"])]

    scores = [
        ("Food Safety Score", recommendation.food_safety_score),
        ("Sustainability Score", recommendation.sustainability_score),
        ("Cost Score", recommendation.cost_score),
        ("Overall Score", recommendation.overall_score),
    ]

    data = [["Metric", "Score", "Rating"]]
    for label, score in scores:
        score_val = score or 0.0
        data.append([label, f"{score_val:.1f} / 100", _score_rating(score_val)])

    table = Table(data, colWidths=[7.0 * cm, 4.0 * cm, 4.5 * cm])
    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_GREEN, colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ])
    )
    elements.append(table)
    return elements


def _barrier_properties_block(styles, recommendation) -> list:
    elements = [Paragraph("Barrier Properties", styles["section_header"])]

    raw = recommendation.barrier_properties
    if isinstance(raw, str):
        try:
            props = json.loads(raw)
        except (ValueError, TypeError):
            props = {}
    elif isinstance(raw, dict):
        props = raw
    else:
        props = {}

    if not props:
        elements.append(Paragraph("No barrier data available.", styles["body"]))
        return elements

    label_map = {
        "moisture_barrier": "Moisture Barrier",
        "oxygen_barrier": "Oxygen Barrier",
        "light_barrier": "Light Barrier",
        "thermal_resistance": "Thermal Resistance",
        "mechanical_strength": "Mechanical Strength",
    }

    data = [["Barrier Property", "Score (0–1)", "Level"]]
    for key, label in label_map.items():
        val = props.get(key)
        if val is not None:
            data.append([label, f"{float(val):.2f}", _barrier_level(float(val))])

    if len(data) > 1:
        table = Table(data, colWidths=[6.5 * cm, 3.5 * cm, 4.0 * cm])
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_GREY, colors.white]),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ])
        )
        elements.append(table)

    return elements


def _shelf_life_block(styles, recommendation) -> list:
    elements = [Paragraph("Expected Shelf Life", styles["section_header"])]

    sl_min = recommendation.shelf_life_min_days or 0
    sl_max = recommendation.shelf_life_max_days or 0

    if sl_min and sl_max:
        text = f"<b>{sl_min}–{sl_max} days</b> ({sl_min // 30}–{sl_max // 30} months approx.)"
    else:
        text = "Not calculated."

    elements.append(Paragraph(text, styles["body"]))
    return elements


def _explanation_block(styles, recommendation) -> list:
    elements = [Paragraph("AI Recommendation Rationale", styles["section_header"])]
    explanation = recommendation.explanation or "No explanation available."
    elements.append(Paragraph(explanation, styles["body"]))
    return elements


def _risk_factors_block(styles, recommendation) -> list:
    elements = [Paragraph("Risk Factors", styles["section_header"])]

    raw = recommendation.risk_factors
    if isinstance(raw, str):
        try:
            risks = json.loads(raw)
        except (ValueError, TypeError):
            risks = []
    elif isinstance(raw, list):
        risks = raw
    else:
        risks = []

    if not risks:
        elements.append(Paragraph("No significant risk factors identified.", styles["body"]))
    else:
        for risk in risks:
            elements.append(Paragraph(f"• {risk}", styles["body"]))

    return elements


def _storage_block(styles, recommendation) -> list:
    elements = [Paragraph("Recommended Storage Conditions", styles["section_header"])]
    storage_text = recommendation.storage_conditions_recommended or "Follow product-specific guidelines."
    elements.append(Paragraph(storage_text, styles["body"]))
    return elements


def _footer_block(styles) -> list:
    elements = []
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceAfter=4))
    elements.append(
        Paragraph(
            "<b>Disclaimer:</b> This report is generated by PackSmart AI for informational purposes. "
            "Always validate packaging choices with certified food safety professionals before commercial deployment.",
            styles["small"],
        )
    )
    elements.append(Spacer(1, 0.2 * cm))
    elements.append(
        Paragraph(
            "PackSmart AI  ·  Ministry of Food Processing Industries (MoFPI)  ·  Smart India Hackathon 2026  ·  Problem ID 26236",
            styles["small_center"],
        )
    )
    return elements


# ──────────────────────────────────────────────────────────────────────────────
# Utility helpers
# ──────────────────────────────────────────────────────────────────────────────

def _detail_table_style() -> TableStyle:
    return TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTNAME", (3, 0), (3, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
        ("TEXTCOLOR", (2, 0), (2, -1), NAVY),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LIGHT_GREY, colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#e5e7eb")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ])


def _fmt_pct(val) -> str:
    return f"{val:.1f}%" if val is not None else "N/A"


def _fmt_val(val) -> str:
    return f"{val:.2f}" if val is not None else "N/A"


def _fmt_sensitivity(val) -> str:
    if val is None:
        return "N/A"
    return val.value.title() if hasattr(val, "value") else str(val).title()


def _score_rating(score: float) -> str:
    if score >= 85:
        return "Excellent"
    if score >= 70:
        return "Good"
    if score >= 55:
        return "Fair"
    return "Poor"


def _barrier_level(val: float) -> str:
    if val >= 0.80:
        return "High"
    if val >= 0.50:
        return "Medium"
    return "Low"


# ──────────────────────────────────────────────────────────────────────────────
# Alternate signature used by recommendations router
# ──────────────────────────────────────────────────────────────────────────────

def generate_pdf_report(recommendation, db) -> bytes:
    """
    Alternative entry point used by the recommendations router.
    Resolves food_profile and user from the database session.

    Parameters
    ----------
    recommendation : Recommendation ORM row
    db             : SQLAlchemy Session

    Returns
    -------
    bytes
        Valid PDF byte string.
    """
    from ..models.food import FoodProfile  # local import to avoid circular
    from ..models.user import User

    food_profile = None
    if recommendation.food_profile_id:
        food_profile = db.query(FoodProfile).filter(
            FoodProfile.id == recommendation.food_profile_id
        ).first()

    user = None
    if recommendation.user_id:
        user = db.query(User).filter(User.id == recommendation.user_id).first()

    return generate_recommendation_pdf(recommendation, food_profile, user)

import requests
from io import BytesIO
import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
    Flowable,
    KeepTogether,
    FrameBreak,
    NextPageTemplate,
    ListFlowable,
    ListItem,
    # Macro, # Unused
    # Indenter, # Unused
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white, lightgrey, dimgrey
from reportlab.lib.pagesizes import A4  # , landscape # landscape unused for now

# from reportlab.pdfgen import canvas # Not directly used for story, but for onPage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib.utils import ImageReader  # For getting image size
import textwrap
from math import sin, cos, radians, pi
from datetime import datetime, timedelta
import tempfile  # For cover image

# --- Configuration ---
FILENAME = "AST_Travels_Karnataka_Itinerary_Enhanced.pdf"
COMPANY_NAME = "AST Travels"
COMPANY_SLOGAN = "Explore. Experience. Enjoy."
WEBSITE = "www.asttravels.com"
PHONE = "7349733197"
EMAIL = "asttravels@gmail.com"
SOCIAL_MEDIA = {
    "Facebook": "asttravels",
    "Instagram": "@ast_travels",
    "Twitter": "@AST_Travels",
}

# --- Dates ---
START_DATE = datetime(2024, 7, 15)  # Updated year
TOTAL_DAYS = 7

# --- Enhanced Color Scheme ---
PRIMARY_COLOR = HexColor("#0A4D92")
ACCENT_COLOR = HexColor("#4CAF50")
TEXT_COLOR = HexColor("#333333")
LIGHT_TEXT_COLOR = HexColor("#555555")
BACKGROUND_COLOR = white
TIMELINE_COLOR = HexColor("#FF7F50")
SECONDARY_COLOR = HexColor("#F9A826")
HIGHLIGHT_COLOR = HexColor("#E91E63")
PALE_BLUE = HexColor("#E6F3FF")
PALE_GREEN = HexColor("#E6FFED")
PALE_YELLOW = HexColor("#FFFDE7")

# --- Image URLs ---
IMAGES = {
    "kalasa_bridge": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nofQkh6Fz5h9qZlIKbnryUY2qDuUH0MPumrUaUwnn-lY6dz5k2Nu6IOqmu5ClaBGcHBGfIycb4YA238jFJK8-pT4GFnkyeDYjAqeQejIwB8PRtH7kWR5Dic5btbhIPQ3lqSrNt2JoHm9Cvo=w203-h360-k-no",
    "kalasa_viewpoint": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4noJwwWj1yY59woeFLDI_TeA_t2qatVugfxnSm4elwUNBSGmia0gdKE0vEV8EGRFW3lLXzngQbzScwbehW8rXcDiAzSQwAPZ3SdC8HSm0qFKUDmWMNLh1xmLgLG5NsvB6Aw67k88Rvf2gQDj=w224-h398-k-no",
    "kudremukh_park": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nr3LqVNtgrlNZj3-A6eBKSXILoZGiwNNuNxd9MTIVo2PNKCuI8OmJg51Ubt6M0LEvS7UApHSzbEGwLKvI0lZxtP5k2lxb0zWnzWnoywQQGgje-iPSJ5W5y3RM9XDf2vx_5KYw_x=w203-h152-k-no",
    "kudremukh_dam": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nqrtkd3S5UzB6TcbN5JkCceJueZH7xtT3xSoduLZbmmhq7SPKLrPeKXxCpE2EwS2LJkAa-OgktuBlJQkSv8n_Nwg19i-ZriTfvWy478wpazpiCOaxu9a8g5SeUHTwzuth2hGz2f=w224-h298-k-no",
    "netravati_peak": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nqy-eYjX0oMSA4cqybR484N9_gjeitYett4pct2UcDtL7-HzSo__GuB4I9Muvl1Ygjngvp7AdRXtelcq0RxLdvD5toNkhWSlT0i_lS1_2vS7SQdDvUYAOBdfaVzol4Sq8UYHjOQr5Kzcao=w224-h398-k-no",
    "cover_image": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?q=80&w=1200&auto=format&fit=crop",  # Wider for better fit
    "map_image": "https://i.imgur.com/Z4YfA4g.png",  # Placeholder Karnataka map, ensure it's suitable
    "udupi_beach": "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?q=80&w=500&auto=format&fit=crop",
    "udupi_temple": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Sri_Krishna_Temple%2C_Udupi.jpg/320px-Sri_Krishna_Temple%2C_Udupi.jpg",
    "logo": "https://i.imgur.com/s6Xn6R1.png",  # Placeholder AST Travels logo (generic)
}

# --- Styles ---
styles = getSampleStyleSheet()
# Register a common font if needed for unicode characters, otherwise stick to Helvetica
# pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf')) # Example

# Base styles
styles.add(
    ParagraphStyle(
        name="Normal",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=TEXT_COLOR,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyText",
        parent=styles["Normal"],
        alignment=TA_JUSTIFY,
        spaceAfter=0.1 * inch,
    )
)

# Cover Page Styles
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=48,
        leading=52,
        textColor=white,
        alignment=TA_CENTER,
        spaceBefore=1 * inch,
        textShadowColor=black,
        textShadowOffset=(2, -2),
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSubtitle",
        fontName="Helvetica-Oblique",
        fontSize=20,
        leading=24,
        textColor=PALE_YELLOW,
        alignment=TA_CENTER,
        spaceAfter=0.5 * inch,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverPrice",
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=32,
        textColor=SECONDARY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=0.2 * inch,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverDuration",
        fontName="Helvetica",
        fontSize=16,
        leading=20,
        textColor=PALE_BLUE,
        alignment=TA_CENTER,
    )
)

# Main Titles
styles.add(
    ParagraphStyle(
        name="MainTitle",
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=PRIMARY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=0.2 * inch,
        spaceBefore=0.3 * inch,
    )
)
styles.add(
    ParagraphStyle(
        name="SectionTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=ACCENT_COLOR,
        spaceBefore=0.4 * inch,
        spaceAfter=0.1 * inch,
        keepWithNext=1,
    )
)
styles.add(
    ParagraphStyle(
        name="SubSectionTitle",
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=PRIMARY_COLOR,
        spaceBefore=0.3 * inch,
        spaceAfter=0.1 * inch,
        keepWithNext=1,
    )
)

# Table of Contents Styles
styles.add(
    ParagraphStyle(
        name="TOC",
        fontName="Helvetica-Bold",
        fontSize=16,
        textColor=PRIMARY_COLOR,
        alignment=TA_CENTER,
        spaceBefore=0.2 * inch,
        spaceAfter=0.2 * inch,
    )
)
styles.add(
    ParagraphStyle(
        name="TOCEntry1",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=TEXT_COLOR,
    )
)
styles.add(
    ParagraphStyle(
        name="TOCEntry2",
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=LIGHT_TEXT_COLOR,
        leftIndent=20,
    )
)
styles.add(
    ParagraphStyle(
        name="Dots",
        fontName="Helvetica",
        fontSize=10,
        textColor=lightgrey,
        alignment=TA_RIGHT,
    )
)


# Other Text Styles
styles.add(
    ParagraphStyle(
        name="CaptionText",
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=10,
        textColor=LIGHT_TEXT_COLOR,
        alignment=TA_CENTER,
        spaceAfter=0.1 * inch,
    )
)
styles.add(
    ParagraphStyle(
        name="FooterText",
        fontName="Helvetica",
        fontSize=8,
        textColor=dimgrey,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        name="ContactTitle",
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=PRIMARY_COLOR,
        spaceBefore=0.3 * inch,
        spaceAfter=0.1 * inch,
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="ContactInfo",
        parent=styles["Normal"],
        fontSize=10,
        spaceAfter=0.05 * inch,
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="HighlightText",
        parent=styles["BodyText"],
        textColor=ACCENT_COLOR,
        fontName="Helvetica-BoldItalic",
    )
)
styles.add(
    ParagraphStyle(
        name="SideNote",
        parent=styles["CaptionText"],
        alignment=TA_LEFT,
        textColor=PRIMARY_COLOR,
        fontName="Helvetica-Oblique",
    )
)
styles.add(
    ParagraphStyle(
        name="PackageHighlight",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        textColor=SECONDARY_COLOR,
    )
)

# Testimonial Styles
styles.add(
    ParagraphStyle(
        name="TestimonialText",
        parent=styles["BodyText"],
        fontSize=9,
        alignment=TA_LEFT,
        leading=12,
    )
)
styles.add(
    ParagraphStyle(
        name="TestimonialAuthor",
        fontName="Helvetica-BoldOblique",
        fontSize=9,
        textColor=PRIMARY_COLOR,
        alignment=TA_RIGHT,
        spaceBefore=0.1 * inch,
    )
)
styles.add(
    ParagraphStyle(
        name="QuoteMarks",
        fontName="Helvetica-Bold",
        fontSize=36,
        textColor=ACCENT_COLOR.clone(alpha=0.3),
        alignment=TA_LEFT,
    )
)

# CTA Style
styles.add(
    ParagraphStyle(
        name="CTAText",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        textColor=white,
        fontSize=11,
        leading=15,
    )
)


# --- Custom Flowables (Copied from user's code, minor adjustments if needed) ---
class TimelineFlowable(Flowable):
    def __init__(self, days, width=500):
        Flowable.__init__(self)
        self.days = days
        self.width = width
        self.height = 150

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setStrokeColor(TIMELINE_COLOR)
        canvas.setLineWidth(3)
        start_x = 50
        end_x = self.width - 50
        y_line = (
            self.height / 2 + 20
        )  # Move line up a bit for more space for text below

        canvas.line(start_x, y_line, end_x, y_line)

        dot_spacing = 20
        num_dots = int((end_x - start_x) / dot_spacing)
        for i in range(num_dots + 1):
            dot_x = start_x + i * dot_spacing
            if i % 2 == 0:
                canvas.setFillColor(PALE_YELLOW)
                canvas.circle(dot_x, y_line, 1.5, stroke=0, fill=1)

        segment_width = (end_x - start_x) / (
            len(self.days) - 1 if len(self.days) > 1 else 1
        )
        for i, day_info in enumerate(self.days):
            x = start_x + i * segment_width
            shadow_offset = 1.5
            canvas.setFillColor(dimgrey.clone(alpha=0.3))
            canvas.circle(
                x + shadow_offset, y_line - shadow_offset, 8, stroke=0, fill=1
            )
            canvas.setFillColor(TIMELINE_COLOR)
            canvas.circle(x, y_line, 8, stroke=0, fill=1)
            canvas.setFillColor(TIMELINE_COLOR.clone(alpha=0.7))
            canvas.circle(x, y_line, 5, stroke=0, fill=1)
            canvas.setFillColor(white.clone(alpha=0.6))
            canvas.circle(x - 2, y_line + 2, 2, stroke=0, fill=1)
            canvas.setFillColor(white)
            canvas.setFont("Helvetica-Bold", 7)
            canvas.drawCentredString(x, y_line - 2.5, f"{i+1}")

            # Text positions
            y_day_text = y_line - 25
            y_date_text = y_line - 40
            y_loc_box = y_line + 15  # Position relative to main y_line
            y_act_box = y_loc_box + 25  # Position activity box below location

            canvas.setFillColor(dimgrey.clone(alpha=0.5))
            day_txt = f"Day {i+1}"
            canvas.setFont("Helvetica-Bold", 9)
            canvas.drawCentredString(
                x + 0.5, y_day_text - 0.5, day_txt
            )  # Shadow for day text
            canvas.setFillColor(TEXT_COLOR)
            canvas.drawCentredString(x, y_day_text, day_txt)  # Day text

            date_str = day_info["date"].strftime("%b %d")
            canvas.setFont("Helvetica", 8)
            canvas.drawCentredString(x, y_date_text, date_str)  # Date text

            location = day_info["location"]
            canvas.setFont("Helvetica", 8)
            text_width_loc = canvas.stringWidth(location, "Helvetica", 8)
            box_width_loc = text_width_loc + 10
            box_height_loc = 15
            canvas.setFillColor(PRIMARY_COLOR.clone(alpha=0.15))
            canvas.roundRect(
                x - box_width_loc / 2,
                y_loc_box - box_height_loc / 2,
                box_width_loc,
                box_height_loc,
                3,
                stroke=0,
                fill=1,
            )
            canvas.setFillColor(TEXT_COLOR)
            canvas.drawCentredString(
                x, y_loc_box - 3, location
            )  # Location text (adjust y for centering in box)

            activity = day_info["activity"]
            if len(activity) > 15:
                activity = textwrap.fill(activity, width=15)
            lines = activity.split("\n")
            act_box_height = len(lines) * 10 + 6
            act_box_width = (
                max(
                    [canvas.stringWidth(line, "Helvetica-Oblique", 7) for line in lines]
                )
                + 8
            )
            canvas.setFillColor(TIMELINE_COLOR.clone(alpha=0.15))
            canvas.roundRect(
                x - act_box_width / 2,
                y_act_box - act_box_height / 2,
                act_box_width,
                act_box_height,
                3,
                stroke=0,
                fill=1,
            )
            canvas.setFillColor(TEXT_COLOR)
            canvas.setFont("Helvetica-Oblique", 7)
            for j, line in enumerate(lines):
                canvas.drawCentredString(
                    x, y_act_box + (len(lines) - 1) * 5 - j * 10 - 3, line
                )  # Activity text
        canvas.restoreState()


class RoundedBox(Flowable):
    def __init__(
        self,
        contents,
        width,
        height,
        radius=10,
        padding=10,
        backgroundColor=None,
        borderColor=None,
        borderWidth=1,
        shadowColor=None,
        shadowOffset=3,
    ):
        Flowable.__init__(self)
        self.contents = contents
        self.width = width
        self.height = height
        self.radius = radius
        self.padding = padding
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.shadowColor = shadowColor
        self.shadowOffset = shadowOffset
        # If contents is a list of flowables, wrap them in a KeepInFrame
        if isinstance(self.contents, list):
            from reportlab.platypus.flowables import KeepInFrame

            self.contents = KeepInFrame(
                self.width - 2 * self.padding,
                self.height - 2 * self.padding,
                self.contents,
            )

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        if self.shadowColor:
            canvas.setFillColor(self.shadowColor)
            canvas.roundRect(
                self.shadowOffset,
                -self.shadowOffset,
                self.width,
                self.height,
                self.radius,
                stroke=0,
                fill=1,
            )
        if self.backgroundColor:
            canvas.setFillColor(self.backgroundColor)
        if self.borderColor:
            canvas.setStrokeColor(self.borderColor)
            canvas.setLineWidth(self.borderWidth)
        else:
            canvas.setStrokeColor(None)
        canvas.roundRect(
            0,
            0,
            self.width,
            self.height,
            self.radius,
            stroke=bool(self.borderColor),
            fill=bool(self.backgroundColor),
        )
        if self.backgroundColor:  # Gradient-like highlight
            highlight_color = white.clone(alpha=0.1)
            canvas.setFillColor(highlight_color)
            canvas.roundRect(
                2,
                self.height * 0.6,
                self.width - 4,
                self.height * 0.4 - 2,
                self.radius - 2,
                stroke=0,
                fill=1,
            )

        if isinstance(self.contents, str):
            p_style = ParagraphStyle(
                "RoundedBoxContent", parent=styles["Normal"], alignment=TA_CENTER
            )
            p = Paragraph(self.contents, p_style)
            p_w, p_h = p.wrapOn(
                canvas, self.width - 2 * self.padding, self.height - 2 * self.padding
            )
            p.drawOn(
                canvas,
                self.padding,
                self.padding + (self.height - 2 * self.padding - p_h) / 2,
            )  # Center vertically
        elif self.contents:  # Check if contents exist
            self.contents.wrapOn(
                canvas, self.width - 2 * self.padding, self.height - 2 * self.padding
            )
            self.contents.drawOn(canvas, self.padding, self.padding)
        canvas.restoreState()


class Divider(Flowable):
    def __init__(
        self, width, color=lightgrey, thickness=1, spacer_上下=0.1 * inch, style="solid"
    ):  # Renamed spacer for clarity
        Flowable.__init__(self)
        self.width = width
        self.color = color
        self.thickness = thickness
        self.spacer = spacer_上下
        self.style = style
        self.height = 2 * self.spacer + self.thickness

    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        y = self.spacer
        if self.style == "solid":
            self.canv.line(0, y, self.width, y)
        elif self.style == "dashed":
            dash_pattern = [5, 3]  # dash, gap
            self.canv.setDash(dash_pattern)
            self.canv.line(0, y, self.width, y)
        elif self.style == "fancy":
            self.canv.line(0, y, self.width, y)
            dot_count = int(self.width / 30)
            for i in range(dot_count):
                dot_x = (i + 0.5) * (self.width / dot_count)
                dot_y_offset = 3 if i % 2 == 0 else -3
                self.canv.setFillColor(self.color)
                self.canv.circle(dot_x, y + dot_y_offset, 1.5, fill=1, stroke=0)
            self.canv.setFillColor(self.color)
            self.canv.circle(0, y, 3, fill=1, stroke=0)
            self.canv.circle(self.width, y, 3, fill=1, stroke=0)
        self.canv.restoreState()


class DecorationFlowable(Flowable):
    def __init__(
        self, width, height=20, color=ACCENT_COLOR, style="wave"
    ):  # Reduced default height
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.style = style

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        if self.style == "wave":
            canvas.setStrokeColor(self.color)
            canvas.setLineWidth(1.5)
            amplitude = self.height / 4
            frequency = 10  # Adjusted for visual appeal
            path = canvas.beginPath()
            path.moveTo(0, self.height / 2)
            for x_coord in range(0, int(self.width) + 1, 5):
                y_coord = self.height / 2 + amplitude * sin(
                    2 * pi * frequency * x_coord / self.width + pi / 2
                )  # Shifted for start
                path.lineTo(x_coord, y_coord)
            canvas.drawPath(path, stroke=1, fill=0)
        elif self.style == "corners":
            canvas.setStrokeColor(self.color)
            canvas.setLineWidth(2)
            corner_size = min(self.height, self.width / 10, 10)  # Adaptive corner size
            # Top left
            canvas.line(0, self.height, corner_size, self.height)
            canvas.line(0, self.height, 0, self.height - corner_size)
            # Top right
            canvas.line(self.width - corner_size, self.height, self.width, self.height)
            canvas.line(self.width, self.height, self.width, self.height - corner_size)
            # Bottom left
            canvas.line(0, 0, corner_size, 0)
            canvas.line(0, 0, 0, corner_size)
            # Bottom right
            canvas.line(self.width - corner_size, 0, self.width, 0)
            canvas.line(self.width, 0, self.width, corner_size)
        # Other styles (zigzag, dots) can be added if needed
        canvas.restoreState()


class PlaceholderImage(Flowable):
    def __init__(self, width, height, bgColor=lightgrey.clone(alpha=0.7)):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.bgColor = bgColor

    def draw(self):
        self.canv.setFillColor(self.bgColor)
        self.canv.setStrokeColor(dimgrey)
        self.canv.roundRect(0, 0, self.width, self.height, 5, stroke=1, fill=1)
        self.canv.setFillColor(TEXT_COLOR)
        self.canv.setFont("Helvetica", 10)
        self.canv.drawCentredString(
            self.width / 2, self.height / 2 + 5, "Image Not Available"
        )
        # Camera icon
        self.canv.setStrokeColor(TEXT_COLOR)
        self.canv.setLineWidth(1)
        cx, cy = self.width / 2, self.height / 2 - 10
        w, h = 20, 15
        self.canv.roundRect(cx - w / 2, cy - h / 2, w, h, 2, stroke=1, fill=0)
        self.canv.circle(cx, cy, 4, stroke=1, fill=0)  # Smaller lens
        self.canv.rect(cx - w / 4, cy + h / 2 - 1, w / 2, 3, stroke=0, fill=1)  # Flash


class StarRating(Flowable):
    def __init__(
        self,
        rating,
        max_stars=5,
        star_size=12,
        star_color=SECONDARY_COLOR,
        empty_color=lightgrey,
    ):
        Flowable.__init__(self)
        self.rating = min(float(rating), max_stars)
        self.max_stars = max_stars
        self.star_size = star_size
        self.star_color = star_color
        self.empty_color = empty_color
        self.width = (star_size * 1.1) * max_stars
        self.height = star_size

    def _draw_star(self, canvas, x_offset, filled_fraction, is_empty):
        size = self.star_size
        center_x = x_offset + size / 2
        center_y = size / 2
        points = []
        for i in range(5):
            angle_outer = (2 * pi * i / 5) - pi / 2
            points.append(
                (
                    center_x + size / 2 * cos(angle_outer),
                    center_y + size / 2 * sin(angle_outer),
                )
            )
            angle_inner = angle_outer + pi / 5
            points.append(
                (
                    center_x + size / 4 * cos(angle_inner),
                    center_y + size / 4 * sin(angle_inner),
                )
            )  # Inner radius smaller

        path = canvas.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for point in points[1:]:
            path.lineTo(point[0], point[1])
        path.close()

        if is_empty:
            canvas.setFillColor(self.empty_color)
            canvas.setStrokeColor(self.empty_color.darker(0.3))
            canvas.drawPath(path, stroke=1, fill=1)
        else:
            canvas.saveState()
            canvas.clipPath(path, stroke=0, fill=0)  # Clip to star shape
            # Background for potentially unfilled part
            canvas.setFillColor(self.empty_color)
            canvas.rect(x_offset, 0, size, size, stroke=0, fill=1)
            # Filled part
            canvas.setFillColor(self.star_color)
            canvas.rect(x_offset, 0, size * filled_fraction, size, stroke=0, fill=1)
            canvas.restoreState()
            # Outline for the star
            canvas.setStrokeColor(self.star_color.darker(0.3))
            canvas.setLineWidth(0.5)
            canvas.drawPath(path, stroke=1, fill=0)

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        for i in range(self.max_stars):
            star_x_offset = i * self.star_size * 1.1
            if i < int(self.rating):  # Full star
                self._draw_star(canvas, star_x_offset, 1.0, False)
            elif i < self.rating:  # Partial star
                fraction = self.rating - int(self.rating)
                self._draw_star(canvas, star_x_offset, fraction, False)
            else:  # Empty star
                self._draw_star(canvas, star_x_offset, 0.0, True)
        canvas.restoreState()


# --- Helper to get image from URL ---
def get_image_from_url(url, width=2 * inch, max_height=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, stream=True, timeout=20, headers=headers)
        response.raise_for_status()
        img_data = BytesIO(response.content)
        img = Image(img_data, width=width)  # Initial width

        aspect_ratio = img.imageHeight / img.imageWidth
        img.drawHeight = width * aspect_ratio
        img.drawWidth = width

        if max_height and img.drawHeight > max_height:
            img.drawHeight = max_height
            img.drawWidth = max_height / aspect_ratio
        return img
    except Exception as e:
        print(f"Warning: Could not fetch image from {url}. Error: {e}")
        ph_height = width * 0.6 if not max_height else min(width * 0.6, max_height)
        return PlaceholderImage(width, ph_height)


# --- Global Cache for Logo ---
CACHED_LOGO_DATA = None
CACHED_LOGO_SIZE = None


# --- Header and Footer with custom logo ---
def header_footer(canvas, doc):
    global CACHED_LOGO_DATA, CACHED_LOGO_SIZE
    canvas.saveState()

    # Draw Logo Image
    logo_url = IMAGES.get("logo")
    logo_max_height = 0.5 * inch
    logo_y_pos = doc.height + doc.topMargin - logo_max_height - 0.05 * inch

    if logo_url:
        if CACHED_LOGO_DATA is None:  # Fetch and cache only once
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
                response = requests.get(
                    logo_url, stream=True, timeout=10, headers=headers
                )
                response.raise_for_status()
                CACHED_LOGO_DATA = BytesIO(response.content)

                reader = ImageReader(CACHED_LOGO_DATA)
                img_w, img_h = reader.getSize()
                aspect = img_h / float(img_w)
                logo_height_actual = logo_max_height
                logo_width_actual = logo_height_actual / aspect

                if logo_width_actual > 2 * inch:  # Limit width too
                    logo_width_actual = 2 * inch
                    logo_height_actual = logo_width_actual * aspect

                CACHED_LOGO_SIZE = (logo_width_actual, logo_height_actual)
                CACHED_LOGO_DATA.seek(0)
            except Exception as e:
                print(f"Error fetching/processing logo: {e}")
                CACHED_LOGO_DATA = "Error"

        if CACHED_LOGO_DATA not in [None, "Error"]:
            try:
                logo_width, logo_height = CACHED_LOGO_SIZE
                canvas.drawImage(
                    ImageReader(CACHED_LOGO_DATA),
                    doc.leftMargin,
                    logo_y_pos
                    + (logo_max_height - logo_height),  # Adjust Y to align top
                    width=logo_width,
                    height=logo_height,
                    mask="auto",
                )
                CACHED_LOGO_DATA.seek(0)
            except Exception as e:
                print(f"Error drawing logo: {e}")
                CACHED_LOGO_DATA = "Error"  # Prevent re-drawing if it fails once

    slogan_x_offset = (
        (CACHED_LOGO_SIZE[0] + 0.15 * inch)
        if CACHED_LOGO_SIZE and CACHED_LOGO_DATA != "Error"
        else 0
    )
    if CACHED_LOGO_DATA == "Error" or not CACHED_LOGO_SIZE:  # Fallback if no logo
        canvas.setFont("Helvetica-Bold", 14)
        canvas.setFillColor(PRIMARY_COLOR)
        canvas.drawString(doc.leftMargin, logo_y_pos + 0.1 * inch, COMPANY_NAME)
        slogan_x_offset = (
            canvas.stringWidth(COMPANY_NAME, "Helvetica-Bold", 14) + 0.15 * inch
        )

    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(LIGHT_TEXT_COLOR)
    canvas.drawString(
        doc.leftMargin + slogan_x_offset, logo_y_pos + 0.22 * inch, COMPANY_SLOGAN
    )

    header_line_y = logo_y_pos - 0.1 * inch
    canvas.setStrokeColor(PRIMARY_COLOR.clone(alpha=0.5))
    canvas.setLineWidth(0.5)
    canvas.line(
        doc.leftMargin, header_line_y, doc.leftMargin + doc.width, header_line_y
    )

    # Footer
    footer_text = f"{COMPANY_NAME} | {WEBSITE} | {PHONE}"
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(LIGHT_TEXT_COLOR)
    canvas.drawCentredString(doc.leftMargin + doc.width / 2, 0.45 * inch, footer_text)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(PRIMARY_COLOR)
    canvas.drawRightString(doc.leftMargin + doc.width, 0.45 * inch, f"Page {doc.page}")
    footer_line_y = 0.65 * inch
    canvas.setStrokeColor(PRIMARY_COLOR.clone(alpha=0.5))
    canvas.setLineWidth(0.5)
    canvas.line(
        doc.leftMargin, footer_line_y, doc.leftMargin + doc.width, footer_line_y
    )
    canvas.restoreState()


# Custom first page
def cover_page_layout(canvas, doc):
    canvas.saveState()
    page_width, page_height = A4

    # Background Image
    cover_img_url = IMAGES.get("cover_image")
    if cover_img_url:
        try:
            # Using tempfile as in user's code for robustness
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(
                cover_img_url, stream=True, timeout=20, headers=headers
            )
            response.raise_for_status()
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".jpg"
            ) as temp_img_file:
                temp_img_file.write(response.content)
                temp_img_path = temp_img_file.name

            # Draw image to fill page
            img_reader = ImageReader(temp_img_path)
            img_w, img_h = img_reader.getSize()

            # Calculate aspect ratios
            page_aspect = page_width / page_height
            img_aspect = img_w / img_h

            if img_aspect > page_aspect:  # Image is wider than page
                draw_h = page_height
                draw_w = draw_h * img_aspect
                x_offset = (page_width - draw_w) / 2
                y_offset = 0
            else:  # Image is taller or same aspect as page
                draw_w = page_width
                draw_h = draw_w / img_aspect
                x_offset = 0
                y_offset = (page_height - draw_h) / 2

            canvas.drawImage(
                temp_img_path,
                x_offset,
                y_offset,
                width=draw_w,
                height=draw_h,
                preserveAspectRatio=True,
                anchor="c",
            )
            os.unlink(temp_img_path)

            # Semi-transparent overlay for text readability
            canvas.setFillColorRGB(0, 0, 0, 0.5)  # Black with 50% opacity
            canvas.rect(0, 0, page_width, page_height, fill=1, stroke=0)

        except Exception as e:
            print(f"Error with cover image: {e}. Using fallback.")
            canvas.setFillColor(PRIMARY_COLOR)
            canvas.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    else:  # Fallback if no URL
        canvas.setFillColor(PRIMARY_COLOR)
        canvas.rect(0, 0, page_width, page_height, fill=1, stroke=0)
    canvas.restoreState()


# --- Content Descriptions (Copied from user code) ---
kalasa_desc = (
    "Escape to Kalasa, a haven of spiritual charm...peace and picturesque beauty."
)
udupi_desc = (
    "Discover Udupi, a vibrant coastal gem...a culinary delight known worldwide."
)
kudremukh_desc = "Immerse yourself in the raw beauty of Kudremukh...nature's grandeur and serene water bodies."
netravati_desc = "Embark on an unforgettable adventure to Netravati Peak...unparalleled panoramic beauty."

# --- Package information (Copied from user code) ---
package_info = {
    "Standard": {
        "price": "₹25,999",
        "duration": "7 Days / 6 Nights",
        "rating": 4.5,
        "ideal_for": "Couples, Families",
        "includes": [
            "Accommodation (3-star)",
            "Breakfast & Dinner",
            "AC Transport",
            "Guide",
            "Entrance Fees",
        ],
        "highlights": "Great value for a comprehensive Karnataka experience.",
    },
    "Premium": {
        "price": "₹39,999",
        "duration": "7 Days / 6 Nights",
        "rating": 4.8,
        "ideal_for": "Luxury, Honeymooners",
        "includes": [
            "Luxury Accommodation (4/5-star)",
            "All Meals",
            "Premium AC Vehicle",
            "Private Guides",
            "Photography",
            "Welcome Gift",
        ],
        "highlights": "Ultimate Karnataka experience with premium amenities.",
    },
}

# --- Testimonials (Copied from user code) ---
testimonials = [
    {
        "text": "AST Travels exceeded our expectations. Perfectly balanced itinerary.",
        "author": "Priya & Rahul S., Delhi",
    },
    {
        "text": "Knowledgeable guide for Kudremukh trek. Safe and enjoyable. Will book again!",
        "author": "Rajesh P., Mumbai",
    },
    {
        "text": "From Udupi beaches to Netravati peaks, every moment was magical.",
        "author": "Meera K., Bangalore",
    },
]


# --- Daily Itinerary (Copied from user code) ---
def create_itinerary_days():
    itinerary = []
    days_config = [
        ("Bangalore → Kalasa", "Arrival & Transfer"),
        ("Kalasa", "Temples & Viewpoint"),
        ("Kalasa", "Hanging Bridge & Local Culture"),
        ("Kalasa → Udupi", "Travel & Beach Exploration"),
        ("Udupi", "Temple Visit & St. Mary's Island"),
        ("Udupi → Kudremukh", "Travel & Lakya Dam"),
        ("Kudremukh → Netravati Base", "National Park Trek & Transfer"),
        ("Netravati Peak & Departure", "Sunrise Trek & Return Journey"),
    ]
    actual_total_days = min(
        TOTAL_DAYS, len(days_config)
    )  # Ensure we don't go over defined configs

    for i in range(actual_total_days):
        date = START_DATE + timedelta(days=i)
        day = {
            "date": date,
            "location": days_config[i][0],
            "activity": days_config[i][1],
        }
        itinerary.append(day)
    return itinerary


# --- Build PDF ---
def build_pdf():
    doc = SimpleDocTemplate(
        FILENAME,
        pagesize=A4,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=1.0 * inch,
        bottomMargin=0.8 * inch,
        title="AST Travels Karnataka Itinerary",
    )  # Adjusted top margin

    # Page Templates
    cover_frame = Frame(
        0,
        0,
        A4[0],
        A4[1],
        id="cover_fullpage",
        leftPadding=0.5 * inch,
        rightPadding=0.5 * inch,
        topPadding=1 * inch,
        bottomPadding=1 * inch,
    )
    cover_template = PageTemplate(
        id="cover", frames=[cover_frame], onPage=cover_page_layout
    )

    content_frame = Frame(
        doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal_content"
    )
    content_template = PageTemplate(
        id="content", frames=[content_frame], onPage=header_footer
    )

    col_width = doc.width / 2 - 0.125 * inch  # Space between columns 0.25 inch
    two_col_frame_1 = Frame(
        doc.leftMargin, doc.bottomMargin, col_width, doc.height, id="col1"
    )
    two_col_frame_2 = Frame(
        doc.leftMargin + col_width + 0.25 * inch,
        doc.bottomMargin,
        col_width,
        doc.height,
        id="col2",
    )
    two_column_template = PageTemplate(
        id="two_column", frames=[two_col_frame_1, two_col_frame_2], onPage=header_footer
    )

    doc.addPageTemplates([cover_template, content_template, two_column_template])
    story = []

    # --- Cover Page ---
    story.append(NextPageTemplate("cover"))
    story.append(Spacer(1, A4[1] * 0.35))  # Push content down on cover
    story.append(Paragraph(COMPANY_NAME.upper(), styles["CoverTitle"]))
    story.append(
        Paragraph(
            "Karnataka's Treasures: Western Ghats & Coastal Beauty",
            styles["CoverSubtitle"],
        )
    )
    story.append(Spacer(1, A4[1] * 0.20))
    story.append(
        Paragraph(
            f"Starting from {package_info['Standard']['price']}", styles["CoverPrice"]
        )
    )
    story.append(
        Paragraph(package_info["Standard"]["duration"], styles["CoverDuration"])
    )
    story.append(PageBreak())

    # --- Table of Contents ---
    story.append(NextPageTemplate("content"))
    story.append(
        DecorationFlowable(
            doc.width, style="corners", color=PRIMARY_COLOR.clone(alpha=0.3)
        )
    )
    story.append(Paragraph("Your Karnataka Adventure", styles["MainTitle"]))
    story.append(Paragraph("Table of Contents", styles["TOC"]))

    toc_items = [  # (Text, Page Number, StyleKey)
        ("Welcome to Your Journey", 3, "TOCEntry1"),
        ("Tour At a Glance (7-Day Itinerary)", 3, "TOCEntry1"),
        ("Route Map Preview", 4, "TOCEntry1"),
        ("Destination Highlights", 4, "TOCEntry1"),
        ("  Kalasa: Spiritual Charm", 4, "TOCEntry2"),
        ("  Udupi: Coastal Beauty", 5, "TOCEntry2"),
        ("  Kudremukh: Wilderness Beckons", 5, "TOCEntry2"),
        ("  Netravati Peak: Trekker's Paradise", 6, "TOCEntry2"),
        ("Choose Your Package", 7, "TOCEntry1"),
        ("Voices of Our Travelers", 8, "TOCEntry1"),
        ("Book Your Adventure", 8, "TOCEntry1"),
    ]
    toc_data = []
    for item, page, style_key in toc_items:
        num_dots = 60 - len(item) - len(str(page))  # Approximate dots
        leader_dots = "." * max(5, num_dots)
        toc_data.append(
            [
                Paragraph(item, styles[style_key]),
                Paragraph(leader_dots, styles["Dots"]),
                Paragraph(str(page), styles[style_key]),
            ]
        )

    toc_table = Table(
        toc_data,
        colWidths=[doc.width * 0.75, doc.width * 0.1, doc.width * 0.15],
        style=TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (2, 0), (2, -1), "RIGHT"),
                ("RIGHTPADDING", (1, 0), (1, -1), 0),
                ("LEFTPADDING", (1, 0), (1, -1), 0),
            ]
        ),
    )
    story.append(toc_table)
    story.append(Spacer(1, 0.1 * inch))
    story.append(
        DecorationFlowable(
            doc.width, style="corners", color=PRIMARY_COLOR.clone(alpha=0.3)
        )
    )
    story.append(PageBreak())

    # --- Welcome Message & Timeline ---
    story.append(Paragraph("Welcome to Your Journey", styles["SectionTitle"]))
    story.append(
        DecorationFlowable(width=doc.width * 0.6, style="wave", color=ACCENT_COLOR)
    )
    story.append(Spacer(1, 0.1 * inch))
    welcome_text_flowables = [
        Paragraph(
            f"Dear Traveler,<br/><br/>Welcome to an exclusive Karnataka adventure with <b>{COMPANY_NAME}</b>! "
            "This itinerary is your guide to a memorable exploration of stunning temples, pristine beaches, "
            "lush forests, and majestic peaks. We're thrilled to have you join us.",
            styles["BodyText"],
        ),
        Spacer(1, 0.1 * inch),
        Paragraph(
            "Prepare for a transformative experience through diverse landscapes, from the spiritual serenity of "
            "<i>Kalasa</i> to Udupi's coastal charm, Kudremukh's wilderness, and Netravati's heights. "
            "Our curated journey blends natural beauty, cultural heritage, and local flavors.",
            styles["BodyText"],
        ),
    ]
    story.append(
        RoundedBox(
            welcome_text_flowables,
            width=doc.width,
            height=2.5 * inch,
            backgroundColor=PALE_BLUE,
            borderColor=PRIMARY_COLOR.clone(alpha=0.5),
            shadowColor=dimgrey.clone(alpha=0.2),
            padding=15,
            radius=8,
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("Tour At a Glance: 7-Day Itinerary", styles["SectionTitle"]))
    story.append(
        DecorationFlowable(width=doc.width * 0.7, style="wave", color=ACCENT_COLOR)
    )
    story.append(TimelineFlowable(create_itinerary_days(), width=doc.width))
    story.append(PageBreak())

    # --- Map ---
    story.append(Paragraph("Route Map Preview", styles["SectionTitle"]))
    story.append(
        DecorationFlowable(width=doc.width * 0.5, style="wave", color=ACCENT_COLOR)
    )
    map_img_obj = get_image_from_url(
        IMAGES["map_image"], width=doc.width * 0.8, max_height=doc.height * 0.5
    )
    map_padding = 10  # points
    map_box_width = (
        map_img_obj.drawWidth + 2 * map_padding
        if hasattr(map_img_obj, "drawWidth")
        else doc.width * 0.8
    )
    map_box_height = (
        map_img_obj.drawHeight + 2 * map_padding
        if hasattr(map_img_obj, "drawHeight")
        else doc.height * 0.4
    )

    map_container = RoundedBox(
        map_img_obj,
        width=map_box_width,
        height=map_box_height,
        backgroundColor=PALE_BLUE.clone(alpha=0.3),
        borderColor=PRIMARY_COLOR,
        radius=8,
        shadowColor=dimgrey.clone(alpha=0.2),
        padding=map_padding,
    )

    # Center the map
    story.append(
        Table(
            [[map_container]],
            colWidths=[doc.width],
            style=TableStyle([("ALIGN", (0, 0), (0, 0), "CENTER")]),
        )
    )
    story.append(
        Paragraph(
            "<i>A visual guide to your adventure across Karnataka's scenic spots.</i>",
            styles["CaptionText"],
        )
    )
    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Divider(width=doc.width, style="fancy", color=PRIMARY_COLOR.clone(alpha=0.4))
    )

    # --- Destinations ---
    story.append(
        Paragraph("Destination Highlights", styles["MainTitle"])
    )  # Main title for all destinations

    # Kalasa
    story.append(
        Paragraph("Kalasa: Spiritual Charm & Lush Landscapes", styles["SectionTitle"])
    )
    img_k_bridge = get_image_from_url(
        IMAGES["kalasa_bridge"], width=doc.width * 0.35, max_height=2.8 * inch
    )
    kalasa_box_content = [
        Paragraph(kalasa_desc, styles["BodyText"]),
        Spacer(0.1 * inch, 0.1 * inch),
        Paragraph(
            "<b>Key Sights:</b> Ambaa Teertha, Ancient Temples, Hanging Bridge, Bhadra River.",
            styles["HighlightText"],
        ),
    ]
    kalasa_text_box = RoundedBox(
        kalasa_box_content,
        width=doc.width * 0.55,
        height=(
            img_k_bridge.drawHeight
            if hasattr(img_k_bridge, "drawHeight")
            else 2.5 * inch
        ),
        backgroundColor=PALE_GREEN.clone(alpha=0.5),
        padding=15,
        radius=8,
    )
    story.append(
        Table(
            [[img_k_bridge, kalasa_text_box]],
            colWidths=[doc.width * 0.4, doc.width * 0.6],
            style=TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (1, 0), (1, 0), 0.2 * inch),
                ]
            ),
        )
    )
    story.append(
        Paragraph(
            "<i>Kalasa Hanging Bridge: A walk above the Bhadra.</i>",
            styles["CaptionText"],
        )
    )
    story.append(Divider(width=doc.width, style="dashed", color=LIGHT_TEXT_COLOR))

    # Udupi
    story.append(
        Paragraph("Udupi: Coastal Beauty & Temple Heritage", styles["SectionTitle"])
    )
    img_u_beach = get_image_from_url(
        IMAGES["udupi_beach"], width=doc.width * 0.35, max_height=2.8 * inch
    )
    udupi_box_content = [
        Paragraph(udupi_desc, styles["BodyText"]),
        Spacer(0.1 * inch, 0.1 * inch),
        Paragraph(
            "<b>Must Visit:</b> Sri Krishna Temple, Malpe Beach, St. Mary's Island. Taste authentic Udupi cuisine!",
            styles["HighlightText"],
        ),
    ]
    udupi_text_box = RoundedBox(
        udupi_box_content,
        width=doc.width * 0.55,
        height=(
            img_u_beach.drawHeight if hasattr(img_u_beach, "drawHeight") else 2.5 * inch
        ),
        backgroundColor=PALE_YELLOW.clone(alpha=0.5),
        padding=15,
        radius=8,
    )
    story.append(
        Table(
            [[udupi_text_box, img_u_beach]],
            colWidths=[doc.width * 0.6, doc.width * 0.4],
            style=TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("RIGHTPADDING", (0, 0), (0, 0), 0.2 * inch),
                ]
            ),
        )
    )
    story.append(
        Paragraph(
            "<i>Udupi's serene beaches and vibrant culture await.</i>",
            styles["CaptionText"],
        )
    )
    story.append(Divider(width=doc.width, style="dashed", color=LIGHT_TEXT_COLOR))
    story.append(PageBreak())

    # Kudremukh
    story.append(Paragraph("Kudremukh: Wilderness Beckons", styles["SectionTitle"]))
    img_k_park = get_image_from_url(
        IMAGES["kudremukh_park"], width=doc.width * 0.35, max_height=2.8 * inch
    )
    kudremukh_box_content = [
        Paragraph(kudremukh_desc, styles["BodyText"]),
        Spacer(0.1 * inch, 0.1 * inch),
        Paragraph(
            "<b>Explore:</b> Kudremukh National Park, Lakya Dam, Hanuman Gundi Falls. Rich biodiversity.",
            styles["HighlightText"],
        ),
    ]
    kudremukh_text_box = RoundedBox(
        kudremukh_box_content,
        width=doc.width * 0.55,
        height=(
            img_k_park.drawHeight if hasattr(img_k_park, "drawHeight") else 2.5 * inch
        ),
        backgroundColor=PALE_GREEN.clone(alpha=0.5),
        padding=15,
        radius=8,
    )
    story.append(
        Table(
            [[img_k_park, kudremukh_text_box]],
            colWidths=[doc.width * 0.4, doc.width * 0.6],
            style=TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (1, 0), (1, 0), 0.2 * inch),
                ]
            ),
        )
    )
    story.append(
        Paragraph(
            "<i>Kudremukh National Park: A trekker's delight.</i>",
            styles["CaptionText"],
        )
    )
    story.append(Divider(width=doc.width, style="dashed", color=LIGHT_TEXT_COLOR))

    # Netravati Peak
    story.append(
        Paragraph("Netravati Peak: Trekker's Paradise", styles["SectionTitle"])
    )
    img_n_peak = get_image_from_url(
        IMAGES["netravati_peak"], width=doc.width * 0.35, max_height=2.8 * inch
    )
    netravati_box_content = [
        Paragraph(netravati_desc, styles["BodyText"]),
        Spacer(0.1 * inch, 0.1 * inch),
        Paragraph(
            "<b>Experience:</b> Awe-inspiring sunrises, verdant valleys, diverse birdlife. A rewarding climb!",
            styles["HighlightText"],
        ),
    ]
    netravati_text_box = RoundedBox(
        netravati_box_content,
        width=doc.width * 0.55,
        height=(
            img_n_peak.drawHeight if hasattr(img_n_peak, "drawHeight") else 2.5 * inch
        ),
        backgroundColor=PALE_YELLOW.clone(alpha=0.5),
        padding=15,
        radius=8,
    )
    story.append(
        Table(
            [[netravati_text_box, img_n_peak]],
            colWidths=[doc.width * 0.6, doc.width * 0.4],
            style=TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("RIGHTPADDING", (0, 0), (0, 0), 0.2 * inch),
                ]
            ),
        )
    )
    story.append(
        Paragraph(
            "<i>Netravati Peak: Panoramic views await.</i>", styles["CaptionText"]
        )
    )
    story.append(PageBreak())

    # --- Package Options ---
    story.append(NextPageTemplate("two_column"))
    story.append(Paragraph("Choose Your Package", styles["MainTitle"]))
    story.append(
        DecorationFlowable(col_width * 0.8, style="wave", color=ACCENT_COLOR)
    )  # Decoration for column width

    # Standard Package (Column 1)
    std_title = Paragraph("Standard Package", styles["SubSectionTitle"])
    std_price_rating = Table(
        [
            [
                Paragraph(
                    f"<b>{package_info['Standard']['price']}</b> <font size=8>per person</font>",
                    styles["PackageHighlight"],
                ),
                StarRating(package_info["Standard"]["rating"]),
            ]
        ],
        colWidths=[col_width * 0.6, col_width * 0.35],
        style=TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]),
    )
    std_details = [
        Paragraph(
            f"<b>Ideal for:</b> {package_info['Standard']['ideal_for']}",
            styles["BodyText"],
        )
    ]
    std_includes_title = Paragraph("<b>Includes:</b>", styles["BodyText"])
    std_includes_list = ListFlowable(
        [
            ListItem(
                Paragraph(item, styles["BodyText"]),
                leftIndent=15,
                bulletColor=ACCENT_COLOR,
                bulletOffsetY=-2,
            )
            for item in package_info["Standard"]["includes"]
        ],
        bulletType="bullet",
        start="circle",
    )
    std_highlight = Paragraph(
        f"<i>{package_info['Standard']['highlights']}</i>", styles["SideNote"]
    )

    std_box_content = (
        [std_title, std_price_rating, Spacer(0.1 * inch, 0.1 * inch)]
        + std_details
        + [
            std_includes_title,
            std_includes_list,
            Spacer(0.1 * inch, 0.1 * inch),
            std_highlight,
        ]
    )

    # Estimate height needed for std_box_content
    # This is a simplification; exact height calculation is complex
    std_est_height = 4.5 * inch
    story.append(
        RoundedBox(
            std_box_content,
            width=col_width - 0.1 * inch,
            height=std_est_height,
            backgroundColor=PALE_BLUE,
            borderColor=PRIMARY_COLOR,
            radius=8,
            padding=10,
            shadowColor=dimgrey.clone(alpha=0.2),
        )
    )

    # Premium Package (Column 2)
    story.append(FrameBreak())
    prem_title = Paragraph(
        "Premium Package <font size=9 color='{HIGHLIGHT_COLOR.hexval()}'> ✨ Best Value</font>",
        styles["SubSectionTitle"],
    )
    prem_price_rating = Table(
        [
            [
                Paragraph(
                    f"<b>{package_info['Premium']['price']}</b> <font size=8>per person</font>",
                    styles["PackageHighlight"],
                ),
                StarRating(package_info["Premium"]["rating"]),
            ]
        ],
        colWidths=[col_width * 0.6, col_width * 0.35],
        style=TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]),
    )
    prem_details = [
        Paragraph(
            f"<b>Ideal for:</b> {package_info['Premium']['ideal_for']}",
            styles["BodyText"],
        )
    ]
    prem_includes_title = Paragraph(
        "<b>Includes (All Standard plus):</b>", styles["BodyText"]
    )
    prem_includes_list = ListFlowable(
        [
            ListItem(
                Paragraph(item, styles["BodyText"]),
                leftIndent=15,
                bulletColor=SECONDARY_COLOR,
                bulletOffsetY=-2,
            )
            for item in package_info["Premium"]["includes"]
        ],
        bulletType="bullet",
        start="circle",
    )  # Diff bullet color
    prem_highlight = Paragraph(
        f"<i>{package_info['Premium']['highlights']}</i>", styles["SideNote"]
    )

    prem_box_content = (
        [prem_title, prem_price_rating, Spacer(0.1 * inch, 0.1 * inch)]
        + prem_details
        + [
            prem_includes_title,
            prem_includes_list,
            Spacer(0.1 * inch, 0.1 * inch),
            prem_highlight,
        ]
    )

    prem_est_height = 5.5 * inch  # Premium has more includes
    story.append(
        RoundedBox(
            prem_box_content,
            width=col_width - 0.1 * inch,
            height=prem_est_height,
            backgroundColor=PALE_YELLOW,
            borderColor=SECONDARY_COLOR,
            radius=8,
            padding=10,
            shadowColor=dimgrey.clone(alpha=0.2),
        )
    )
    story.append(PageBreak())

    # --- Testimonials ---
    story.append(NextPageTemplate("content"))
    story.append(Paragraph("Voices of Our Travelers", styles["MainTitle"]))
    story.append(DecorationFlowable(doc.width * 0.7, style="wave", color=ACCENT_COLOR))

    testimonial_boxes = []
    for t in testimonials:
        content = [
            Paragraph("“", styles["QuoteMarks"]),
            Paragraph(t["text"], styles["TestimonialText"]),
            Spacer(0.1 * inch, 0.05 * inch),
            Paragraph(f"— {t['author']}", styles["TestimonialAuthor"]),
        ]
        # Estimate height for testimonial box
        t_height = 1.8 * inch + (len(t["text"]) // 50) * 0.2 * inch  # Rough estimate
        testimonial_boxes.append(
            RoundedBox(
                content,
                width=doc.width / 3 - 0.2 * inch,
                height=t_height,
                backgroundColor=PALE_BLUE.clone(alpha=0.6),
                radius=8,
                padding=10,
                borderColor=ACCENT_COLOR.clone(alpha=0.4),
                shadowColor=dimgrey.clone(alpha=0.15),
            )
        )

    if len(testimonial_boxes) == 3:  # Assuming 3 testimonials for a row
        story.append(
            Table(
                [testimonial_boxes],
                colWidths=[doc.width / 3] * 3,
                style=TableStyle(
                    [
                        ("LEFTPADDING", (0, 0), (-1, -1), 0.05 * inch),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0.05 * inch),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ]
                ),
            )
        )
    else:  # Fallback for different number of testimonials
        for box in testimonial_boxes:
            story.append(box)
            story.append(Spacer(1, 0.1 * inch))

    # --- Contact Information / CTA ---
    story.append(Paragraph("Book Your Adventure!", styles["MainTitle"]))
    story.append(DecorationFlowable(doc.width * 0.7, style="wave", color=ACCENT_COLOR))
    story.append(
        Paragraph(
            f"Ready to explore Karnataka's wonders? Contact <b>{COMPANY_NAME}</b> today!",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 0.2 * inch))

    contact_data = [
        [
            Paragraph("<b>✆ Phone:</b>", styles["ContactInfo"]),
            Paragraph(PHONE, styles["ContactInfo"]),
        ],
        [
            Paragraph("<b>✉ Email:</b>", styles["ContactInfo"]),
            Paragraph(EMAIL, styles["ContactInfo"]),
        ],
        [
            Paragraph("<b>🌐 Website:</b>", styles["ContactInfo"]),
            Paragraph(WEBSITE, styles["ContactInfo"]),
        ],
    ]
    for platform, handle in SOCIAL_MEDIA.items():
        icon = "🔗"  # Default icon
        if "Facebook" in platform:
            icon = "<b>ƒ</b>"  # Using simple text for icons
        if "Instagram" in platform:
            icon = "<b>📷</b>"
        if "Twitter" in platform:
            icon = "<b>🐦</b>"
        contact_data.append(
            [
                Paragraph(f"{icon} {platform}:", styles["ContactInfo"]),
                Paragraph(handle, styles["ContactInfo"]),
            ]
        )

    contact_table = Table(
        contact_data,
        colWidths=[doc.width * 0.3, doc.width * 0.7],
        style=TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("GRID", (0, 0), (-1, -1), 0.5, PALE_BLUE.darker(0.1)),
                ("BACKGROUND", (0, 0), (0, -1), PALE_BLUE.clone(alpha=0.3)),
            ]
        ),
    )
    story.append(contact_table)
    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph(
            "<b>Office Hours:</b> Monday - Saturday, 9:00 AM - 6:00 PM (IST)",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    cta_para = Paragraph(
        "<b>Your unforgettable journey awaits!</b><br/>"
        "Reach out to our travel experts to customize your trip or book now. "
        "Early bird discounts available for a limited time!",
        styles["CTAText"],
    )
    story.append(
        RoundedBox(
            cta_para,
            width=doc.width,
            height=1.3 * inch,
            radius=10,
            backgroundColor=HIGHLIGHT_COLOR,
            padding=15,
            shadowColor=dimgrey.clone(alpha=0.3),
        )
    )

    # Build
    try:
        doc.build(story)
        print(f"PDF '{FILENAME}' generated successfully.")
    except Exception as e:
        print(f"Error building PDF: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    build_pdf()

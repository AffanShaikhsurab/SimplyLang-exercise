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
    Macro,
    Indenter,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white, lightgrey, dimgrey
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate
import textwrap
from math import sin, cos, radians, pi
from datetime import datetime, timedelta

# --- Configuration ---
FILENAME = "AST_Travels_Karnataka_Itinerary.pdf"
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
START_DATE = datetime(2023, 11, 15)
TOTAL_DAYS = 7

# --- Enhanced Color Scheme ---
PRIMARY_COLOR = HexColor("#0A4D92")  # Deeper blue
ACCENT_COLOR = HexColor("#4CAF50")  # Nature green
TEXT_COLOR = HexColor("#333333")
LIGHT_TEXT_COLOR = HexColor("#555555")
BACKGROUND_COLOR = white
TIMELINE_COLOR = HexColor("#FF7F50")  # Coral color for timeline
SECONDARY_COLOR = HexColor("#F9A826")  # Warm yellow/orange
HIGHLIGHT_COLOR = HexColor("#E91E63")  # Pink/magenta for highlights
PALE_BLUE = HexColor("#E6F3FF")  # Light blue for backgrounds
PALE_GREEN = HexColor("#E6FFED")  # Light green for backgrounds
PALE_YELLOW = HexColor("#FFFDE7")  # Light yellow for backgrounds

# --- Image URLs ---
IMAGES = {
    "kalasa_bridge": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nofQkh6Fz5h9qZlIKbnryUY2qDuUH0MPumrUaUwnn-lY6dz5k2Nu6IOqmu5ClaBGcHBGfIycb4YA238jFJK8-pT4GFnkyeDYjAqeQejIwB8PRtH7kWR5Dic5btbhIPQ3lqSrNt2JoHm9Cvo=w203-h360-k-no",
    "kalasa_viewpoint": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4noJwwWj1yY59woeFLDI_TeA_t2qatVugfxnSm4elwUNBSGmia0gdKE0vEV8EGRFW3lLXzngQbzScwbehW8rXcDiAzSQwAPZ3SdC8HSm0qFKUDmWMNLh1xmLgLG5NsvB6Aw67k88Rvf2gQDj=w224-h398-k-no",
    "kudremukh_park": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nr3LqVNtgrlNZj3-A6eBKSXILoZGiwNNuNxd9MTIVo2PNKCuI8OmJg51Ubt6M0LEvS7UApHSzbEGwLKvI0lZxtP5k2lxb0zWnzWnoywQQGgje-iPSJ5W5y3RM9XDf2vx_5KYw_x=w203-h152-k-no",
    "kudremukh_dam": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nqrtkd3S5UzB6TcbN5JkCceJueZH7xtT3xSoduLZbmmhq7SPKLrPeKXxCpE2EwS2LJkAa-OgktuBlJQkSv8n_Nwg19i-ZriTfvWy478wpazpiCOaxu9a8g5SeUHTwzuth2hGz2f=w224-h298-k-no",
    "netravati_peak": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nqy-eYjX0oMSA4cqybR484N9_gjeitYett4pct2UcDtL7-HzSo__GuB4I9Muvl1Ygjngvp7AdRXtelcq0RxLdvD5toNkhWSlT0i_lS1_2vS7SQdDvUYAOBdfaVzol4Sq8UYHjOQr5Kzcao=w224-h398-k-no",
    "cover_image": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?q=80&w=1000&auto=format&fit=crop",
    "map_image": "https://i.imgur.com/BbQw1aD.png",  # Karnataka map
    "udupi_beach": "https://images.unsplash.com/photo-1596895111956-bf1cf0599ce5?q=80&w=500&auto=format&fit=crop",
    "udupi_temple": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Sri_Krishna_Temple%2C_Udupi.jpg/320px-Sri_Krishna_Temple%2C_Udupi.jpg",
    "logo": "https://i.imgur.com/L3Zr2dw.png",  # A placeholder for your logo
}


# --- Custom Flowables ---
class TimelineFlowable(Flowable):
    def __init__(self, days, width=500):
        Flowable.__init__(self)
        self.days = days
        self.width = width
        self.height = 150  # Increased height for more visual space

    def draw(self):
        canvas = self.canv
        canvas.saveState()

        # Draw timeline line with gradient effect
        canvas.setStrokeColor(TIMELINE_COLOR)
        canvas.setLineWidth(3)
        start_x = 50
        end_x = self.width - 50
        y = self.height / 2

        # Main timeline line
        canvas.line(start_x, y, end_x, y)

        # Add decorative dots along the line
        dot_spacing = 20
        num_dots = int((end_x - start_x) / dot_spacing)
        for i in range(num_dots + 1):
            dot_x = start_x + i * dot_spacing
            if i % 2 == 0:  # Skip every other dot for visual effect
                canvas.setFillColor(PALE_YELLOW)
                canvas.circle(dot_x, y, 1.5, stroke=0, fill=1)

        # Draw days with enhanced styling
        segment_width = (end_x - start_x) / (len(self.days) - 1)
        for i, day_info in enumerate(self.days):
            x = start_x + i * segment_width

            # Draw shadow for depth
            shadow_offset = 1.5
            canvas.setFillColor(dimgrey.clone(alpha=0.3))
            canvas.circle(x + shadow_offset, y - shadow_offset, 8, stroke=0, fill=1)

            # Draw circle with gradient-like effect
            canvas.setFillColor(TIMELINE_COLOR)
            canvas.circle(x, y, 8, stroke=0, fill=1)
            canvas.setFillColor(TIMELINE_COLOR.clone(alpha=0.7))
            canvas.circle(x, y, 5, stroke=0, fill=1)

            # Draw highlight
            canvas.setFillColor(white.clone(alpha=0.6))
            canvas.circle(x - 2, y + 2, 2, stroke=0, fill=1)

            # Draw day number in circle
            canvas.setFillColor(white)
            canvas.setFont("Helvetica-Bold", 7)
            canvas.drawCentredString(x, y - 2.5, f"{i+1}")

            # Draw text with shadow effect for depth
            # Day text shadow
            canvas.setFillColor(dimgrey.clone(alpha=0.5))
            day_txt = f"Day {i+1}"
            canvas.setFont("Helvetica-Bold", 9)
            canvas.drawCentredString(x + 0.5, y - 20.5, day_txt)

            # Day text
            canvas.setFillColor(TEXT_COLOR)
            canvas.drawCentredString(x, y - 20, day_txt)

            # Draw date with nicer formatting
            date_str = day_info["date"].strftime("%b %d")
            canvas.setFont("Helvetica", 8)
            canvas.drawCentredString(x, y - 35, date_str)

            # Draw location box for better visibility
            location = day_info["location"]
            canvas.setFont("Helvetica", 8)
            text_width = canvas.stringWidth(location, "Helvetica", 8)
            box_width = text_width + 10
            box_height = 15

            # Location box
            canvas.setFillColor(PRIMARY_COLOR.clone(alpha=0.15))
            canvas.roundRect(
                x - box_width / 2, y + 15, box_width, box_height, 3, stroke=0, fill=1
            )

            # Location text
            canvas.setFillColor(TEXT_COLOR)
            canvas.drawCentredString(x, y + 22, location)

            # Draw activity (rotated if needed)
            activity = day_info["activity"]
            if len(activity) > 15:
                activity = textwrap.fill(activity, width=15)

            # Activity box
            lines = activity.split("\n")
            act_box_height = len(lines) * 10 + 6
            act_box_width = (
                max(
                    [canvas.stringWidth(line, "Helvetica-Oblique", 7) for line in lines]
                )
                + 8
            )

            # Draw activity background
            canvas.setFillColor(TIMELINE_COLOR.clone(alpha=0.15))
            canvas.roundRect(
                x - act_box_width / 2,
                y + 40,
                act_box_width,
                act_box_height,
                3,
                stroke=0,
                fill=1,
            )

            # Draw activity text
            canvas.setFillColor(TEXT_COLOR)
            canvas.setFont("Helvetica-Oblique", 7)
            for j, line in enumerate(lines):
                canvas.drawCentredString(x, y + 45 + j * 10, line)

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

    def draw(self):
        canvas = self.canv
        canvas.saveState()

        # Draw shadow if specified
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

        # Draw rounded rectangle
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

        # Add gradient-like effect if background is set
        if self.backgroundColor:
            highlight_color = white.clone(alpha=0.2)
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

        # Draw contents
        if isinstance(self.contents, str):
            # If contents is a string, draw as a centered text
            canvas.setFont("Helvetica", 10)
            canvas.setFillColor(TEXT_COLOR)
            canvas.drawCentredString(self.width / 2, self.height / 2 - 4, self.contents)
        elif hasattr(self.contents, "draw"):
            # If contents is a flowable
            self.contents.wrapOn(
                canvas, self.width - 2 * self.padding, self.height - 2 * self.padding
            )
            self.contents.drawOn(canvas, self.padding, self.padding)

        canvas.restoreState()


class Divider(Flowable):
    def __init__(
        self, width, color=lightgrey, thickness=1, spacer=0.1 * inch, style="solid"
    ):
        Flowable.__init__(self)
        self.width = width
        self.color = color
        self.thickness = thickness
        self.spacer = spacer
        self.height = 2 * self.spacer + self.thickness
        self.style = style  # "solid", "dashed", or "fancy"

    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)

        y = self.spacer

        if self.style == "solid":
            self.canv.line(0, y, self.width, y)

        elif self.style == "dashed":
            dash_length = 5
            space_length = 3
            current_x = 0

            while current_x < self.width:
                end_x = min(current_x + dash_length, self.width)
                self.canv.line(current_x, y, end_x, y)
                current_x = end_x + space_length

        elif self.style == "fancy":
            # Draw a main line
            self.canv.line(0, y, self.width, y)

            # Draw decorative dots
            dot_count = int(self.width / 30)
            for i in range(dot_count):
                dot_x = (i + 0.5) * (self.width / dot_count)

                # Alternating dots above and below
                dot_y = y + 3 if i % 2 == 0 else y - 3

                self.canv.setFillColor(self.color)
                self.canv.circle(dot_x, dot_y, 1.5, fill=1, stroke=0)

            # Draw decorative elements at the ends
            self.canv.setFillColor(self.color)
            self.canv.circle(0, y, 3, fill=1, stroke=0)
            self.canv.circle(self.width, y, 3, fill=1, stroke=0)

        self.canv.restoreState()


class DecorationFlowable(Flowable):
    """A decorative element to add visual interest"""

    def __init__(self, width, height=30, color=ACCENT_COLOR, style="wave"):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color
        self.style = style  # "wave", "zigzag", "dots", "corners"

    def draw(self):
        canvas = self.canv
        canvas.saveState()

        if self.style == "wave":
            canvas.setStrokeColor(self.color)
            canvas.setLineWidth(1)

            amplitude = 5  # Height of the wave
            frequency = 20  # Number of wave cycles

            x_points = [x for x in range(0, int(self.width) + 1, 2)]
            y_points = [
                self.height / 2 + amplitude * sin(2 * pi * frequency * x / self.width)
                for x in x_points
            ]

            for i in range(len(x_points) - 1):
                canvas.line(x_points[i], y_points[i], x_points[i + 1], y_points[i + 1])

        elif self.style == "zigzag":
            canvas.setStrokeColor(self.color)
            canvas.setLineWidth(1)

            segment_width = 10
            segment_height = 6
            num_segments = int(self.width / segment_width) + 1

            canvas.setLineJoin(1)  # Rounded join
            path = canvas.beginPath()
            path.moveTo(0, self.height / 2)

            for i in range(num_segments):
                if i % 2 == 0:
                    y = self.height / 2 + segment_height
                else:
                    y = self.height / 2 - segment_height

                path.lineTo(i * segment_width, y)

            path.lineTo(self.width, self.height / 2)
            canvas.drawPath(path, stroke=1, fill=0)

        elif self.style == "dots":
            canvas.setFillColor(self.color)

            dot_spacing = 15
            num_dots = int(self.width / dot_spacing)

            for i in range(num_dots + 1):
                x = i * dot_spacing
                canvas.circle(x, self.height / 2, 2, stroke=0, fill=1)

        elif self.style == "corners":
            canvas.setStrokeColor(self.color)
            canvas.setLineWidth(1.5)
            corner_size = 10

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

        canvas.restoreState()


class PlaceholderImage(Flowable):
    def __init__(self, width, height, bgColor=lightgrey):
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
            self.width / 2, self.height / 2, "Image Not Available"
        )

        # Draw a camera icon
        self.canv.setStrokeColor(TEXT_COLOR)
        self.canv.setLineWidth(1)
        # Simple camera shape
        cx, cy = self.width / 2, self.height / 2 - 15
        w, h = 20, 15
        self.canv.roundRect(cx - w / 2, cy - h / 2, w, h, 2, stroke=1, fill=0)
        self.canv.circle(cx, cy, 5, stroke=1, fill=0)


class StarRating(Flowable):
    """A star rating display"""

    def __init__(self, rating, max_stars=5, star_size=12, star_color=SECONDARY_COLOR):
        Flowable.__init__(self)
        self.rating = min(rating, max_stars)  # Limit to max stars
        self.max_stars = max_stars
        self.star_size = star_size
        self.star_color = star_color
        self.width = (star_size * 1.2) * max_stars
        self.height = star_size * 1.5

    def draw(self):
        canvas = self.canv
        canvas.saveState()

        # Draw stars
        for i in range(self.max_stars):
            if i < int(self.rating):
                # Full star
                self._draw_star(canvas, i * self.star_size * 1.2, filled=True)
            elif i < self.rating:
                # Partial star
                fraction = self.rating - int(self.rating)
                self._draw_star(
                    canvas, i * self.star_size * 1.2, filled=True, fraction=fraction
                )
            else:
                # Empty star
                self._draw_star(canvas, i * self.star_size * 1.2, filled=False)

        canvas.restoreState()

    def _draw_star(self, canvas, x_offset, filled=True, fraction=1.0):
        """Draw a single star"""
        points = []
        size = self.star_size
        center_x = x_offset + size / 2
        center_y = size / 2

        # Create star points
        for i in range(5):
            # Outer points (star tips)
            angle = (2 * pi * i / 5) - pi / 2
            points.append(
                (center_x + size / 2 * cos(angle), center_y + size / 2 * sin(angle))
            )

            # Inner points
            angle += pi / 5
            points.append(
                (center_x + size / 5 * cos(angle), center_y + size / 5 * sin(angle))
            )

        # Draw the star
        path = canvas.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for point in points[1:]:
            path.lineTo(point[0], point[1])
        path.close()

        if filled:
            canvas.setFillColor(self.star_color)
            if fraction < 1.0:
                # Draw the partial star by clipping
                canvas.saveState()
                canvas.clipPath(path, stroke=0)
                canvas.setFillColor(self.star_color)
                canvas.rect(
                    center_x - size / 2,
                    center_y - size / 2,
                    size * fraction,
                    size,
                    stroke=0,
                    fill=1,
                )
                canvas.restoreState()

                # Draw the outline of the entire star
                canvas.setStrokeColor(self.star_color)
                canvas.setLineWidth(0.5)
                canvas.drawPath(path, stroke=1, fill=0)
            else:
                canvas.setStrokeColor(self.star_color)
                canvas.drawPath(path, stroke=1, fill=1)
        else:
            # Empty star (just outline)
            canvas.setStrokeColor(self.star_color)
            canvas.setLineWidth(0.5)
            canvas.drawPath(path, stroke=1, fill=0)


# --- Helper to get image from URL ---
def get_image_from_url(url, width=2 * inch):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, stream=True, timeout=10, headers=headers)
        response.raise_for_status()
        img_data = response.content

        # Save to a temporary file to avoid BytesIO issues
        temp_img = BytesIO(img_data)
        img = Image(temp_img, width=width)

        # Maintain aspect ratio
        img.drawHeight = width * img.imageHeight / img.imageWidth
        img.drawWidth = width
        return img
    except Exception as e:
        print(f"Warning: Could not fetch image from {url}. Error: {e}")
        # Create a placeholder rectangle instead
        placeholder = PlaceholderImage(width, width * 0.75)
        return placeholder


# --- Header and Footer with custom logo ---
def header_footer(canvas, doc):
    canvas.saveState()

    # Get logo
    try:
        # Use a simpler approach for logo
        canvas.setFont("Helvetica-Bold", 16)
        canvas.setFillColor(PRIMARY_COLOR)
        canvas.drawString(
            doc.leftMargin, doc.height + doc.topMargin - 0.4 * inch, COMPANY_NAME
        )
    except Exception as e:
        print(f"Error with logo: {e}")

    # Header
    canvas.setFont("Helvetica", 10)
    canvas.setFillColor(LIGHT_TEXT_COLOR)
    canvas.drawString(
        doc.leftMargin + 1.2 * inch,
        doc.height + doc.topMargin - 0.35 * inch,
        COMPANY_SLOGAN,
    )

    header_line_y = doc.height + doc.topMargin - 0.6 * inch
    canvas.setStrokeColor(PRIMARY_COLOR)
    canvas.setLineWidth(1.5)
    canvas.line(
        doc.leftMargin, header_line_y, doc.leftMargin + doc.width, header_line_y
    )

    # Footer
    footer_text = f"{COMPANY_NAME} | {WEBSITE} | {PHONE}"
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(LIGHT_TEXT_COLOR)
    canvas.drawCentredString(doc.leftMargin + doc.width / 2, 0.5 * inch, footer_text)

    # Page number
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(PRIMARY_COLOR)
    page_num = f"Page {doc.page}"
    canvas.drawRightString(doc.leftMargin + doc.width, 0.5 * inch, page_num)

    footer_line_y = 0.7 * inch
    canvas.setStrokeColor(PRIMARY_COLOR)
    canvas.setLineWidth(1.5)
    canvas.line(
        doc.leftMargin, footer_line_y, doc.leftMargin + doc.width, footer_line_y
    )

    canvas.restoreState()


# Custom first page - add the missing function
def cover_page(canvas, doc):
    canvas.saveState()

    try:
        # Try to draw the background image for the cover
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(
            IMAGES["cover_image"], stream=True, timeout=10, headers=headers
        )
        response.raise_for_status()

        # Create a temporary file for the image
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name

        # Draw the cover image
        canvas.drawImage(
            temp_path, 0, 0, width=A4[0], height=A4[1], preserveAspectRatio=False
        )

        # Clean up temporary file
        import os

        os.unlink(temp_path)

        # Add semi-transparent overlay for better text readability
        canvas.setFillColorRGB(0, 0, 0, 0.5)  # Black with 50% opacity
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)

    except Exception as e:
        print(f"Error with cover image: {e}")
        # Fallback to a solid color if image fails
        canvas.setFillColor(PRIMARY_COLOR)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)

    canvas.restoreState()


# --- Styles ---
styles = getSampleStyleSheet()

# Modify the existing BodyText style
styles["BodyText"].fontName = "Helvetica"
styles["BodyText"].fontSize = 10
styles["BodyText"].leading = 14
styles["BodyText"].textColor = TEXT_COLOR
styles["BodyText"].alignment = TA_JUSTIFY
styles["BodyText"].spaceAfter = 0.1 * inch

# Add new styles and update existing ones
# Define HighlightText style if it doesn't exist
styles.add(
    ParagraphStyle(
        name="HighlightText",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        textColor=HIGHLIGHT_COLOR,
    )
)

# Define PackageHighlight style if it doesn't exist
if "PackageHighlight" not in styles:
    styles.add(
        ParagraphStyle(
            name="PackageHighlight",
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=14,
            textColor=ACCENT_COLOR,
            alignment=TA_LEFT,
        )
    )

# Define ContactInfo style if it doesn't exist
if "ContactInfo" not in styles:
    styles.add(
        ParagraphStyle(
            name="ContactInfo",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=TEXT_COLOR,
            spaceAfter=0.05 * inch,
            alignment=TA_LEFT,
        )
    )

# Define TestimonialText style if it doesn't exist
if "TestimonialText" not in styles:
    styles.add(
        ParagraphStyle(
            name="TestimonialText",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=TEXT_COLOR,
            alignment=TA_LEFT,
            firstLineIndent=10,
            spaceAfter=0.05 * inch,
            italic=1,
        )
    )

# Define TestimonialAuthor style if it doesn't exist
if "TestimonialAuthor" not in styles:
    styles.add(
        ParagraphStyle(
            name="TestimonialAuthor",
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=ACCENT_COLOR,
            alignment=TA_RIGHT,
        )
    )


# --- Build PDF ---
def build_pdf():
    # Reference the global styles
    global styles

    # Create document with multiple page templates
    doc = SimpleDocTemplate(
        FILENAME,
        pagesize=A4,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=1.2 * inch,
        bottomMargin=0.8 * inch,
    )

    # Create page templates
    cover_template = PageTemplate(
        id="cover",
        frames=[
            Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
        ],
        onPage=cover_page,
    )

    # Two-column layout for some pages
    content_template = PageTemplate(
        id="content",
        frames=[
            Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
        ],
        onPage=header_footer,
    )

    # Two-column layout for some pages
    two_column_template = PageTemplate(
        id="two_column",
        frames=[
            Frame(
                doc.leftMargin,
                doc.bottomMargin,
                doc.width / 2 - 0.25 * inch,
                doc.height,
                id="col1",
            ),
            Frame(
                doc.leftMargin + doc.width / 2 + 0.25 * inch,
                doc.bottomMargin,
                doc.width / 2 - 0.25 * inch,
                doc.height,
                id="col2",
            ),
        ],
        onPage=header_footer,
    )

    doc.addPageTemplates([cover_template, content_template, two_column_template])

    # Initialize story
    story = []

    # --- Cover Page ---
    story.append(NextPageTemplate("cover"))
    story.append(Spacer(1, 3 * inch))  # Push content down
    story.append(Paragraph("Karnataka's Treasures", styles["CoverTitle"]))
    story.append(
        Paragraph(
            "A Scenic Getaway Through Western Ghats & Coastal Beauty",
            styles["CoverSubtitle"],
        )
    )

    # Cover page details
    story.append(Spacer(1, 2 * inch))
    price_text = f"Starting from {package_info['Standard']['price']} per person"
    price_para = Paragraph(
        price_text,
        ParagraphStyle(
            name="CoverPrice",
            parent=styles["CoverSubtitle"],
            fontSize=30,  # Larger for emphasis
            textColor=SECONDARY_COLOR,
            italic=0,
        ),
    )
    story.append(price_para)

    story.append(Spacer(1, 0.5 * inch))
    duration = package_info["Standard"]["duration"]
    story.append(
        Paragraph(
            duration,
            ParagraphStyle(
                name="CoverDuration",
                parent=styles["CoverSubtitle"],
                fontSize=18,
            ),
        )
    )

    story.append(PageBreak())

    # --- Table of Contents ---
    story.append(NextPageTemplate("content"))

    # TOC Title with decoration
    story.append(DecorationFlowable(doc.width, style="corners"))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Your Karnataka Adventure", styles["MainTitle"]))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Contents", styles["TOC"]))
    story.append(Spacer(1, 0.1 * inch))

    # TOC Entries
    toc_items = [
        ("Welcome", 3),
        ("Your 7-Day Journey", 4),
        ("Destinations", 5),
        ("   • Kalasa: Spiritual Charm & Lush Landscapes", 5),
        ("   • Udupi: Coastal Beauty & Temple Heritage", 6),
        ("   • Kudremukh: Rolling Grasslands & Wildlife", 7),
        ("   • Netravati Peak: Trekker's Paradise", 8),
        ("Tour Packages", 9),
        ("What Our Clients Say", 10),
        ("Contact Information", 11),
    ]

    # Create TOC table for better formatting
    toc_data = []
    for item, page in toc_items:
        # Check indentation level
        if item.startswith("   "):
            style = styles["TOCEntry2"]
            item = item.strip()
        else:
            style = styles["TOCEntry1"]

        # Create dot leaders
        leader_dots = "." * 50  # Adjust number for spacing

        toc_data.append(
            [
                Paragraph(item, style),
                Paragraph(
                    leader_dots,
                    ParagraphStyle(
                        name="dots",
                        fontName="Helvetica",
                        fontSize=8,
                        textColor=lightgrey,
                    ),
                ),
                Paragraph(str(page), style),
            ]
        )

    toc_table = Table(
        toc_data,
        colWidths=[doc.width * 0.7, doc.width * 0.2, doc.width * 0.1],
        style=TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("RIGHTPADDING", (0, 0), (0, -1), 0),
                ("LEFTPADDING", (1, 0), (1, -1), 0),
                ("RIGHTPADDING", (1, 0), (1, -1), 0),
                ("LEFTPADDING", (2, 0), (2, -1), 0),
                ("ALIGN", (2, 0), (2, -1), "RIGHT"),
            ]
        ),
    )
    story.append(toc_table)

    story.append(Spacer(1, 0.2 * inch))
    story.append(DecorationFlowable(doc.width, style="corners"))

    # Image collage preview
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Preview of Your Journey", styles["SubSectionTitle"]))
    story.append(Spacer(1, 0.2 * inch))

    # Create a photo gallery table of small preview images
    try:
        image_urls = [
            IMAGES[key]
            for key in [
                "kalasa_bridge",
                "udupi_beach",
                "kudremukh_park",
                "netravati_peak",
            ]
        ]
        images = [get_image_from_url(url, width=1.2 * inch) for url in image_urls]

        # Arrange images in a 2x2 grid
        image_grid = [
            [images[0], images[1]],
            [images[2], images[3]],
        ]

        gallery_table = Table(
            image_grid, colWidths=[1.2 * inch] * 2, rowHeights=[0.9 * inch] * 2
        )

        gallery_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        # Center the gallery table
        gallery_wrapper = Table(
            [[gallery_table]],
            colWidths=[doc.width],
            style=TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            ),
        )

        story.append(gallery_wrapper)
    except Exception as e:
        print(f"Error creating image gallery: {e}")

    story.append(PageBreak())

    # --- Welcome Message ---
    story.append(Paragraph("Welcome", styles["SectionTitle"]))

    # Decorative element
    story.append(DecorationFlowable(width=3 * inch, style="wave"))
    story.append(Spacer(1, 0.1 * inch))

    # Welcome box with shadow
    welcome_box = RoundedBox(
        Paragraph(
            f"Welcome to your exclusive Karnataka adventure with {COMPANY_NAME}! "
            f"This brochure outlines your upcoming journey through some of the most "
            f"breathtaking locations in Karnataka. Get ready to explore ancient temples, "
            f"pristine beaches, lush forests, and majestic peaks.",
            styles["BodyText"],
        ),
        width=doc.width,
        height=1.4 * inch,
        backgroundColor=PALE_BLUE,
        borderColor=PRIMARY_COLOR,
        shadowColor=dimgrey.clone(alpha=0.3),
        padding=15,
    )
    story.append(welcome_box)
    story.append(Spacer(1, 0.3 * inch))

    # Highlight paragraph
    story.append(
        Paragraph(
            "Get ready for a <b>transformative journey</b> through Karnataka's diverse landscapes, "
            "from the spiritual serenity of <i>Kalasa</i> to the coastal charm of <i>Udupi</i>, "
            "the wilderness of <i>Kudremukh</i>, and the majestic peaks of <i>Netravati</i>. "
            "Our carefully crafted itinerary ensures you experience the best of Karnataka's natural "
            "beauty, cultural heritage, and local cuisine.",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    # Itinerary Timeline
    story.append(Paragraph("Your 7-Day Journey", styles["SectionTitle"]))

    # Decorative element
    story.append(DecorationFlowable(width=3 * inch, style="zigzag"))
    story.append(Spacer(1, 0.2 * inch))

    # Enhanced timeline
    story.append(TimelineFlowable(create_itinerary(), width=doc.width))
    story.append(Spacer(1, 0.3 * inch))

    # Map of the journey with decoration
    story.append(Paragraph("Your Journey Through Karnataka", styles["SectionTitle"]))
    story.append(DecorationFlowable(width=3 * inch, style="dots"))
    story.append(Spacer(1, 0.1 * inch))

    try:
        # Create a map placeholder with better styling
        map_container = RoundedBox(
            PlaceholderImage(5 * inch, 3.5 * inch, bgColor=PALE_BLUE),
            width=5 * inch,
            height=3.5 * inch,
            backgroundColor=None,
            borderColor=PRIMARY_COLOR,
            radius=5,
            shadowColor=dimgrey.clone(alpha=0.3),
        )

        # Wrap map in table for centering
        map_table = Table(
            [
                [map_container],
                [
                    Paragraph(
                        "<i>Explore Karnataka's most scenic locations</i>",
                        styles["CaptionText"],
                    )
                ],
            ],
            colWidths=[5 * inch],
            style=TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            ),
        )

        # Center the map table
        story.append(
            Table(
                [[map_table]],
                colWidths=[doc.width],
                style=TableStyle(
                    [
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ]
                ),
            )
        )
    except Exception as e:
        print(f"Error with map: {e}")

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Divider(width=doc.width, style="fancy", color=PRIMARY_COLOR.clone(alpha=0.6))
    )
    story.append(Spacer(1, 0.3 * inch))

    # --- Destinations Section Title ---
    story.append(Paragraph("Destinations", styles["SectionTitle"]))
    story.append(DecorationFlowable(width=3 * inch, style="wave"))
    story.append(Spacer(1, 0.2 * inch))

    # --- Kalasa ---
    story.append(
        Paragraph(
            "Kalasa: Spiritual Charm & Lush Landscapes", styles["SubSectionTitle"]
        )
    )

    img_kalasa_bridge = get_image_from_url(IMAGES["kalasa_bridge"], width=2.5 * inch)
    img_kalasa_viewpoint = get_image_from_url(
        IMAGES["kalasa_viewpoint"], width=2.5 * inch
    )

    # Enhanced content layout with background colors and shadows
    kalasa_box = RoundedBox(
        Paragraph(kalasa_desc, styles["BodyText"]),
        width=doc.width - 2.8 * inch,
        height=2.5 * inch,
        backgroundColor=PALE_GREEN.clone(alpha=0.7),
        borderColor=None,
        padding=15,
        shadowColor=dimgrey.clone(alpha=0.2),
        shadowOffset=3,
    )

    kalasa_content = [
        [img_kalasa_bridge, kalasa_box],
        [
            Paragraph(
                "<i>Kalasa Hanging Bridge: A walk to remember</i>",
                styles["CaptionText"],
            ),
            "",
        ],
    ]

    kalasa_table = Table(kalasa_content, colWidths=[2.8 * inch, doc.width - 2.8 * inch])
    kalasa_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (1, 0), (1, -1), 0.3 * inch),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0.1 * inch),
            ]
        )
    )
    story.append(kalasa_table)

    # Key attractions
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Key Attractions:", styles["HighlightText"]))

    attractions = ListFlowable(
        [
            ListItem(Paragraph("Ambaa Teertha Viewpoint", styles["BodyText"])),
            ListItem(Paragraph("Ancient Temples", styles["BodyText"])),
            ListItem(Paragraph("Hanging Bridge", styles["BodyText"])),
            ListItem(Paragraph("Bhadra River", styles["BodyText"])),
        ],
        bulletType="bullet",
        leftIndent=20,
        spaceBefore=5,
        spaceAfter=10,
    )
    story.append(attractions)

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Divider(width=doc.width, style="dashed", color=PRIMARY_COLOR.clone(alpha=0.6))
    )
    story.append(Spacer(1, 0.3 * inch))

    # --- Udupi with improved layout ---
    story.append(
        Paragraph("Udupi: Coastal Beauty & Temple Heritage", styles["SubSectionTitle"])
    )

    # Get Udupi images (or placeholders)
    img_udupi_beach = get_image_from_url(IMAGES["udupi_beach"], width=2.5 * inch)
    img_udupi_temple = get_image_from_url(IMAGES["udupi_temple"], width=2.5 * inch)

    # Enhanced content layout
    udupi_box = RoundedBox(
        Paragraph(udupi_desc, styles["BodyText"]),
        width=doc.width - 2.8 * inch,
        height=2.5 * inch,
        backgroundColor=PALE_YELLOW.clone(alpha=0.7),
        borderColor=None,
        padding=15,
        shadowColor=dimgrey.clone(alpha=0.2),
        shadowOffset=3,
    )

    udupi_content = [
        [udupi_box, img_udupi_beach],
        ["", Paragraph("<i>Serene beaches of Udupi</i>", styles["CaptionText"])],
    ]

    udupi_table = Table(udupi_content, colWidths=[doc.width - 2.8 * inch, 2.8 * inch])
    udupi_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("RIGHTPADDING", (0, 0), (0, -1), 0.3 * inch),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0.1 * inch),
            ]
        )
    )
    story.append(udupi_table)

    # Key attractions
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Key Attractions:", styles["HighlightText"]))

    attractions = ListFlowable(
        [
            ListItem(Paragraph("Sri Krishna Temple", styles["BodyText"])),
            ListItem(Paragraph("Malpe Beach", styles["BodyText"])),
            ListItem(Paragraph("St. Mary's Island", styles["BodyText"])),
            ListItem(Paragraph("Authentic Udupi Cuisine", styles["BodyText"])),
        ],
        bulletType="bullet",
        leftIndent=20,
        spaceBefore=5,
        spaceAfter=10,
    )
    story.append(attractions)

    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph(
            "<i>Pro Tip: Don't miss trying the famous Udupi dosa and filter coffee!</i>",
            styles["SideNote"],
        )
    )

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Divider(width=doc.width, style="dashed", color=PRIMARY_COLOR.clone(alpha=0.6))
    )
    story.append(Spacer(1, 0.3 * inch))

    # --- Kudremukh ---
    story.append(
        Paragraph("Kudremukh: Rolling Grasslands & Wildlife", styles["SubSectionTitle"])
    )

    img_kudremukh_park = get_image_from_url(IMAGES["kudremukh_park"], width=2.5 * inch)
    img_kudremukh_dam = get_image_from_url(IMAGES["kudremukh_dam"], width=2.5 * inch)

    kudremukh_content = [
        [img_kudremukh_park, Paragraph(kudremukh_desc, styles["BodyText"])],
        [
            Paragraph(
                "<i>Kudremukh National Park: Biodiversity Hotspot</i>",
                styles["CaptionText"],
            ),
            "",
        ],
        [
            img_kudremukh_dam,
            Paragraph(
                "The Lakya Dam area provides breathtaking views and highlights the region's water resources.",
                styles["BodyText"],
            ),
        ],
        [
            Paragraph(
                "<i>Lakya Dam Viewpoint: Serene Waterscape</i>", styles["CaptionText"]
            ),
            "",
        ],
    ]
    kudremukh_table = Table(
        kudremukh_content, colWidths=[2.8 * inch, doc.width - 2.8 * inch]
    )
    kudremukh_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (1, 0), (1, -1), 0.3 * inch),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0.1 * inch),
            ]
        )
    )
    story.append(kudremukh_table)

    # Key attractions
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Key Attractions:", styles["HighlightText"]))

    attractions = ListFlowable(
        [
            ListItem(Paragraph("Kudremukh National Park", styles["BodyText"])),
            ListItem(Paragraph("Lakya Dam", styles["BodyText"])),
            ListItem(Paragraph("Hanuman Gundi Falls", styles["BodyText"])),
            ListItem(Paragraph("Diverse Flora and Fauna", styles["BodyText"])),
        ],
        bulletType="bullet",
        leftIndent=20,
        spaceBefore=5,
        spaceAfter=10,
    )
    story.append(attractions)

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Divider(width=doc.width, style="dashed", color=PRIMARY_COLOR.clone(alpha=0.6))
    )
    story.append(Spacer(1, 0.3 * inch))

    # --- Netravati Peak ---
    story.append(
        Paragraph("Netravati Peak: Trekker's Paradise", styles["SubSectionTitle"])
    )
    img_netravati = get_image_from_url(IMAGES["netravati_peak"], width=2.5 * inch)

    netravati_content = [
        [img_netravati, Paragraph(netravati_desc, styles["BodyText"])],
        [
            Paragraph(
                "<i>Netravati Peak Trek: Breathtaking Vistas</i>", styles["CaptionText"]
            ),
            "",
        ],
    ]
    netravati_table = Table(
        netravati_content, colWidths=[2.8 * inch, doc.width - 2.8 * inch]
    )
    netravati_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (1, 0), (1, -1), 0.3 * inch),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0.1 * inch),
            ]
        )
    )
    story.append(netravati_table)

    # Key attractions
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Key Attractions:", styles["HighlightText"]))

    attractions = ListFlowable(
        [
            ListItem(Paragraph("Netravati Peak", styles["BodyText"])),
            ListItem(Paragraph("Sunrise Views", styles["BodyText"])),
            ListItem(Paragraph("Birdwatching", styles["BodyText"])),
            ListItem(Paragraph("Scenic Trekking Trails", styles["BodyText"])),
        ],
        bulletType="bullet",
        leftIndent=20,
        spaceBefore=5,
        spaceAfter=10,
    )
    story.append(attractions)

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Divider(width=doc.width, style="dashed", color=PRIMARY_COLOR.clone(alpha=0.6))
    )
    story.append(Spacer(1, 0.3 * inch))

    # --- Package Options with two-column layout ---
    story.append(PageBreak())
    story.append(NextPageTemplate("two_column"))

    story.append(Paragraph("Tour Packages", styles["SectionTitle"]))
    story.append(DecorationFlowable(width=3 * inch, style="wave"))
    story.append(Spacer(1, 0.2 * inch))

    # Standard Package
    standard_content = []

    # Package title
    standard_content.append(Paragraph("Standard Package", styles["SubSectionTitle"]))

    # Price and rating on same line
    price_rating_table = Table(
        [
            [
                Paragraph(
                    f"<b>Price:</b> {package_info['Standard']['price']} per person",
                    styles["PackageHighlight"],
                ),
                StarRating(package_info["Standard"]["rating"]),
            ]
        ],
        colWidths=[3 * inch, 1.5 * inch],
        style=TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        ),
    )
    standard_content.append(price_rating_table)

    # Duration
    standard_content.append(
        Paragraph(
            f"<b>Duration:</b> {package_info['Standard']['duration']}",
            styles["BodyText"],
        )
    )

    # Ideal for
    standard_content.append(
        Paragraph(
            f"<b>Ideal for:</b> {package_info['Standard']['ideal_for']}",
            styles["BodyText"],
        )
    )

    standard_content.append(Spacer(1, 0.1 * inch))
    standard_content.append(Paragraph("<b>Inclusions:</b>", styles["BodyText"]))

    # Inclusions list
    inclusions = ListFlowable(
        [
            ListItem(Paragraph(item, styles["BodyText"]))
            for item in package_info["Standard"]["includes"]
        ],
        bulletType="bullet",
        leftIndent=20,
        spaceBefore=5,
        spaceAfter=10,
    )
    standard_content.append(inclusions)

    # Highlights
    standard_content.append(Spacer(1, 0.1 * inch))
    standard_content.append(
        Paragraph(
            f"<b>Highlights:</b> {package_info['Standard']['highlights']}",
            styles["BodyText"],
        )
    )

    # Add standard package to story
    for item in standard_content:
        story.append(item)

    # Premium Package (will go to second column)
    story.append(FrameBreak())
    premium_content = []

    # Package title with premium marker
    premium_title_table = Table(
        [
            [
                Paragraph("Premium Package", styles["SubSectionTitle"]),
                RoundedBox(
                    Paragraph(
                        "BEST VALUE",
                        ParagraphStyle(
                            name="BestValue",
                            fontName="Helvetica-Bold",
                            fontSize=8,
                            textColor=white,
                            alignment=TA_CENTER,
                        ),
                    ),
                    width=1 * inch,
                    height=0.3 * inch,
                    backgroundColor=HIGHLIGHT_COLOR,
                    borderColor=None,
                ),
            ]
        ],
        colWidths=[2.5 * inch, 1.5 * inch],
        style=TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ]
        ),
    )
    premium_content.append(premium_title_table)

    # Price and rating
    price_rating_table = Table(
        [
            [
                Paragraph(
                    f"<b>Price:</b> {package_info['Premium']['price']} per person",
                    styles["PackageHighlight"],
                ),
                StarRating(package_info["Premium"]["rating"]),
            ]
        ],
        colWidths=[3 * inch, 1.5 * inch],
        style=TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        ),
    )
    premium_content.append(price_rating_table)

    # Duration
    premium_content.append(
        Paragraph(
            f"<b>Duration:</b> {package_info['Premium']['duration']}",
            styles["BodyText"],
        )
    )

    # Ideal for
    premium_content.append(
        Paragraph(
            f"<b>Ideal for:</b> {package_info['Premium']['ideal_for']}",
            styles["BodyText"],
        )
    )

    premium_content.append(Spacer(1, 0.1 * inch))
    premium_content.append(Paragraph("<b>Inclusions:</b>", styles["BodyText"]))

    # Premium inclusions with highlighted differences
    premium_inclusions = []
    for i, item in enumerate(package_info["Premium"]["includes"]):
        if (
            i >= len(package_info["Standard"]["includes"])
            or item != package_info["Standard"]["includes"][i]
        ):
            # This is a premium-only feature
            premium_inclusions.append(
                ListItem(
                    Paragraph(f"{item} <i>(Premium only)</i>", styles["HighlightText"])
                )
            )
        else:
            premium_inclusions.append(ListItem(Paragraph(item, styles["BodyText"])))

    premium_content.append(
        ListFlowable(
            premium_inclusions,
            bulletType="bullet",
            leftIndent=20,
            spaceBefore=5,
            spaceAfter=10,
        )
    )

    # Highlights
    premium_content.append(Spacer(1, 0.1 * inch))
    premium_content.append(
        Paragraph(
            f"<b>Highlights:</b> {package_info['Premium']['highlights']}",
            styles["BodyText"],
        )
    )

    # Add premium package to story (in second column)
    for item in premium_content:
        story.append(item)

    # --- Testimonials with enhanced design ---
    story.append(PageBreak())
    story.append(NextPageTemplate("content"))
    story.append(Paragraph("What Our Clients Say", styles["SectionTitle"]))
    story.append(DecorationFlowable(width=3 * inch, style="wave"))
    story.append(Spacer(1, 0.2 * inch))

    # Enhanced testimonial boxes
    testimonial_data = []
    for i, testimonial in enumerate(testimonials):
        # Create decorative quote marks
        quote_marks = Paragraph(
            '"',
            ParagraphStyle(
                name="QuoteMarks",
                fontName="Helvetica-Bold",
                fontSize=36,
                textColor=ACCENT_COLOR.clone(alpha=0.3),
                alignment=TA_LEFT,
            ),
        )

        # Main testimonial text
        testimonial_text = Paragraph(
            f'{testimonial["text"]}',
            styles["TestimonialText"],
        )

        # Author
        author_text = Paragraph(
            f'- {testimonial["author"]}',
            styles["TestimonialAuthor"],
        )

        # Assemble the testimonial components
        testimonial_content = Table(
            [[quote_marks], [testimonial_text], [Spacer(1, 0.1 * inch)], [author_text]],
            colWidths=[(doc.width - 0.8 * inch) / 3 - 20],
            style=TableStyle(
                [
                    ("TOPPADDING", (0, 0), (0, 0), 0),
                    ("BOTTOMPADDING", (0, 0), (0, 0), -10),  # Overlap quote with text
                    ("LEFTPADDING", (0, 0), (0, 0), 0),
                    ("ALIGN", (-1, -1), (-1, -1), "RIGHT"),  # Right-align author
                ]
            ),
        )

        # Create fancy testimonial box
        testimonial_box = RoundedBox(
            testimonial_content,
            width=(doc.width - 0.8 * inch) / 3,
            height=2.5 * inch,
            radius=10,
            backgroundColor=PALE_BLUE.clone(alpha=0.5),
            borderColor=ACCENT_COLOR.clone(alpha=0.3),
            padding=10,
            shadowColor=dimgrey.clone(alpha=0.2),
            shadowOffset=3,
        )

        testimonial_data.append(testimonial_box)

    # Create a row of testimonials
    testimonials_table = Table(
        [testimonial_data],
        colWidths=[(doc.width - 0.8 * inch) / 3] * 3,
        rowHeights=[2.5 * inch + 0.2 * inch],  # Add extra space for shadow
    )
    testimonials_table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0.1 * inch),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0.1 * inch),
                ("TOPPADDING", (0, 0), (-1, -1), 0.1 * inch),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0.1 * inch),
            ]
        )
    )
    story.append(testimonials_table)

    # --- Enhanced Contact Information ---
    story.append(PageBreak())
    story.append(Paragraph("Contact Information", styles["SectionTitle"]))
    story.append(DecorationFlowable(width=3 * inch, style="wave"))
    story.append(Spacer(1, 0.2 * inch))

    # Introduction text
    story.append(
        Paragraph(
            f"Ready to embark on your Karnataka adventure? Contact our friendly team at {COMPANY_NAME} "
            f"to customize your journey or make a booking. We're here to answer all your questions "
            f"and ensure your trip is tailored to your preferences.",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 0.3 * inch))

    # Create a more attractive contact information section with icons
    contact_info = Table(
        [
            [
                Paragraph(f"<b>✆ Phone:</b>", styles["ContactInfo"]),
                Paragraph(PHONE, styles["ContactInfo"]),
            ],
            [
                Paragraph(f"<b>✉ Email:</b>", styles["ContactInfo"]),
                Paragraph(EMAIL, styles["ContactInfo"]),
            ],
            [
                Paragraph(f"<b>🌐 Website:</b>", styles["ContactInfo"]),
                Paragraph(WEBSITE, styles["ContactInfo"]),
            ],
        ],
        colWidths=[1.5 * inch, doc.width - 1.5 * inch],
        style=TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.5, PALE_BLUE),  # Light grid lines
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    PALE_BLUE.clone(alpha=0.3),
                ),  # Light background for first column
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        ),
    )
    story.append(contact_info)

    # Social media section
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Connect With Us", styles["SubSectionTitle"]))
    story.append(Spacer(1, 0.1 * inch))

    # Social media table
    social_data = []
    for platform, handle in SOCIAL_MEDIA.items():
        # Determine icon based on platform
        if platform == "Facebook":
            icon = "ƒ"  # Simple representation for Facebook
        elif platform == "Instagram":
            icon = "📷"  # Camera for Instagram
        elif platform == "Twitter":
            icon = "🐦"  # Bird for Twitter
        else:
            icon = "🔗"  # Generic link

        social_data.append(
            [
                Paragraph(f"<b>{icon} {platform}:</b>", styles["ContactInfo"]),
                Paragraph(handle, styles["ContactInfo"]),
            ]
        )

    social_table = Table(
        social_data,
        colWidths=[1.5 * inch, doc.width - 1.5 * inch],
        style=TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.5, PALE_YELLOW),  # Light grid lines
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    PALE_YELLOW.clone(alpha=0.3),
                ),  # Light background for first column
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        ),
    )
    story.append(social_table)

    # Office hours
    story.append(Spacer(1, 0.2 * inch))
    story.append(
        Paragraph(
            "<b>Office Hours:</b> Monday to Saturday, 9:00 AM to 6:00 PM IST",
            styles["BodyText"],
        )
    )

    # Final message
    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "We look forward to helping you plan your unforgettable journey through Karnataka!",
            styles["BodyText"],
        )
    )

    # Call to action with enhanced design
    story.append(Spacer(1, 0.4 * inch))

    # CTA content
    cta_text = Paragraph(
        "<b>Ready to book your adventure?</b><br/>"
        "Contact us today to secure your spot on this incredible journey. "
        "Early bookings receive special discounts!",
        ParagraphStyle(
            name="CTAText",
            parent=styles["BodyText"],
            alignment=TA_CENTER,
            textColor=white,
        ),
    )

    cta_box = RoundedBox(
        cta_text,
        width=doc.width,
        height=1.2 * inch,
        radius=15,  # More rounded corners
        backgroundColor=ACCENT_COLOR,
        borderColor=ACCENT_COLOR,
        padding=15,
        shadowColor=dimgrey.clone(alpha=0.4),
        shadowOffset=4,
    )
    story.append(cta_box)

    # Build the PDF
    try:
        doc.build(story)
        print(f"PDF '{FILENAME}' generated successfully.")
    except Exception as e:
        print(f"Error building PDF: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    build_pdf()

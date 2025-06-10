import math
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

# --- Color Definitions ---
PRIMARY_COLOR = HexColor("#1a75ff")  # Blue
SECONDARY_COLOR = HexColor("#ff8c1a")  # Orange
ACCENT_COLOR = HexColor("#009933")  # Green
HIGHLIGHT_COLOR = HexColor("#ff3300")  # Red
TEXT_COLOR = HexColor("#333333")  # Dark gray
LIGHT_TEXT_COLOR = HexColor("#666666")  # Light gray
PALE_BLUE = HexColor("#e6f0ff")  # Light blue background
PALE_GREEN = HexColor("#e6ffe6")  # Light green background
PALE_YELLOW = HexColor("#fffce6")  # Light yellow background

# --- Date Configuration ---
START_DATE = datetime(2025, 6, 1)  # June 1, 2025
TOTAL_DAYS = 7

# --- Image URLs ---
IMAGES = {
    "cover_image": "https://example.com/karnataka_cover.jpg",
    "kalasa_bridge": "https://example.com/kalasa_bridge.jpg",
    "kalasa_viewpoint": "https://example.com/kalasa_viewpoint.jpg",
    "udupi_beach": "https://example.com/udupi_beach.jpg",
    "udupi_temple": "https://example.com/udupi_temple.jpg",
    "kudremukh_park": "https://example.com/kudremukh_park.jpg",
    "kudremukh_dam": "https://example.com/kudremukh_dam.jpg",
    "netravati_peak": "https://example.com/netravati_peak.jpg",
}

# --- Destination Descriptions ---
kalasa_desc = """Nestled in the Western Ghats of Karnataka, Kalasa is a serene town known for its spiritual significance and natural beauty. Surrounded by lush green forests, rolling hills, and meandering rivers, it offers a perfect retreat for those seeking tranquility away from the bustling city life. The town is home to ancient temples, scenic viewpoints, and the iconic hanging bridge over the Bhadra River."""

udupi_desc = """Udupi, a coastal gem of Karnataka, is famous for its pristine beaches, ancient temples, and mouth-watering cuisine. The Sri Krishna Temple stands as the town's spiritual heart, attracting pilgrims from across the country. Just a short drive away, Malpe Beach offers golden sands and azure waters perfect for a relaxing day by the sea. Don't miss St. Mary's Island with its unique hexagonal basalt rock formations."""

kudremukh_desc = """Named after the horse-faced mountain peak, Kudremukh National Park is a biodiversity hotspot nestled in the Western Ghats. Home to lush grasslands, dense forests, and diverse wildlife, it's a paradise for nature enthusiasts and adventure seekers. The area boasts numerous trekking trails, cascading waterfalls, and the scenic Lakya Dam surrounded by mist-covered hills."""

netravati_desc = """Netravati Peak offers one of the most breathtaking trekking experiences in Karnataka. Standing tall in the Western Ghats, this summit provides panoramic views of the surrounding valleys, dense forests, and the distant Arabian Sea on clear days. The trek to the peak takes you through diverse terrain - from thick forests to open grasslands, offering glimpses of exotic flora and fauna along the way."""

# --- Package Information ---
package_info = {
    "Standard": {
        "price": "₹24,999",
        "duration": "7 Days / 6 Nights",
        "rating": 4.2,
        "ideal_for": "Couples, small groups, and nature enthusiasts",
        "includes": [
            "Accommodation (3-star hotels and resorts)",
            "Daily breakfast and dinner",
            "All transportation within Karnataka",
            "Guided tours at all locations",
            "All entry fees to attractions",
            "Experienced tour guide throughout",
        ],
        "highlights": "Perfect for travelers seeking an immersive experience of Karnataka's natural beauty and cultural heritage without breaking the bank.",
    },
    "Premium": {
        "price": "₹34,999",
        "duration": "7 Days / 6 Nights",
        "rating": 4.8,
        "ideal_for": "Families, luxury travelers, and photography enthusiasts",
        "includes": [
            "Luxury accommodation (4-5 star resorts)",
            "All meals included with special local cuisine experiences",
            "Private transportation in premium vehicles",
            "Guided tours at all locations with specialized local experts",
            "All entry fees to attractions with priority access",
            "Professional photography session at scenic spots",
            "Personalized itinerary customization",
            "Complimentary spa session in Udupi",
        ],
        "highlights": "The ultimate Karnataka experience with exclusive accommodations, personalized service, and unique experiences not available in the standard package.",
    },
}

# --- Testimonials ---
testimonials = [
    {
        "text": "Our trip to Karnataka with AST Travels was beyond expectations. The itinerary perfectly balanced nature, culture, and relaxation. Kudremukh was the highlight of our journey!",
        "author": "Ravi & Priya Sharma, Delhi",
    },
    {
        "text": "The attention to detail was impressive. From seamless transportation to knowledgeable guides, every aspect was well-planned. Will definitely book with AST again!",
        "author": "James Wilson, UK",
    },
    {
        "text": "As a solo female traveler, safety was my priority. The team ensured I felt secure throughout while experiencing the best of Karnataka. The Udupi temples were magnificent!",
        "author": "Ananya Desai, Mumbai",
    },
]


# --- Itinerary Function ---
def create_itinerary():
    itinerary = []
    for i in range(TOTAL_DAYS):
        current_date = START_DATE + timedelta(days=i)

        # Define locations and activities for each day
        if i == 0:  # Day 1
            location = "Kalasa"
            activity = "Arrival & Temple Visit"
        elif i == 1:  # Day 2
            location = "Kalasa"
            activity = "Hanging Bridge & Viewpoints"
        elif i == 2:  # Day 3
            location = "Kudremukh"
            activity = "National Park Exploration"
        elif i == 3:  # Day 4
            location = "Kudremukh"
            activity = "Lakya Dam & Waterfalls"
        elif i == 4:  # Day 5
            location = "Netravati"
            activity = "Peak Trek & Camping"
        elif i == 5:  # Day 6
            location = "Udupi"
            activity = "Temple Tour & Beach Visit"
        else:  # Day 7
            location = "Udupi"
            activity = "St. Mary's Island & Departure"

        itinerary.append(
            {"date": current_date, "location": location, "activity": activity}
        )

    return itinerary


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


# --- Custom Flowables ---
class DecorationFlowable(Flowable):
    """A flowable for adding decorative elements to the document."""

    def __init__(self, width, style="wave", color=PRIMARY_COLOR, height=0.25 * inch):
        Flowable.__init__(self)
        self.width = width
        self.style = style
        self.color = color
        self.height = height

    def draw(self):
        canvas = self.canv
        canvas.saveState()

        canvas.setStrokeColor(self.color)
        canvas.setLineWidth(1.5)

        if self.style == "wave":
            # Draw a wave pattern
            x, y = 0, self.height / 2
            amplitude = self.height / 2
            period = 0.2 * inch

            path = canvas.beginPath()
            path.moveTo(x, y)

            for i in range(int(self.width / period) + 1):
                x = i * period
                if i % 2 == 0:
                    path.lineTo(x, y + amplitude)
                else:
                    path.lineTo(x, y - amplitude)

            canvas.drawPath(path, stroke=1, fill=0)

        elif self.style == "zigzag":
            # Draw a zigzag pattern
            x, y = 0, self.height / 2
            amplitude = self.height / 2
            period = 0.15 * inch

            path = canvas.beginPath()
            path.moveTo(x, y)

            for i in range(int(self.width / period) + 1):
                x = i * period
                if i % 2 == 0:
                    path.lineTo(x, y + amplitude)
                else:
                    path.lineTo(x, y - amplitude)

            canvas.drawPath(path, stroke=1, fill=0)

        elif self.style == "dots":
            # Draw a dot pattern
            dot_radius = 1.5
            spacing = 0.15 * inch

            for i in range(int(self.width / spacing) + 1):
                x = i * spacing
                canvas.circle(x, self.height / 2, dot_radius, fill=1)

        elif self.style == "corners":
            # Draw corner decorations
            size = self.height * 2

            # Top-left corner
            path = canvas.beginPath()
            path.moveTo(0, size)
            path.lineTo(0, 0)
            path.lineTo(size, 0)
            canvas.drawPath(path, stroke=1, fill=0)

            # Top-right corner
            path = canvas.beginPath()
            path.moveTo(self.width, size)
            path.lineTo(self.width, 0)
            path.lineTo(self.width - size, 0)
            canvas.drawPath(path, stroke=1, fill=0)

            # Bottom-left corner
            path = canvas.beginPath()
            path.moveTo(0, self.height * 4 - size)
            path.lineTo(0, self.height * 4)
            path.lineTo(size, self.height * 4)
            canvas.drawPath(path, stroke=1, fill=0)

            # Bottom-right corner
            path = canvas.beginPath()
            path.moveTo(self.width, self.height * 4 - size)
            path.lineTo(self.width, self.height * 4)
            path.lineTo(self.width - size, self.height * 4)
            canvas.drawPath(path, stroke=1, fill=0)

        canvas.restoreState()

    def wrap(self, availWidth, availHeight):
        return (min(self.width, availWidth), self.height)


class Divider(Flowable):
    """A flowable to create horizontal dividers."""

    def __init__(self, width, style="solid", color=PRIMARY_COLOR):
        Flowable.__init__(self)
        self.width = width
        self.style = style
        self.color = color
        self.height = 0.1 * inch

    def draw(self):
        canvas = self.canv
        canvas.saveState()

        canvas.setStrokeColor(self.color)

        if self.style == "dashed":
            canvas.setDash([6, 3])
        elif self.style == "dotted":
            canvas.setDash([2, 2])
        elif self.style == "fancy":
            # Draw a fancy divider with a center element
            # Center line
            canvas.setLineWidth(1)
            canvas.line(0, self.height / 2, self.width, self.height / 2)

            # Center diamond
            center_x = self.width / 2
            diamond_size = 0.15 * inch
            canvas.setFillColor(self.color)
            canvas.setStrokeColor(self.color)

            path = canvas.beginPath()
            path.moveTo(center_x, self.height / 2 + diamond_size / 2)
            path.lineTo(center_x + diamond_size / 2, self.height / 2)
            path.lineTo(center_x, self.height / 2 - diamond_size / 2)
            path.lineTo(center_x - diamond_size / 2, self.height / 2)
            path.close()
            canvas.drawPath(path, stroke=1, fill=1)

            # Tiny dots on each side
            dot_space = 0.4 * inch
            dot_radius = 2

            for x in [center_x - dot_space, center_x + dot_space]:
                canvas.circle(x, self.height / 2, dot_radius, fill=1)

            canvas.restoreState()
            return

        # Draw the line
        canvas.setLineWidth(1)
        canvas.line(0, self.height / 2, self.width, self.height / 2)

        canvas.restoreState()

    def wrap(self, availWidth, availHeight):
        return (min(self.width, availWidth), self.height)


class RoundedBox(Flowable):
    """A flowable that creates a rounded box around another flowable."""

    def __init__(
        self,
        flowable,
        width=None,
        height=None,
        backgroundColor=None,
        borderColor=None,
        radius=5,
        padding=5,
        shadowColor=None,
        shadowOffset=3,
    ):
        Flowable.__init__(self)
        self.flowable = flowable
        self.backgroundColor = backgroundColor
        self.borderColor = borderColor
        self.radius = radius
        self.padding = padding
        self.shadowColor = shadowColor
        self.shadowOffset = shadowOffset

        # Wrap the inner flowable to determine size if not specified
        if width is None or height is None:
            # Use a large value to find the natural size
            if isinstance(flowable, Paragraph):
                max_width = 500  # A reasonable maximum
                w, h = flowable.wrap(max_width, 10000)

                if width is None:
                    width = w + 2 * padding
                if height is None:
                    height = h + 2 * padding
            else:
                # For other flowables, try to determine size
                try:
                    if width is None:
                        width = flowable.width + 2 * padding
                    if height is None:
                        height = flowable.height + 2 * padding
                except AttributeError:
                    # Default sizes if we can't determine
                    if width is None:
                        width = 100
                    if height is None:
                        height = 20

        self.width = width
        self.height = height

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
                fill=1,
                stroke=0,
            )

        # Draw background
        if self.backgroundColor:
            canvas.setFillColor(self.backgroundColor)
            canvas.roundRect(
                0, 0, self.width, self.height, self.radius, fill=1, stroke=0
            )

        # Draw border
        if self.borderColor:
            canvas.setStrokeColor(self.borderColor)
            canvas.roundRect(
                0, 0, self.width, self.height, self.radius, fill=0, stroke=1
            )

        # Draw the contained flowable
        canvas.translate(self.padding, self.padding)
        self.flowable.drawOn(canvas, 0, 0)

        canvas.restoreState()

    def wrap(self, availWidth, availHeight):
        # Allow the box to be constrained by available space
        return (min(self.width, availWidth), min(self.height, availHeight))


class PlaceholderImage(Flowable):
    """A flowable that creates a placeholder for an image."""

    def __init__(self, width, height, bgColor=PALE_BLUE, text=None):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.bgColor = bgColor
        self.text = text if text else "Map Preview"

    def draw(self):
        canvas = self.canv
        canvas.saveState()

        # Draw background
        canvas.setFillColor(self.bgColor)
        canvas.rect(0, 0, self.width, self.height, fill=1, stroke=0)

        # Draw border
        canvas.setStrokeColor(PRIMARY_COLOR)
        canvas.setLineWidth(1)
        canvas.rect(0, 0, self.width, self.height, fill=0, stroke=1)

        # Draw diagonal lines
        canvas.setLineWidth(0.5)
        canvas.line(0, 0, self.width, self.height)
        canvas.line(0, self.height, self.width, 0)

        # Draw text
        canvas.setFont("Helvetica", 14)
        canvas.setFillColor(TEXT_COLOR)
        canvas.drawCentredString(self.width / 2, self.height / 2, self.text)

        canvas.restoreState()

    def wrap(self, availWidth, availHeight):
        return (self.width, self.height)


class TimelineFlowable(Flowable):
    """A flowable for displaying a timeline of events."""

    def __init__(self, events, width, height=None):
        Flowable.__init__(self)
        self.events = events
        self.width = width
        self.height = height or 2.5 * inch

    def draw(self):
        canvas = self.canv
        canvas.saveState()

        # Parameters
        timeline_y = self.height / 2
        circle_radius = 6
        spacing = self.width / (len(self.events) + 1)

        # Draw the horizontal line
        canvas.setStrokeColor(PRIMARY_COLOR)
        canvas.setLineWidth(2)
        canvas.line(0, timeline_y, self.width, timeline_y)

        # Draw events
        for i, event in enumerate(self.events):
            x_pos = spacing * (i + 1)

            # Alternate display above/below the timeline
            if i % 2 == 0:
                text_y = timeline_y + 15
                line_end = timeline_y + circle_radius + 10
                date_y = timeline_y - 25
            else:
                text_y = timeline_y - 35
                line_end = timeline_y - circle_radius - 10
                date_y = timeline_y + 15

            # Draw connecting line
            canvas.setLineWidth(1)
            canvas.line(x_pos, timeline_y, x_pos, line_end)

            # Draw circle marker
            canvas.setFillColor(SECONDARY_COLOR)
            canvas.setStrokeColor(PRIMARY_COLOR)
            canvas.setLineWidth(1)
            canvas.circle(x_pos, timeline_y, circle_radius, stroke=1, fill=1)

            # Format and draw date
            date_str = event["date"].strftime("%b %d")
            canvas.setFont("Helvetica-Bold", 8)
            canvas.setFillColor(ACCENT_COLOR)
            canvas.drawCentredString(x_pos, date_y, date_str)

            # Draw location
            canvas.setFont("Helvetica-Bold", 10)
            canvas.setFillColor(TEXT_COLOR)
            canvas.drawCentredString(x_pos, text_y, event["location"])

            # Draw activity
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(LIGHT_TEXT_COLOR)
            canvas.drawCentredString(x_pos, text_y - 12, event["activity"])

        canvas.restoreState()

    def wrap(self, availWidth, availHeight):
        return (min(self.width, availWidth), self.height)


class StarRating(Flowable):
    """A flowable for displaying a star rating."""

    def __init__(self, rating, width=1.5 * inch, height=0.25 * inch):
        Flowable.__init__(self)
        self.rating = min(5, max(0, rating))  # Ensure between 0 and 5
        self.width = width
        self.height = height

    def draw(self):
        canvas = self.canv
        canvas.saveState()

        # Parameters
        star_size = self.height * 0.8
        spacing = star_size * 1.2
        total_width = spacing * 5
        start_x = (self.width - total_width) / 2

        # Draw stars
        for i in range(5):
            x_center = start_x + i * spacing + star_size / 2
            y_center = self.height / 2

            # Determine if star is filled, half-filled, or empty
            full_stars = int(self.rating)
            remainder = self.rating - full_stars

            if i < full_stars:
                self._drawStar(canvas, x_center, y_center, star_size, SECONDARY_COLOR)
            elif i == full_stars and remainder > 0:
                # Draw half star
                self._drawStar(canvas, x_center, y_center, star_size, LIGHT_TEXT_COLOR)
                self._drawHalfStar(
                    canvas, x_center, y_center, star_size, SECONDARY_COLOR
                )
            else:
                self._drawStar(canvas, x_center, y_center, star_size, LIGHT_TEXT_COLOR)

        # Draw the rating number
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(TEXT_COLOR)
        canvas.drawRightString(self.width, self.height * 0.7, f"{self.rating}/5.0")

        canvas.restoreState()

    def _drawStar(self, canvas, x_center, y_center, size, color):
        """Helper method to draw a 5-pointed star."""
        canvas.setFillColor(color)
        canvas.setStrokeColor(color)

        # Calculate points of a 5-pointed star
        points = []
        for i in range(10):
            # Alternating radius for points and inward angles
            radius = size / 2 if i % 2 == 0 else size / 5
            angle = math.pi / 2 + i * 2 * math.pi / 10

            x = x_center + radius * math.cos(angle)
            y = y_center + radius * math.sin(angle)
            points.append((x, y))

        # Draw the star
        path = canvas.beginPath()
        path.moveTo(points[0][0], points[0][1])
        for x, y in points[1:]:
            path.lineTo(x, y)
        path.close()
        canvas.drawPath(path, stroke=0, fill=1)

    def _drawHalfStar(self, canvas, x_center, y_center, size, color):
        """Helper method to draw half of a 5-pointed star."""
        canvas.setFillColor(color)

        # Create a clipping rectangle for the left half of the star
        canvas.saveState()
        canvas.rect(
            x_center - size / 2, y_center - size / 2, size / 2, size, stroke=0, fill=0
        )
        canvas.clipPath()

        # Draw the full star which will be clipped
        self._drawStar(canvas, x_center, y_center, size, color)

        canvas.restoreState()

    def wrap(self, availWidth, availHeight):
        return (min(self.width, availWidth), self.height)


def get_image_from_url(url, width=None, height=None):
    """Fetch an image from URL and return a ReportLab Image object."""
    try:
        import requests
        from io import BytesIO

        # Fetch the image with a proper user agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, stream=True, timeout=10, headers=headers)
        response.raise_for_status()

        # Use BytesIO to create a file-like object from the response content
        img_data = BytesIO(response.content)

        # Create a placeholder image in case of error
        if width is None:
            width = 2 * inch
        if height is None:
            height = 1.5 * inch

        # Create the image and set dimensions
        img = Image(img_data, width=width, height=height)

        return img

    except Exception as e:
        print(f"Error loading image from {url}: {e}")

        # Create a placeholder instead
        placeholder = PlaceholderImage(
            width if width is not None else 2 * inch,
            height if height is not None else 1.5 * inch,
            text="Image unavailable",
        )
        return placeholder


# --- Define styles ---
# Add these styles if they don't exist in the styles dictionary
styles = getSampleStyleSheet()

if "SectionTitle" not in styles:
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=PRIMARY_COLOR,
            spaceAfter=0.1 * inch,
            spaceBefore=0.2 * inch,
            alignment=TA_LEFT,
        )
    )

if "SubSectionTitle" not in styles:
    styles.add(
        ParagraphStyle(
            name="SubSectionTitle",
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=PRIMARY_COLOR,
            spaceAfter=0.1 * inch,
            alignment=TA_LEFT,
        )
    )

if "CoverTitle" not in styles:
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="Helvetica-Bold",
            fontSize=40,
            leading=44,
            textColor=white,
            alignment=TA_CENTER,
            spaceAfter=0.3 * inch,
        )
    )

if "CoverSubtitle" not in styles:
    styles.add(
        ParagraphStyle(
            name="CoverSubtitle",
            fontName="Helvetica",
            fontSize=24,
            leading=28,
            textColor=white,
            alignment=TA_CENTER,
            italic=1,
        )
    )

if "MainTitle" not in styles:
    styles.add(
        ParagraphStyle(
            name="MainTitle",
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=PRIMARY_COLOR,
            alignment=TA_CENTER,
            spaceAfter=0.2 * inch,
        )
    )

if "TOC" not in styles:
    styles.add(
        ParagraphStyle(
            name="TOC",
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=PRIMARY_COLOR,
            alignment=TA_LEFT,
        )
    )

if "TOCEntry1" not in styles:
    styles.add(
        ParagraphStyle(
            name="TOCEntry1",
            fontName="Helvetica",
            fontSize=11,
            textColor=TEXT_COLOR,
            alignment=TA_LEFT,
        )
    )

if "TOCEntry2" not in styles:
    styles.add(
        ParagraphStyle(
            name="TOCEntry2",
            fontName="Helvetica",
            fontSize=10,
            textColor=TEXT_COLOR,
            alignment=TA_LEFT,
        )
    )

if "CaptionText" not in styles:
    styles.add(
        ParagraphStyle(
            name="CaptionText",
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=LIGHT_TEXT_COLOR,
            alignment=TA_CENTER,
        )
    )

if "SideNote" not in styles:
    styles.add(
        ParagraphStyle(
            name="SideNote",
            fontName="Helvetica",
            fontSize=9,
            leading=11,
            textColor=ACCENT_COLOR,
            alignment=TA_LEFT,
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

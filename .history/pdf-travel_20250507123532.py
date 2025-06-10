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
from math import sin, cos, radians
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

# --- Colors ---
PRIMARY_COLOR = HexColor("#005A9C")  # A professional blue
ACCENT_COLOR = HexColor("#4CAF50")  # A nature green
TEXT_COLOR = HexColor("#333333")
LIGHT_TEXT_COLOR = HexColor("#555555")
BACKGROUND_COLOR = white
TIMELINE_COLOR = HexColor("#FF7F50")  # Coral color for timeline
SECONDARY_COLOR = HexColor("#F9A826")  # Warm yellow/orange

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


# --- Create a company logo ---
def create_logo():
    logo_io = BytesIO()
    c = canvas.Canvas(logo_io, pagesize=(200, 100))

    # Draw circle background
    c.setFillColor(PRIMARY_COLOR)
    c.circle(50, 50, 40, fill=1)

    # Draw text
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(50, 55, "AST")
    c.setFont("Helvetica", 12)
    c.drawCentredString(50, 35, "TRAVELS")

    # Draw stylized airplane
    c.setStrokeColor(white)
    c.setLineWidth(2)
    c.line(70, 50, 110, 60)  # Wing
    c.line(90, 50, 130, 50)  # Body
    c.line(90, 50, 110, 40)  # Tail

    c.save()
    return BytesIO(logo_io.getvalue())


# --- Custom Flowables ---
class TimelineFlowable(Flowable):
    def __init__(self, days, width=500):
        Flowable.__init__(self)
        self.days = days
        self.width = width
        self.height = 120

    def draw(self):
        canvas = self.canv
        canvas.saveState()

        # Draw timeline line
        canvas.setStrokeColor(TIMELINE_COLOR)
        canvas.setLineWidth(3)
        start_x = 50
        end_x = self.width - 50
        y = self.height / 2
        canvas.line(start_x, y, end_x, y)

        # Draw days
        segment_width = (end_x - start_x) / (len(self.days) - 1)
        for i, day_info in enumerate(self.days):
            x = start_x + i * segment_width

            # Draw circle
            canvas.setFillColor(TIMELINE_COLOR)
            canvas.circle(x, y, 8, stroke=0, fill=1)

            # Draw text
            canvas.setFillColor(TEXT_COLOR)
            canvas.setFont("Helvetica-Bold", 9)
            day_txt = f"Day {i+1}"
            canvas.drawCentredString(x, y - 20, day_txt)

            # Draw date
            date_str = day_info["date"].strftime("%b %d")
            canvas.setFont("Helvetica", 8)
            canvas.drawCentredString(x, y - 35, date_str)

            # Draw location
            canvas.setFont("Helvetica", 8)
            canvas.drawCentredString(x, y + 25, day_info["location"])

            # Draw activity (rotated if needed)
            activity = day_info["activity"]
            if len(activity) > 15:
                activity = textwrap.fill(activity, width=15)

            # Draw activity text (above the circle)
            canvas.setFont("Helvetica-Oblique", 7)
            for j, line in enumerate(activity.split("\n")):
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

    def draw(self):
        canvas = self.canv
        canvas.saveState()

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
    def __init__(self, width, color=lightgrey, thickness=1, spacer=0.1 * inch):
        Flowable.__init__(self)
        self.width = width
        self.color = color
        self.thickness = thickness
        self.spacer = spacer
        self.height = 2 * self.spacer + self.thickness

    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.spacer, self.width, self.spacer)
        self.canv.restoreState()


# --- Styles ---
styles = getSampleStyleSheet()

# Modify the existing BodyText style
styles["BodyText"].fontName = "Helvetica"
styles["BodyText"].fontSize = 10
styles["BodyText"].leading = 14
styles["BodyText"].textColor = TEXT_COLOR
styles["BodyText"].alignment = TA_JUSTIFY
styles["BodyText"].spaceAfter = 0.1 * inch

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
styles.add(
    ParagraphStyle(
        name="SectionTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=ACCENT_COLOR,
        spaceBefore=0.3 * inch,
        spaceAfter=0.1 * inch,
    )
)
styles.add(
    ParagraphStyle(
        name="CaptionText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=LIGHT_TEXT_COLOR,
        alignment=TA_CENTER,
        spaceAfter=0.1 * inch,
        italic=1,  # Use italic property instead of Helvetica-Italic
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
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=TEXT_COLOR,
        spaceAfter=0.05 * inch,
        alignment=TA_LEFT,
    )
)

# Adding more professional styles
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=36,
        leading=40,
        textColor=white,
        alignment=TA_CENTER,
        spaceAfter=0.2 * inch,
    )
)

styles.add(
    ParagraphStyle(
        name="CoverSubtitle",
        fontName="Helvetica",  # Changed from Helvetica-Italic
        fontSize=18,
        leading=22,
        textColor=white,
        alignment=TA_CENTER,
        spaceAfter=0.4 * inch,
        italic=1,  # Use italic property instead
    )
)

styles.add(
    ParagraphStyle(
        name="PackageTitle",
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=PRIMARY_COLOR,
        alignment=TA_LEFT,
        spaceBefore=0.2 * inch,
    )
)

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

styles.add(
    ParagraphStyle(
        name="SidebarTitle",
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=16,
        textColor=white,
        alignment=TA_CENTER,
        spaceBefore=0.1 * inch,
        spaceAfter=0.1 * inch,
    )
)

styles.add(
    ParagraphStyle(
        name="TestimonialText",
        fontName="Helvetica",  # Changed from Helvetica-Italic
        fontSize=9,
        leading=12,
        textColor=TEXT_COLOR,
        alignment=TA_LEFT,
        firstLineIndent=10,
        spaceAfter=0.05 * inch,
        italic=1,  # Use italic property instead
    )
)

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


# --- Helper to get image from URL ---
def get_image_from_url(url, width=2 * inch):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        img_file = BytesIO(response.content)
        img = Image(
            img_file, width=width, height=width
        )  # Initial height, will be adjusted
        img.drawHeight = (
            width * img.imageHeight / img.imageWidth
        )  # Maintain aspect ratio
        img.drawWidth = width
        return img
    except Exception as e:
        print(f"Warning: Could not fetch image from {url}. Error: {e}")
        return Paragraph(
            f"[Image: {url.split('/')[-1]} not available]", styles["CaptionText"]
        )


# --- Header and Footer with custom logo ---
def header_footer(canvas, doc):
    canvas.saveState()

    # Get logo
    try:
        logo_data = create_logo()
        logo = Image(logo_data, width=0.8 * inch, height=0.4 * inch)
        logo.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 0.5 * inch)
    except Exception as e:
        print(f"Error with logo: {e}")
        # Fallback to text if logo fails
        canvas.setFont("Helvetica-Bold", 14)
        canvas.setFillColor(PRIMARY_COLOR)
        canvas.drawString(
            doc.leftMargin, doc.height + doc.topMargin - 0.4 * inch, COMPANY_NAME
        )

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


# Custom first page
def cover_page(canvas, doc):
    canvas.saveState()

    # Background image for cover
    try:
        cover_img_data = requests.get(
            IMAGES["cover_image"], stream=True, timeout=10
        ).content
        cover_img_io = BytesIO(cover_img_data)
        canvas.drawImage(
            cover_img_io,
            0,
            0,
            width=A4[0],
            height=A4[1],
            preserveAspectRatio=False,
            mask="auto",
        )

        # Semi-transparent overlay
        canvas.setFillColorRGB(0, 0, 0, 0.6)  # Black with 60% opacity
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    except Exception as e:
        print(f"Error with cover image: {e}")
        # Fallback to solid color if image fails
        canvas.setFillColor(PRIMARY_COLOR)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)

    # No headers and footers on cover page

    canvas.restoreState()


# --- Content Descriptions ---
kalasa_desc = """
Escape to Kalasa, a haven of spiritual charm nestled amidst Karnataka's lush Western Ghats.
Experience profound riverfront serenity along the banks of the Bhadra, feel the sacred vibes
emanating from ancient temples, and seek a touch of adventure on the iconic Kalasa Hanging Bridge.
The breathtaking Ambaa Teertha Viewpoint offers panoramic vistas, making Kalasa a perfect blend of
peace and picturesque beauty.
"""

udupi_desc = """
Discover Udupi, a vibrant coastal gem renowned for its stunning beaches, rich temple heritage,
and delectable local cuisine. Home to the famous Sri Krishna Matha, Udupi offers a unique
spiritual experience, while its sun-kissed shores invite relaxation. Don't miss the chance
to savor authentic Udupi dishes, a culinary delight known worldwide.
"""

kudremukh_desc = """
Immerse yourself in the raw beauty of Kudremukh, the 'horse-face' range, characterized by its
rolling grasslands, dense shola forests, and diverse wildlife. Explore the Kudremukh National Park,
a hotspot for eco-tourism and trekking, and be mesmerized by the stunning vistas from the Lakya Dam
Viewpoint, a testament to nature's grandeur and serene water bodies.
"""

netravati_desc = """
Embark on an unforgettable adventure to Netravati Peak, a perfect trekking destination for
nature lovers and thrill-seekers alike. Witness awe-inspiring sunrise views painting the sky,
traverse through verdant green valleys, and keep an eye out for diverse birdlife. The
challenging yet rewarding climb offers unparalleled panoramic beauty.
"""

# --- Package information ---
package_info = {
    "Standard": {
        "price": "₹25,999",
        "duration": "7 Days / 6 Nights",
        "includes": [
            "Accommodation in 3-star hotels",
            "Daily breakfast & dinner",
            "AC vehicle for transportation",
            "Experienced guide for all treks",
            "All entrance fees to parks & monuments",
        ],
    },
    "Premium": {
        "price": "₹39,999",
        "duration": "7 Days / 6 Nights",
        "includes": [
            "Luxury accommodation in 4-5 star hotels",
            "All meals included with specialty dining",
            "Premium AC vehicle with personal driver",
            "Private guides for treks and sightseeing",
            "Photography sessions at scenic spots",
            "Complimentary welcome gift",
        ],
    },
}

# --- Testimonials ---
testimonials = [
    {
        "text": "The Karnataka tour organized by AST Travels exceeded our expectations. The itinerary was perfectly balanced between adventure and relaxation.",
        "author": "Priya & Rahul Sharma, Delhi",
    },
    {
        "text": "Our guide was incredibly knowledgeable and made our Kudremukh trek both safe and enjoyable. Will definitely book with AST again!",
        "author": "Rajesh Patel, Mumbai",
    },
    {
        "text": "From the beaches of Udupi to the peaks of Netravati, every moment was magical and beautifully organized.",
        "author": "Meera Krishnan, Bangalore",
    },
]


# --- Daily Itinerary ---
def create_itinerary():
    itinerary = []
    for i in range(TOTAL_DAYS):
        date = START_DATE + timedelta(days=i)
        day = {"date": date}

        if i == 0:
            day["location"] = "Bangalore → Kalasa"
            day["activity"] = "Arrival & Transfer"
        elif i == 1:
            day["location"] = "Kalasa"
            day["activity"] = "Temple Tour"
        elif i == 2:
            day["location"] = "Kalasa"
            day["activity"] = "Hanging Bridge"
        elif i == 3:
            day["location"] = "Kalasa → Udupi"
            day["activity"] = "Travel & Beach"
        elif i == 4:
            day["location"] = "Udupi"
            day["activity"] = "Temple Visit"
        elif i == 5:
            day["location"] = "Kudremukh"
            day["activity"] = "National Park Trek"
        else:
            day["location"] = "Netravati Peak"
            day["activity"] = "Peak Trek"

        itinerary.append(day)
    return itinerary


# --- Build PDF ---
def build_pdf():
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

    content_template = PageTemplate(
        id="content",
        frames=[
            Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
        ],
        onPage=header_footer,
    )

    doc.addPageTemplates([cover_template, content_template])

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
            fontSize=24,
            textColor=SECONDARY_COLOR,
            italic=0,  # Override parent's italic setting
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
                fontSize=16,
            ),
        )
    )

    story.append(PageBreak())

    # --- Content Pages ---
    story.append(NextPageTemplate("content"))

    # Welcome message
    welcome_box = RoundedBox(
        Paragraph(
            f"Welcome to your exclusive Karnataka adventure with {COMPANY_NAME}! "
            f"This brochure outlines your upcoming journey through some of the most "
            f"breathtaking locations in Karnataka. Get ready to explore ancient temples, "
            f"pristine beaches, lush forests, and majestic peaks.",
            styles["BodyText"],
        ),
        width=doc.width,
        height=1.2 * inch,
        backgroundColor=HexColor("#F0F7FF"),
        borderColor=PRIMARY_COLOR,
        padding=15,
    )
    story.append(welcome_box)
    story.append(Spacer(1, 0.3 * inch))

    # Itinerary Timeline
    story.append(Paragraph("Your 7-Day Journey", styles["SectionTitle"]))
    story.append(Spacer(1, 0.1 * inch))
    story.append(TimelineFlowable(create_itinerary(), width=doc.width))
    story.append(Spacer(1, 0.3 * inch))

    # Map of the journey
    try:
        map_img = get_image_from_url(IMAGES["map_image"], width=4 * inch)
        map_table = Table(
            [
                [Paragraph("Your Journey Through Karnataka", styles["SectionTitle"])],
                [map_img],
                [
                    Paragraph(
                        "<i>Explore Karnataka's most scenic locations</i>",
                        styles["CaptionText"],
                    )
                ],
            ],
            colWidths=[doc.width],
        )
        map_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0.1 * inch),
                ]
            )
        )
        story.append(map_table)
    except Exception as e:
        print(f"Error with map: {e}")

    story.append(Spacer(1, 0.3 * inch))
    story.append(Divider(width=doc.width))
    story.append(Spacer(1, 0.3 * inch))

    # --- Kalasa ---
    story.append(
        Paragraph("Kalasa: Spiritual Charm & Lush Landscapes", styles["SectionTitle"])
    )

    img_kalasa_bridge = get_image_from_url(IMAGES["kalasa_bridge"], width=2.2 * inch)
    img_kalasa_viewpoint = get_image_from_url(
        IMAGES["kalasa_viewpoint"], width=2.2 * inch
    )

    kalasa_content = [
        [img_kalasa_bridge, Paragraph(kalasa_desc, styles["BodyText"])],
        [
            Paragraph(
                "<i>Kalasa Hanging Bridge: A walk to remember</i>",
                styles["CaptionText"],
            ),
            "",
        ],  # Caption for first image
        [
            img_kalasa_viewpoint,
            Paragraph(
                "Ambaa Teertha offers stunning panoramic views of the river and surrounding greenery.",
                styles["BodyText"],
            ),
        ],
        [
            Paragraph(
                "<i>Ambaa Teertha Viewpoint: Nature's Vista</i>", styles["CaptionText"]
            ),
            "",
        ],  # Caption for second image
    ]
    kalasa_table = Table(
        kalasa_content, colWidths=[2.5 * inch, doc.width - 2.5 * inch - 0.2 * inch]
    )  # Adjusted width for text
    kalasa_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (1, 0), (1, -1), 0.2 * inch),  # Padding for text column
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0.1 * inch),
                ("BACKGROUND", (0, 0), (0, 0), HexColor("#F8F8F8")),
                ("BACKGROUND", (0, 2), (0, 2), HexColor("#F8F8F8")),
            ]
        )
    )
    story.append(kalasa_table)
    story.append(Spacer(1, 0.3 * inch))
    story.append(Divider(width=doc.width))
    story.append(Spacer(1, 0.3 * inch))

    # --- Udupi with improved layout ---
    story.append(
        Paragraph("Udupi: Coastal Beauty & Temple Heritage", styles["SectionTitle"])
    )

    # Get Udupi images
    img_udupi_beach = get_image_from_url(IMAGES["udupi_beach"], width=2.2 * inch)
    img_udupi_temple = get_image_from_url(IMAGES["udupi_temple"], width=2.2 * inch)

    # Create a more attractive layout for Udupi
    udupi_content = [
        [Paragraph(udupi_desc, styles["BodyText"]), img_udupi_beach],
        ["", Paragraph("<i>Serene beaches of Udupi</i>", styles["CaptionText"])],
        [
            img_udupi_temple,
            Paragraph(
                "The historic Sri Krishna Temple is an architectural marvel and spiritual center attracting devotees from across the country.",
                styles["BodyText"],
            ),
        ],
        [
            Paragraph("<i>Sri Krishna Matha: Spiritual Hub</i>", styles["CaptionText"]),
            "",
        ],
    ]

    udupi_table = Table(
        udupi_content, colWidths=[doc.width - 2.5 * inch - 0.2 * inch, 2.5 * inch]
    )
    udupi_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("RIGHTPADDING", (0, 0), (0, -1), 0.2 * inch),
                ("LEFTPADDING", (1, 2), (1, 2), 0.2 * inch),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0.1 * inch),
                ("BACKGROUND", (1, 0), (1, 0), HexColor("#F8F8F8")),
                ("BACKGROUND", (0, 2), (0, 2), HexColor("#F8F8F8")),
            ]
        )
    )
    story.append(udupi_table)
    story.append(Spacer(1, 0.3 * inch))
    story.append(Divider(width=doc.width))
    story.append(Spacer(1, 0.3 * inch))

    # --- Kudremukh ---
    story.append(
        Paragraph("Kudremukh: Rolling Grasslands & Wildlife", styles["SectionTitle"])
    )

    img_kudremukh_park = get_image_from_url(IMAGES["kudremukh_park"], width=2.2 * inch)
    img_kudremukh_dam = get_image_from_url(IMAGES["kudremukh_dam"], width=2.2 * inch)

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
        kudremukh_content, colWidths=[2.5 * inch, doc.width - 2.5 * inch - 0.2 * inch]
    )
    kudremukh_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (1, 0), (1, -1), 0.2 * inch),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0.1 * inch),
                ("BACKGROUND", (0, 0), (0, 0), HexColor("#F8F8F8")),
                ("BACKGROUND", (0, 2), (0, 2), HexColor("#F8F8F8")),
            ]
        )
    )
    story.append(kudremukh_table)
    story.append(Spacer(1, 0.3 * inch))
    story.append(Divider(width=doc.width))
    story.append(Spacer(1, 0.3 * inch))

    # --- Netravati Peak ---
    story.append(
        Paragraph("Netravati Peak: Trekker's Paradise", styles["SectionTitle"])
    )
    img_netravati = get_image_from_url(IMAGES["netravati_peak"], width=2.2 * inch)

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
        netravati_content, colWidths=[2.5 * inch, doc.width - 2.5 * inch - 0.2 * inch]
    )
    netravati_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (1, 0), (1, -1), 0.2 * inch),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0.1 * inch),
                ("BACKGROUND", (0, 0), (0, 0), HexColor("#F8F8F8")),
            ]
        )
    )
    story.append(netravati_table)
    story.append(Spacer(1, 0.3 * inch))

    # --- Package Options ---
    story.append(PageBreak())

    story.append(Paragraph("Tour Packages", styles["MainTitle"]))
    story.append(Spacer(1, 0.2 * inch))

    # Standard Package
    story.append(Paragraph("Standard Package", styles["PackageTitle"]))
    story.append(
        Paragraph(
            f"<b>Price:</b> {package_info['Standard']['price']} per person",
            styles["PackageHighlight"],
        )
    )
    story.append(
        Paragraph(
            f"<b>Duration:</b> {package_info['Standard']['duration']}",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("<b>Inclusions:</b>", styles["BodyText"]))

    for item in package_info["Standard"]["includes"]:
        story.append(Paragraph(f"• {item}", styles["BodyText"]))

    story.append(Spacer(1, 0.2 * inch))

    # Premium Package
    story.append(Paragraph("Premium Package", styles["PackageTitle"]))
    story.append(
        Paragraph(
            f"<b>Price:</b> {package_info['Premium']['price']} per person",
            styles["PackageHighlight"],
        )
    )
    story.append(
        Paragraph(
            f"<b>Duration:</b> {package_info['Premium']['duration']}",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("<b>Inclusions:</b>", styles["BodyText"]))

    for item in package_info["Premium"]["includes"]:
        story.append(Paragraph(f"• {item}", styles["BodyText"]))

    story.append(Spacer(1, 0.3 * inch))

    # --- Testimonials ---
    story.append(Paragraph("What Our Clients Say", styles["SectionTitle"]))
    story.append(Spacer(1, 0.1 * inch))

    # Create testimonial boxes
    testimonial_data = []
    for i, testimonial in enumerate(testimonials):
        testimonial_box = RoundedBox(
            contents=Paragraph(
                f'"{testimonial["text"]}"<br/><br/><i>- {testimonial["author"]}</i>',
                styles["TestimonialText"],
            ),
            width=(doc.width - 0.4 * inch) / 3,
            height=2 * inch,
            radius=10,
            backgroundColor=HexColor("#F8F8F8"),
            borderColor=lightgrey,
            padding=10,
        )

        testimonial_data.append(testimonial_box)

    # Create a row of testimonials
    testimonials_table = Table(
        [testimonial_data],
        colWidths=[(doc.width - 0.4 * inch) / 3] * 3,
        rowHeights=[2.2 * inch],
    )
    testimonials_table.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0.1 * inch),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0.1 * inch),
            ]
        )
    )
    story.append(testimonials_table)

    story.append(Spacer(1, 0.3 * inch))

    # --- Contact Information ---
    story.append(PageBreak())  # Ensure contact info is on a new page or has space
    story.append(Paragraph("Contact Information", styles["ContactTitle"]))
    story.append(Paragraph(f"For Bookings & Enquiries:", styles["BodyText"]))
    story.append(Spacer(1, 0.1 * inch))

    # Create a more attractive contact information section
    contact_data = [
        [
            Paragraph("<b>Phone:</b>", styles["ContactInfo"]),
            Paragraph(PHONE, styles["ContactInfo"]),
        ],
        [
            Paragraph("<b>Email:</b>", styles["ContactInfo"]),
            Paragraph(EMAIL, styles["ContactInfo"]),
        ],
        [
            Paragraph("<b>Website:</b>", styles["ContactInfo"]),
            Paragraph(WEBSITE, styles["ContactInfo"]),
        ],
    ]

    # Add social media
    for platform, handle in SOCIAL_MEDIA.items():
        contact_data.append(
            [
                Paragraph(f"<b>{platform}:</b>", styles["ContactInfo"]),
                Paragraph(handle, styles["ContactInfo"]),
            ]
        )

    contact_table = Table(contact_data, colWidths=[1 * inch, 3 * inch])
    contact_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(contact_table)
    story.append(Spacer(1, 0.2 * inch))

    # Final message
    story.append(
        Paragraph(
            "We look forward to helping you plan your unforgettable journey through Karnataka!",
            styles["BodyText"],
        )
    )

    # Booking call to action
    story.append(Spacer(1, 0.3 * inch))
    cta_box = RoundedBox(
        Paragraph(
            "<b>Ready to book your adventure?</b><br/>"
            "Contact us today to secure your spot on this incredible journey. "
            "Early bookings receive special discounts!",
            ParagraphStyle(
                name="CTAText",
                parent=styles["BodyText"],
                alignment=TA_CENTER,
            ),
        ),
        width=doc.width,
        height=1 * inch,
        radius=10,
        backgroundColor=ACCENT_COLOR,
        padding=10,
    )
    story.append(cta_box)

    # Build the PDF
    try:
        doc.build(story)
        print(f"PDF '{FILENAME}' generated successfully.")
    except Exception as e:
        print(f"Error building PDF: {e}")


if __name__ == "__main__":
    build_pdf()

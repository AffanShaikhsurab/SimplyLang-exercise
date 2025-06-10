import requests
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white, lightgrey, dimgrey
from reportlab.lib.pagesizes import A4

# --- Configuration ---
FILENAME = "AST_Travels_Karnataka_Itinerary.pdf"
COMPANY_NAME = "AST Travels"
WEBSITE = "www.asttravels.com"
PHONE = "7349733197"
EMAIL = "asttravels@gmail.com"

# --- Colors ---
PRIMARY_COLOR = HexColor("#005A9C")  # A professional blue
ACCENT_COLOR = HexColor("#4CAF50")   # A nature green
TEXT_COLOR = HexColor("#333333")
LIGHT_TEXT_COLOR = HexColor("#555555")
BACKGROUND_COLOR = white

# --- Image URLs ---
IMAGES = {
    "kalasa_bridge": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nofQkh6Fz5h9qZlIKbnryUY2qDuUH0MPumrUaUwnn-lY6dz5k2Nu6IOqmu5ClaBGcHBGfIycb4YA238jFJK8-pT4GFnkyeDYjAqeQejIwB8PRtH7kWR5Dic5btbhIPQ3lqSrNt2JoHm9Cvo=w203-h360-k-no",
    "kalasa_viewpoint": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4noJwwWj1yY59woeFLDI_TeA_t2qatVugfxnSm4elwUNBSGmia0gdKE0vEV8EGRFW3lLXzngQbzScwbehW8rXcDiAzSQwAPZ3SdC8HSm0qFKUDmWMNLh1xmLgLG5NsvB6Aw67k88Rvf2gQDj=w224-h398-k-no",
    "kudremukh_park": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nr3LqVNtgrlNZj3-A6eBKSXILoZGiwNNuNxd9MTIVo2PNKCuI8OmJg51Ubt6M0LEvS7UApHSzbEGwLKvI0lZxtP5k2lxb0zWnzWnoywQQGgje-iPSJ5W5y3RM9XDf2vx_5KYw_x=w203-h152-k-no",
    "kudremukh_dam": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nqrtkd3S5UzB6TcbN5JkCceJueZH7xtT3xSoduLZbmmhq7SPKLrPeKXxCpE2EwS2LJkAa-OgktuBlJQkSv8n_Nwg19i-ZriTfvWy478wpazpiCOaxu9a8g5SeUHTwzuth2hGz2f=w224-h298-k-no",
    "netravati_peak": "https://lh3.googleusercontent.com/gps-cs-s/AC9h4nqy-eYjX0oMSA4cqybR484N9_gjeitYett4pct2UcDtL7-HzSo__GuB4I9Muvl1Ygjngvp7AdRXtelcq0RxLdvD5toNkhWSlT0i_lS1_2vS7SQdDvUYAOBdfaVzol4Sq8UYHjOQr5Kzcao=w224-h398-k-no"
}

# --- Styles ---
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='MainTitle',
                          fontName='Helvetica-Bold',
                          fontSize=24,
                          leading=28,
                          textColor=PRIMARY_COLOR,
                          alignment=TA_CENTER,
                          spaceAfter=0.2*inch))
styles.add(ParagraphStyle(name='SectionTitle',
                          fontName='Helvetica-Bold',
                          fontSize=18,
                          leading=22,
                          textColor=ACCENT_COLOR,
                          spaceBefore=0.3*inch,
                          spaceAfter=0.1*inch))
styles.add(ParagraphStyle(name='BodyText',
                          parent=styles['Normal'],
                          fontName='Helvetica',
                          fontSize=10,
                          leading=14,
                          textColor=TEXT_COLOR,
                          alignment=TA_JUSTIFY,
                          spaceAfter=0.1*inch))
styles.add(ParagraphStyle(name='CaptionText',
                          parent=styles['Normal'],
                          fontName='Helvetica-Oblique',
                          fontSize=8,
                          leading=10,
                          textColor=LIGHT_TEXT_COLOR,
                          alignment=TA_CENTER,
                          spaceAfter=0.1*inch))
styles.add(ParagraphStyle(name='FooterText',
                          fontName='Helvetica',
                          fontSize=8,
                          textColor=dimgrey,
                          alignment=TA_CENTER))
styles.add(ParagraphStyle(name='ContactTitle',
                          fontName='Helvetica-Bold',
                          fontSize=14,
                          textColor=PRIMARY_COLOR,
                          spaceBefore=0.3*inch,
                          spaceAfter=0.1*inch,
                          alignment=TA_LEFT))
styles.add(ParagraphStyle(name='ContactInfo',
                          parent=styles['Normal'],
                          fontName='Helvetica',
                          fontSize=10,
                          leading=14,
                          textColor=TEXT_COLOR,
                          spaceAfter=0.05*inch,
                          alignment=TA_LEFT))

# --- Helper to get image from URL ---
def get_image_from_url(url, width=2*inch):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        img_file = BytesIO(response.content)
        img = Image(img_file, width=width, height=width) # Initial height, will be adjusted
        img.drawHeight = width * img.imageHeight / img.imageWidth # Maintain aspect ratio
        img.drawWidth = width
        return img
    except Exception as e:
        print(f"Warning: Could not fetch image from {url}. Error: {e}")
        return Paragraph(f"[Image: {url.split('/')[-1]} not available]", styles['CaptionText'])


# --- Header and Footer ---
def header_footer(canvas, doc):
    canvas.saveState()
    
    # Header
    logo_text = Paragraph(f"{COMPANY_NAME} [Logo]", ParagraphStyle(name='LogoPlaceholder', fontName='Helvetica-Bold', fontSize=14, textColor=PRIMARY_COLOR))
    w_logo, h_logo = logo_text.wrapOn(canvas, doc.width, doc.topMargin)
    logo_text.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h_logo - 0.1*inch)
    
    header_line_y = doc.height + doc.topMargin - h_logo - 0.15*inch
    canvas.setStrokeColor(lightgrey)
    canvas.line(doc.leftMargin, header_line_y, doc.leftMargin + doc.width, header_line_y)

    # Footer
    footer_text = Paragraph(f"{COMPANY_NAME} | {WEBSITE} | Page {doc.page}", styles['FooterText'])
    w_footer, h_footer = footer_text.wrapOn(canvas, doc.width, doc.bottomMargin)
    footer_text.drawOn(canvas, doc.leftMargin, h_footer - 0.1*inch) # Adjust y position
    
    footer_line_y = h_footer + 0.05*inch
    canvas.setStrokeColor(lightgrey)
    canvas.line(doc.leftMargin, footer_line_y, doc.leftMargin+doc.width, footer_line_y)
    
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

# --- Build PDF ---
def build_pdf():
    doc = SimpleDocTemplate(FILENAME,
                            pagesize=A4,
                            leftMargin=0.75*inch,
                            rightMargin=0.75*inch,
                            topMargin=1.2*inch, # Increased for header space
                            bottomMargin=0.8*inch) # Increased for footer space
    story = []

    # Main Title
    story.append(Paragraph("Your Scenic Getaway Awaits: Karnataka's Treasures", styles['MainTitle']))
    story.append(Spacer(1, 0.3*inch))

    # --- Kalasa ---
    story.append(Paragraph("Kalasa: Spiritual Charm & Lush Landscapes", styles['SectionTitle']))
    
    img_kalasa_bridge = get_image_from_url(IMAGES["kalasa_bridge"], width=2.2*inch)
    img_kalasa_viewpoint = get_image_from_url(IMAGES["kalasa_viewpoint"], width=2.2*inch)

    kalasa_content = [
        [img_kalasa_bridge, Paragraph(kalasa_desc, styles['BodyText'])],
        [Paragraph("<i>Kalasa Hanging Bridge: A walk to remember</i>", styles['CaptionText']), ''], # Caption for first image
        [img_kalasa_viewpoint, Paragraph("Ambaa Teertha offers stunning panoramic views of the river and surrounding greenery.", styles['BodyText'])],
        [Paragraph("<i>Ambaa Teertha Viewpoint: Nature's Vista</i>", styles['CaptionText']), ''] # Caption for second image
    ]
    kalasa_table = Table(kalasa_content, colWidths=[2.5*inch, doc.width - 2.5*inch - 0.2*inch]) # Adjusted width for text
    kalasa_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (1,0), (1,-1), 0.2*inch), # Padding for text column
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.1*inch),
    ]))
    story.append(kalasa_table)
    story.append(Spacer(1, 0.2*inch))

    # --- Udupi ---
    story.append(Paragraph("Udupi: Coastal Beauty & Temple Heritage", styles['SectionTitle']))
    story.append(Paragraph(udupi_desc, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    # --- Kudremukh ---
    story.append(Paragraph("Kudremukh: Rolling Grasslands & Wildlife", styles['SectionTitle']))
    
    img_kudremukh_park = get_image_from_url(IMAGES["kudremukh_park"], width=2.2*inch)
    img_kudremukh_dam = get_image_from_url(IMAGES["kudremukh_dam"], width=2.2*inch)

    kudremukh_content = [
        [img_kudremukh_park, Paragraph(kudremukh_desc, styles['BodyText'])],
        [Paragraph("<i>Kudremukh National Park: Biodiversity Hotspot</i>", styles['CaptionText']), ''],
        [img_kudremukh_dam, Paragraph("The Lakya Dam area provides breathtaking views and highlights the region's water resources.", styles['BodyText'])],
        [Paragraph("<i>Lakya Dam Viewpoint: Serene Waterscape</i>", styles['CaptionText']), '']
    ]
    kudremukh_table = Table(kudremukh_content, colWidths=[2.5*inch, doc.width - 2.5*inch - 0.2*inch])
    kudremukh_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (1,0), (1,-1), 0.2*inch),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.1*inch),
    ]))
    story.append(kudremukh_table)
    story.append(Spacer(1, 0.2*inch))
    
    # --- Netravati Peak ---
    story.append(Paragraph("Netravati Peak: Trekker's Paradise", styles['SectionTitle']))
    img_netravati = get_image_from_url(IMAGES["netravati_peak"], width=2.2*inch)
    
    netravati_content = [
        [img_netravati, Paragraph(netravati_desc, styles['BodyText'])] ,
        [Paragraph("<i>Netravati Peak Trek: Breathtaking Vistas</i>", styles['CaptionText']), '']
    ]
    netravati_table = Table(netravati_content, colWidths=[2.5*inch, doc.width - 2.5*inch - 0.2*inch])
    netravati_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (1,0), (1,-1), 0.2*inch),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.1*inch),
    ]))
    story.append(netravati_table)
    story.append(Spacer(1, 0.3*inch))

    # --- Contact Information ---
    story.append(PageBreak()) # Ensure contact info is on a new page or has space
    story.append(Paragraph("Contact Information", styles['ContactTitle']))
    story.append(Paragraph(f"For Bookings & Enquiries:", styles['BodyText']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(f"<b>Phone:</b> {PHONE}", styles['ContactInfo']))
    story.append(Paragraph(f"<b>Email:</b> {EMAIL}", styles['ContactInfo']))
    story.append(Paragraph(f"<b>Website:</b> {WEBSITE}", styles['ContactInfo']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("We look forward to helping you plan your unforgettable journey!", styles['BodyText']))


    # Build the PDF
    try:
        doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
        print(f"PDF '{FILENAME}' generated successfully.")
    except Exception as e:
        print(f"Error building PDF: {e}")

if __name__ == '__main__':
    build_pdf()
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#71717A"))
        
        # Running header on page 2
        if self._pageNumber > 1:
            self.drawString(36, 762, "Personal Resume Website — Project Report | Abhay Dewangan (Roll No: 26120050)")
            self.setStrokeColor(colors.HexColor("#E4E4E7"))
            self.setLineWidth(0.5)
            self.line(36, 756, 576, 756)
            
        # Running footer
        footer_text = f"Abhay Dewangan · Roll No: 26120050 · IIM Bangalore DBE · WD Mid-Term Project · Page {self._pageNumber} of {page_count}"
        self.drawCentredString(306, 22, footer_text)
        self.setStrokeColor(colors.HexColor("#E4E4E7"))
        self.setLineWidth(0.5)
        self.line(36, 32, 576, 32)
        
        self.restoreState()

def create_project_report(output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=38
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=colors.HexColor('#18181B')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#E8734A')  # Terracotta accent
    )
    
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#18181B'),
        spaceBefore=7,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.2,
        textColor=colors.HexColor('#27272A')
    )
    
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=10,
        firstLineIndent=-7,
        spaceAfter=2.5
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=9.8,
        textColor=colors.HexColor('#27272A')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor('#18181B')
    )

    story = []

    # ── HEADER BLOCK ──
    story.append(Paragraph("Personal Resume Website — Project Report", title_style))
    story.append(Paragraph("Website Development (WD) · Mid-Term Project · IIM Bangalore Online BBA in DBE", subtitle_style))
    story.append(Spacer(1, 6))

    # Metadata Table
    meta_data = [
        [
            Paragraph("<b>Student Name:</b> Abhay Dewangan", body_style),
            Paragraph("<b>Course:</b> Website Development (WD)", body_style),
            Paragraph("<b>Roll Number:</b> 26120050", body_style)
        ],
        [
            Paragraph("<b>File Name:</b> 26120050_WD_MTProject.pdf", body_style),
            Paragraph("<b>Live Website:</b> <a href='https://addevloper.github.io/26120050_WD_MTProject/' color='#E8734A'><u>GitHub Pages</u></a> / <a href='https://26120050-wd-mtproject.vercel.app' color='#E8734A'><u>Vercel</u></a>", body_style),
            Paragraph("<b>GitHub Repo:</b> <a href='https://github.com/ADDevloper/26120050_WD_MTProject' color='#E8734A'><u>ADDevloper/26120050_WD_MTProject</u></a>", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[175, 185, 180])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F4F5')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E4E4E7')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E4E4E7')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 6))

    # ── SECTION 1: OBJECTIVE & DESIGN PHILOSOPHY ──
    story.append(Paragraph("1. Objective & Design Philosophy: Modern Dark-Mode & Terracotta Aesthetic", h1_style))
    obj_text = (
        "The objective of this project was to transform a personal resume website into a modern, highly interactive, and responsive "
        "digital portfolio using pure semantic HTML5, advanced CSS3 techniques, and lightweight vanilla JavaScript (zero external "
        "frameworks, zero runtime dependencies). Drawing design inspiration from <b>buildwithclaude.in</b>, the website reflects "
        "the personality of a 19-year-old founder building two tech startups in public (FlowLab & Closet) while studying at IIM Bangalore."
    )
    story.append(Paragraph(obj_text, body_style))
    story.append(Spacer(1, 3))

    points = [
        "<b>Cohesive Color System:</b> Designed around CSS Custom Properties in <code>:root</code> featuring deep dark backgrounds (<code>#0A0A0B</code>, <code>#141416</code>) accented by high-energy terracotta/burnt-orange tones (<code>#E8734A</code>, <code>#F28C6A</code>) and crisp high-contrast typography.",
        "<b>Expressive Typography:</b> Integrated Google Fonts (Inter for clean, readable headings & body; JetBrains Mono for tech tags, code details, and stats). Fluid sizing via <code>clamp()</code> prevents awkward line wraps across viewports.",
        "<b>Micro-Animations & Visual Rhythm:</b> Implemented smooth cursor glow trails, dynamic HTML5 canvas particles, glowing animated rings around avatars, and interactive 3D card tilt without external animation libraries.",
        "<b>Accessibility & Motion Control:</b> Fully supports keyboard navigation via <code>:focus-visible</code> and honors user motion preferences using <code>@media (prefers-reduced-motion: reduce)</code>."
    ]
    for p in points:
        story.append(Paragraph(f"• {p}", bullet_style))
    story.append(Spacer(1, 4))

    # ── SECTION 2: CSS CONCEPTS & TECHNIQUES IMPLEMENTED ──
    story.append(Paragraph("2. CSS Concepts & Techniques Implemented", h1_style))
    story.append(Paragraph(
        "Every core CSS competency outlined in the module was intentionally engineered and organized into a maintainable hierarchy:",
        body_style
    ))
    story.append(Spacer(1, 3))

    tech_points = [
        "<b>CSS Selectors Hierarchy:</b> Element selectors (<code>body</code>, <code>h1-h3</code>, <code>a</code>) for clean reset and baseline rules; Class selectors (<code>.hero</code>, <code>.project-card</code>, <code>.skill-tag</code>) for reusable components; ID selectors (<code>#navbar</code>, <code>#hero</code>, <code>#projects</code>) for specific layout landmarks and scroll anchoring.",
        "<b>Flexbox Layouts (<code>display: flex</code>):</b> Used on the sticky navigation bar (logo badge left, links right), hero CTA button groups, hobby tag clusters, contact pill cards, and footer metadata alignment.",
        "<b>CSS Grid (<code>display: grid</code>):</b> Powers the About section info grid, 3-column Skills categorization, 2-column Projects grid, 3-column Experience timeline, and 4-column Achievements stats counter row.",
        "<b>Positioning & Sticky Behavior:</b> Pinned sticky navigation with <code>position: fixed</code> and <code>backdrop-filter: blur(20px)</code>; absolute layering for floating background ambient shapes, typewriter cursor, and avatar spin rings.",
        "<b>CSS Variables & Design Tokens:</b> 20+ custom variables defined in <code>:root</code> managing background steps, border shades, accent glows, spacing scales, and cubic-bezier easing curves.",
        "<b>Responsive Media Queries:</b> Four responsive breakpoints (1024px tablet, 768px mobile, 480px small mobile, prefers-reduced-motion) dynamically converting grids into single columns, adjusting typography scales, and toggling the mobile hamburger drawer.",
        "<b>Custom Micro-Interactions:</b> 3D card perspective tilt (<code>perspective(1000px) rotateX() rotateY()</code>), gradient text animations (<code>background-clip: text</code>), button ripple effects, and shimmering skill tags with sliding pseudo-elements."
    ]
    for tp in tech_points:
        story.append(Paragraph(f"• {tp}", bullet_style))
    story.append(Spacer(1, 5))

    # Skills Table
    skills_data = [
        [
            Paragraph("CSS Variables (<code>:root</code>)", table_cell_bold),
            Paragraph("Flexbox (<code>display: flex</code>)", table_cell_bold),
            Paragraph("CSS Grid (<code>display: grid</code>)", table_cell_bold),
            Paragraph("<code>position: fixed / sticky</code>", table_cell_bold)
        ],
        [
            Paragraph("Fluid <code>clamp()</code> Scale", table_cell),
            Paragraph("Glassmorphism Blur", table_cell),
            Paragraph("Media Queries (4 Breakpoints)", table_cell),
            Paragraph("CSS Keyframes & Transforms", table_cell)
        ],
        [
            Paragraph("3D Card Perspective Tilt", table_cell),
            Paragraph("Pseudo-elements (<code>::before/::after</code>)", table_cell),
            Paragraph("<code>prefers-reduced-motion</code>", table_cell),
            Paragraph("Google Fonts (Inter/JetBrains)", table_cell)
        ]
    ]
    t_skills = Table(skills_data, colWidths=[135, 135, 135, 135])
    t_skills.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FAFAFA')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E4E4E7')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E4E4E7')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_skills)

    # ── PAGE BREAK FOR CLEAN 2-PAGE LAYOUT ──
    story.append(PageBreak())

    # ── SECTION 3: SECTION-BY-SECTION WALKTHROUGH ──
    story.append(Paragraph("3. Section-by-Section Walkthrough & Design Decisions", h1_style))
    story.append(Paragraph(
        "Each section of the website was built semantically and styled to serve a specific communication objective:",
        body_style
    ))
    story.append(Spacer(1, 4))

    sections_table_data = [
        [
            Paragraph("Section", table_header),
            Paragraph("Semantic HTML", table_header),
            Paragraph("CSS & Design Decisions", table_header)
        ],
        [
            Paragraph("<b>Sticky Navigation</b>", table_cell_bold),
            Paragraph("<code>&lt;header&gt; &gt; &lt;nav&gt;</code>", table_cell),
            Paragraph("Pinned with <code>position: fixed</code>; glassmorphic backdrop blur (20px); active scrollspy link indicators; responsive animated hamburger toggle for mobile devices.", table_cell)
        ],
        [
            Paragraph("<b>Hero / Intro</b>", table_cell_bold),
            Paragraph("<code>&lt;section id='hero'&gt;</code>", table_cell),
            Paragraph("Full-height viewport (100vh); dynamic particle canvas with mouse physics; animated spinning gradient border on 'AD' initials badge; fluid gradient typewriter title; scroll-down indicator.", table_cell)
        ],
        [
            Paragraph("<b>About Me</b>", table_cell_bold),
            Paragraph("<code>&lt;section id='about'&gt;</code>", table_cell),
            Paragraph("2-column asymmetric grid; narrative lead typography highlighting IIM Bangalore and tech startup identity; 4 info pill cards with hover lift; interactive rounded hobby badge cluster.", table_cell)
        ],
        [
            Paragraph("<b>Education Timeline</b>", table_cell_bold),
            Paragraph("<code>&lt;section id='education'&gt;</code>", table_cell),
            Paragraph("Vertical timeline with pseudo-element line; glowing indicator dots that pulse on scroll intersection; cards for IIM Bangalore BBA DBE, Senior Secondary, and Secondary schooling.", table_cell)
        ],
        [
            Paragraph("<b>Skills &amp; Tech</b>", table_cell_bold),
            Paragraph("<code>&lt;section id='skills'&gt;</code>", table_cell),
            Paragraph("3-column responsive grid grouping Development, Business Strategy, and Tools/Platforms; monospace badge tags with animated shimmer sweep and hover glow.", table_cell)
        ],
        [
            Paragraph("<b>Featured Projects</b>", table_cell_bold),
            Paragraph("<code>&lt;section id='projects'&gt;</code>", table_cell),
            Paragraph("2-column card grid featuring FlowLab (AI Video Workflows), Closet (AI Wardrobe), Portfolio Website, and Building in Public; interactive 3D perspective mouse tilt.", table_cell)
        ],
        [
            Paragraph("<b>Startup Experience</b>", table_cell_bold),
            Paragraph("<code>&lt;section id='experience'&gt;</code>", table_cell),
            Paragraph("3-card horizontal layout with status badges ('Active: Building in Public', 'The Philosophy'); highlights dual founder roles and serial entrepreneurial journey.", table_cell)
        ],
        [
            Paragraph("<b>Achievements &amp; Stats</b>", table_cell_bold),
            Paragraph("<code>&lt;section id='achievements'&gt;</code>", table_cell),
            Paragraph("4-counter stats bar with animated JavaScript numbers counting up upon scroll entry; 4 achievement cards detailing IIM admission, dual startups, full-stack building, and public metrics.", table_cell)
        ],
        [
            Paragraph("<b>Contact &amp; Footer</b>", table_cell_bold),
            Paragraph("<code>&lt;footer id='contact'&gt;</code>", table_cell),
            Paragraph("Call-to-action cards linking directly to GitHub (@ADDevloper) and Email; animated heartbeat pulsing icon; copyright with auto-updating JavaScript year.", table_cell)
        ]
    ]

    t_sec = Table(sections_table_data, colWidths=[95, 110, 335])
    t_sec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#18181B')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#D4D4D8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E4E4E7')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#FBFBFB')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sec)
    story.append(Spacer(1, 5))

    # ── SECTION 4: PROJECT FILE STRUCTURE & HOSTING VERIFICATION ──
    story.append(Paragraph("4. Project File Structure & Hosting Verification", h1_style))
    
    struct_data = [
        [
            Paragraph("<b>Repository Layout</b>", table_cell_bold),
            Paragraph("<code>26120050_WD_MTProject/</code><br/>&nbsp;&nbsp;&bull; <code>index.html</code> (Semantic HTML5 markup with 8 structured sections)<br/>&nbsp;&nbsp;&bull; <code>style.css</code> (CSS3 custom properties, design tokens, responsive breakpoints, animations)<br/>&nbsp;&nbsp;&bull; <code>script.js</code> (Interactive typewriter, canvas particle physics, 3D card tilt, stats counter)<br/>&nbsp;&nbsp;&bull; <code>README.md</code> (Complete architecture documentation and deployment instructions)", table_cell)
        ],
        [
            Paragraph("<b>Zero-Dependency Compliance</b>", table_cell_bold),
            Paragraph("100% pure vanilla HTML5, CSS3, and JavaScript. Zero external UI frameworks (No Tailwind, Bootstrap, or jQuery) and zero build steps. Fully compatible with GitHub Pages, Vercel, and modern web browsers.", table_cell)
        ],
        [
            Paragraph("<b>Live Hosting URLs</b>", table_cell_bold),
            Paragraph("• <b>GitHub Repository:</b> <a href='https://github.com/ADDevloper/26120050_WD_MTProject' color='#E8734A'><u>https://github.com/ADDevloper/26120050_WD_MTProject</u></a><br/>• <b>GitHub Pages:</b> <a href='https://addevloper.github.io/26120050_WD_MTProject/' color='#E8734A'><u>https://addevloper.github.io/26120050_WD_MTProject/</u></a><br/>• <b>Vercel Deployment:</b> <a href='https://26120050-wd-mtproject.vercel.app' color='#E8734A'><u>https://26120050-wd-mtproject.vercel.app</u></a>", table_cell)
        ]
    ]
    t_struct = Table(struct_data, colWidths=[120, 420])
    t_struct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F4F5')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#E4E4E7')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E4E4E7')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_struct)
    story.append(Spacer(1, 5))

    # ── SECTION 5: LEARNING REFLECTION & CONCLUSION ──
    story.append(Paragraph("5. Learning Reflection & Conclusion", h1_style))
    refl_text = (
        "This project provided an invaluable hands-on opportunity to master modern CSS architecture and see how thoughtful "
        "design elevates a simple static resume into an engaging personal brand narrative. By adopting a refined dark theme "
        "with terracotta highlights, I learned how color restraint, deliberate negative space, and typographic scale create "
        "an authoritative feel. Implementing Flexbox, CSS Grid, and fluid clamp sizing reinforced how responsive design "
        "can be cleanly achieved without relying on bloated external UI libraries. The addition of subtle micro-animations "
        "(3D tilt, canvas particles, glowing states) demonstrated how interactive feedback dramatically improves user retention and delight."
    )
    story.append(Paragraph(refl_text, body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {output_filename}")

if __name__ == "__main__":
    out_pdf = r"c:\Users\asus\Documents\web assingment\26120050_WD_MTProject.pdf"
    create_project_report(out_pdf)

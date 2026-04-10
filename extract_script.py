"""
Extract the sales script from the .docx file and output it as structured HTML
with section markers and objection section data attributes.
"""

import sys
import json
from docx import Document
from docx.shared import Pt
import html as html_module

def extract_to_html(docx_path):
    doc = Document(docx_path)
    
    # Section headers that should be highlighted
    section_headers_lower = [
        "door 4: the 60 second eject",
        "call opening",
        "setting the frame",
        "discovery questions",
        "bucket 1: foundation",
        "bucket 2: visibility", 
        "bucket 3: connections",
        "recap",
        "part 4: the consequence",
        "part 5: the transition",
        "the offer",
        "stage 1",
        "stage 2",
        "stage 3",
        "selling themselves",
        "the risk removal",
        "the anchor",
        "the scarcity",
        "the value stack",
        "the price reveal",
        "objection handling",
    ]
    
    # Objection section markers - map text patterns to objection IDs
    # Use normalized (lowercase, ascii) matching
    objection_markers = [
        ("think-about-it", ["have to think about it"]),
        ("scammed-before", ["been scammed in the past", "not sure/been scammed"]),
        ("cant-afford-it", ["money objections"]),
        ("too-expensive", ["really expensive", "too expensive"]),
        ("parents", ["decision maker - parents"]),
        ("need-time", ["time objections"]),
        ("big-decision", ["big decision i have to think"]),
    ]
    
    html_parts = []
    seen_objections = set()
    
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        
        if not text:
            html_parts.append('<div class="script-line empty-line"><br></div>')
            continue
        
        # Normalize for matching (handle curly quotes etc.)
        text_norm = text.lower().replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
        
        # Check if this is a section header
        is_section_header = False
        for header in section_headers_lower:
            if header in text_norm:
                is_section_header = True
                break
        
        # Check if this starts an objection section (first match only)
        objection_id = None
        for oid, patterns in objection_markers:
            if oid in seen_objections:
                continue
            for pattern in patterns:
                if pattern in text_norm:
                    objection_id = oid
                    seen_objections.add(oid)
                    break
            if objection_id:
                break
        
        # Build inline HTML from runs
        line_html = ""
        for run in para.runs:
            run_text = html_module.escape(run.text)
            if not run_text:
                continue
            
            if run.bold:
                run_text = f"<b>{run_text}</b>"
            if run.italic:
                run_text = f"<i>{run_text}</i>"
            if run.underline:
                run_text = f"<u>{run_text}</u>"
            
            line_html += run_text
        
        if not line_html:
            line_html = html_module.escape(text)
        
        # Build classes
        classes = ["script-line"]
        if is_section_header:
            classes.append("section-header")
        if objection_id:
            classes.append("objection-section-header")
        
        attrs = f'class="{" ".join(classes)}"'
        
        if objection_id:
            attrs += f' data-objection="{objection_id}" id="objection-{objection_id}"'
        
        html_parts.append(f'<div {attrs}>{line_html}</div>')
    
    return '\n'.join(html_parts)


if __name__ == "__main__":
    content = extract_to_html("v2 script (2).docx")
    
    with open("script_content.html", "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Extracted {len(content)} characters of HTML")
    
    # Verify all objections were found
    import re
    found = re.findall(r'data-objection="([^"]+)"', content)
    print(f"Found objection markers: {found}")
    print("Saved to script_content.html")

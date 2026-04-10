"""Build the complete index.html with embedded script content."""
import sys

# Read the extracted HTML content
with open('script_content.html', 'r', encoding='utf-8') as f:
    script_html = f.read()

# Escape for embedding in JS template literal
script_html_escaped = script_html.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')

# Write as a JS variable to a temp file
with open('script_var.js', 'w', encoding='utf-8') as f:
    f.write('const DEFAULT_SCRIPT_CONTENT = `')
    f.write(script_html_escaped)
    f.write('`;')

print(f"Generated script_var.js ({len(script_html_escaped)} chars)")

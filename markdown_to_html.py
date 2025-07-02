#!/usr/bin/env python3
"""
markdown_to_html.py

Usage:
    python markdown_to_html.py input.md output.html

Converts a Markdown file to a simple HTML file for presentation or viewing in a browser.
Supports headings, lists, bold, italic, and code blocks.
"""
import sys
import markdown

if len(sys.argv) != 3:
    print("Usage: python markdown_to_html.py input.md output.html")
    sys.exit(1)

input_md = sys.argv[1]
output_html = sys.argv[2]

with open(input_md, 'r', encoding='utf-8') as f:
    md_text = f.read()

html = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])

html_template = f"""
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Markdown to HTML</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2em; background: #f9f9f9; }}
        h1, h2, h3, h4, h5, h6 {{ color: #2c3e50; }}
        pre, code {{ background: #f4f4f4; border-radius: 4px; padding: 2px 6px; }}
        pre {{ padding: 1em; overflow-x: auto; }}
        ul, ol {{ margin-left: 2em; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; }}
        th {{ background: #eee; }}
    </style>
</head>
<body>
{html}
</body>
</html>
"""

with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Converted {input_md} to {output_html}") 
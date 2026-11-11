#!/usr/bin/env python3
"""Render an existing local HTML resume as A4 PDF with WeasyPrint."""
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', type=Path)
    parser.add_argument('pdf', type=Path)
    args = parser.parse_args()
    if not args.html.is_file():
        parser.error('Input HTML does not exist')
    try:
        from weasyprint import HTML, CSS, default_url_fetcher
    except ImportError:
        parser.error('Install WeasyPrint in the active environment: python3 -m pip install weasyprint')
    # The distributed workflow uses self-contained HTML with embedded images.
    blocked_resources = []

    def embedded_resources_only(url):
        if not url.lower().startswith('data:'):
            blocked_resources.append(url)
            raise ValueError('Only embedded data resources are allowed')
        return default_url_fetcher(url)

    pdf = HTML(filename=str(args.html.resolve()),
               url_fetcher=embedded_resources_only).write_pdf(
                   stylesheets=[CSS(string='@page {size: A4;}')])
    if blocked_resources:
        parser.error('External or local resources were blocked. Embed images and CSS in the HTML first.')
    args.pdf.parent.mkdir(parents=True, exist_ok=True)
    args.pdf.write_bytes(pdf)
    print(args.pdf.resolve())

if __name__ == '__main__':
    main()

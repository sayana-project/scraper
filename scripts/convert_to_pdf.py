"""
Script de conversion du rapport Markdown en PDF professionnel
Utilise markdown2 et weasyprint pour générer un PDF formaté
"""

import markdown2
from weasyprint import HTML, CSS
from pathlib import Path

def convert_markdown_to_pdf():
    """Convertit le rapport Markdown en PDF avec style professionnel"""

    # Chemins des fichiers
    base_dir = Path(__file__).parent.parent
    md_file = base_dir / "docs" / "RAPPORT_PROFESSIONNEL_6PAGES.md"
    pdf_file = base_dir / "docs" / "RAPPORT_PROFESSIONNEL_6PAGES.pdf"

    print(f"Lecture du fichier Markdown: {md_file}")

    # Lire le fichier Markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convertir Markdown en HTML
    print("Conversion Markdown -> HTML...")
    html_content = markdown2.markdown(
        md_content,
        extras=['tables', 'fenced-code-blocks', 'header-ids', 'break-on-newline']
    )

    # CSS personnalisé pour un rendu professionnel
    css_style = """
    @page {
        size: A4;
        margin: 2.5cm 2cm;
        @bottom-center {
            content: "Page " counter(page) " / " counter(pages);
            font-size: 10pt;
            color: #666;
        }
    }

    body {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
        text-align: justify;
    }

    h1 {
        font-size: 20pt;
        color: #1a4d8c;
        border-bottom: 3px solid #1a4d8c;
        padding-bottom: 10px;
        margin-top: 0;
        margin-bottom: 20px;
        page-break-after: avoid;
    }

    h2 {
        font-size: 16pt;
        color: #1a4d8c;
        margin-top: 30px;
        margin-bottom: 15px;
        page-break-after: avoid;
        border-left: 4px solid #1a4d8c;
        padding-left: 10px;
    }

    h3 {
        font-size: 13pt;
        color: #2563eb;
        margin-top: 20px;
        margin-bottom: 10px;
        page-break-after: avoid;
    }

    p {
        margin-bottom: 10px;
        text-align: justify;
    }

    strong {
        color: #1a4d8c;
        font-weight: 600;
    }

    code {
        background-color: #f5f5f5;
        border: 1px solid #ddd;
        border-radius: 3px;
        padding: 2px 6px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 9pt;
        color: #c7254e;
    }

    pre {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-left: 4px solid #1a4d8c;
        border-radius: 4px;
        padding: 15px;
        margin: 15px 0;
        overflow-x: auto;
        page-break-inside: avoid;
    }

    pre code {
        background: none;
        border: none;
        padding: 0;
        color: #212529;
        font-size: 9pt;
        line-height: 1.4;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        page-break-inside: avoid;
        font-size: 10pt;
    }

    th {
        background-color: #1a4d8c;
        color: white;
        padding: 10px;
        text-align: left;
        font-weight: 600;
    }

    td {
        border: 1px solid #ddd;
        padding: 8px;
    }

    tr:nth-child(even) {
        background-color: #f8f9fa;
    }

    ul, ol {
        margin: 15px 0;
        padding-left: 25px;
    }

    li {
        margin-bottom: 8px;
    }

    hr {
        border: none;
        border-top: 1px solid #ddd;
        margin: 30px 0;
    }

    blockquote {
        border-left: 4px solid #1a4d8c;
        padding-left: 15px;
        margin: 20px 0;
        color: #555;
        font-style: italic;
    }

    /* Éviter les coupures de page au mauvais endroit */
    h2, h3 {
        page-break-after: avoid;
    }

    table, pre, blockquote {
        page-break-inside: avoid;
    }

    /* Style pour les métadonnées en début de document */
    body > p:first-of-type strong {
        display: block;
        margin: 5px 0;
    }
    """

    # Template HTML complet
    html_template = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Rapport Professionnel - Ear Sayana</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Générer le PDF
    print("Génération du PDF avec WeasyPrint...")
    HTML(string=html_template).write_pdf(
        pdf_file,
        stylesheets=[CSS(string=css_style)]
    )

    print(f"[OK] PDF généré avec succès: {pdf_file}")
    print(f"     Taille: {pdf_file.stat().st_size / 1024:.1f} KB")
    print()
    print("Le rapport PDF est prêt pour impression!")

    return pdf_file

if __name__ == "__main__":
    try:
        pdf_path = convert_markdown_to_pdf()
        print(f"\nFichier PDF créé: {pdf_path}")
    except Exception as e:
        print(f"[ERREUR] Échec de la conversion: {e}")
        import traceback
        traceback.print_exc()

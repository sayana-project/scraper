"""
Script de conversion du rapport Markdown en HTML professionnel
Le HTML peut ensuite être imprimé en PDF depuis n'importe quel navigateur (Ctrl+P)
"""

import markdown2
from pathlib import Path

def convert_markdown_to_html():
    """Convertit le rapport Markdown en HTML avec style professionnel"""

    # Chemins des fichiers
    base_dir = Path(__file__).parent.parent
    md_file = base_dir / "docs" / "RAPPORT_PROFESSIONNEL_6PAGES.md"
    html_file = base_dir / "docs" / "RAPPORT_PROFESSIONNEL_6PAGES.html"

    print(f"Lecture du fichier Markdown: {md_file}")

    # Lire le fichier Markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convertir Markdown en HTML
    print("Conversion Markdown -> HTML...")
    html_body = markdown2.markdown(
        md_content,
        extras=['tables', 'fenced-code-blocks', 'header-ids', 'break-on-newline']
    )

    # Template HTML complet avec CSS professionnel
    html_template = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport Professionnel - Ear Sayana - Simplon.co</title>
    <style>
        /* Styles pour l'impression */
        @media print {
            @page {
                size: A4;
                margin: 2.5cm 2cm;
            }

            body {
                font-size: 11pt;
            }

            h1, h2, h3 {
                page-break-after: avoid;
            }

            table, pre, blockquote {
                page-break-inside: avoid;
            }

            /* Numérotation des pages */
            @page {
                @bottom-center {
                    content: "Page " counter(page);
                }
            }
        }

        /* Styles généraux */
        body {
            font-family: 'Segoe UI', 'Calibri', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
        }

        /* Titres */
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

        /* Paragraphes */
        p {
            margin-bottom: 10px;
            text-align: justify;
        }

        strong {
            color: #1a4d8c;
            font-weight: 600;
        }

        /* Code */
        code {
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 2px 6px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
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

        /* Tableaux */
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
            border: 1px solid #0f3a6f;
        }

        td {
            border: 1px solid #ddd;
            padding: 8px;
        }

        tr:nth-child(even) {
            background-color: #f8f9fa;
        }

        /* Listes */
        ul, ol {
            margin: 15px 0;
            padding-left: 25px;
        }

        li {
            margin-bottom: 8px;
        }

        /* Séparateurs */
        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 30px 0;
        }

        /* Citations */
        blockquote {
            border-left: 4px solid #1a4d8c;
            padding-left: 15px;
            margin: 20px 0;
            color: #555;
            font-style: italic;
        }

        /* Bouton d'impression (caché à l'impression) */
        .print-button {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 24px;
            background-color: #1a4d8c;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            z-index: 1000;
        }

        .print-button:hover {
            background-color: #0f3a6f;
        }

        @media print {
            .print-button {
                display: none;
            }
        }

        /* Instructions */
        .instructions {
            background-color: #e8f4f8;
            border: 1px solid #1a4d8c;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 20px;
        }

        @media print {
            .instructions {
                display: none;
            }
        }
    </style>
</head>
<body>
    <button class="print-button" onclick="window.print()">🖨️ Imprimer en PDF</button>

    <div class="instructions">
        <strong>📄 Instructions pour créer le PDF:</strong>
        <ol>
            <li>Cliquez sur le bouton "Imprimer en PDF" ci-dessus (ou appuyez sur <code>Ctrl+P</code>)</li>
            <li>Dans la boîte de dialogue, sélectionnez "Microsoft Print to PDF" ou "Enregistrer au format PDF"</li>
            <li>Cliquez sur "Enregistrer" et choisissez l'emplacement</li>
            <li>Votre rapport professionnel PDF est prêt!</li>
        </ol>
    </div>

""" + html_body + """

</body>
</html>"""

    # Écrire le fichier HTML
    print(f"Écriture du fichier HTML: {html_file}")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"[OK] HTML généré avec succès: {html_file}")
    print(f"     Taille: {html_file.stat().st_size / 1024:.1f} KB")
    print()
    print("Pour créer le PDF:")
    print(f"1. Ouvrez le fichier dans votre navigateur: {html_file}")
    print("2. Appuyez sur Ctrl+P (ou cliquez sur le bouton 'Imprimer en PDF')")
    print("3. Choisissez 'Microsoft Print to PDF' ou 'Enregistrer au format PDF'")
    print("4. Enregistrez le fichier")
    print()
    print("Le rapport sera parfaitement formaté pour impression!")

    return html_file

if __name__ == "__main__":
    try:
        html_path = convert_markdown_to_html()
        print(f"\nFichier HTML créé: {html_path}")

        # Ouvrir automatiquement dans le navigateur
        import webbrowser
        webbrowser.open(str(html_path))
        print("\nLe fichier a été ouvert dans votre navigateur par défaut.")

    except Exception as e:
        print(f"[ERREUR] Échec de la conversion: {e}")
        import traceback
        traceback.print_exc()

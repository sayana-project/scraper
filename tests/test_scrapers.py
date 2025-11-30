# Test des scrapers C1
import sys
import os

# Ajout du chemin src au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scrapers'))

print("Chemin Python actuel:")
for p in sys.path:
    print(f"  {p}")

print("\nTest des imports...")

try:
    from seloger_scraper import SeLogerScraper
    print("✅ SeLogerScraper import OK")
except Exception as e:
    print(f"❌ Erreur SeLogerScraper: {e}")

try:
    from leboncoin_scraper import LeBonCoinScraper
    print("✅ LeBonCoinScraper import OK")
except Exception as e:
    print(f"❌ Erreur LeBonCoinScraper: {e}")

try:
    from csv_importer import CSVImporter
    print("✅ CSVImporter import OK")
except Exception as e:
    print(f"❌ Erreur CSVImporter: {e}")

try:
    from api_insee import INSEEImporter
    print("✅ INSEEImporter import OK")
except Exception as e:
    print(f"❌ Erreur INSEEImporter: {e}")

print("\nTest des scrapers...")

# Test SeLoger
try:
    seloger = SeLogerScraper()
    properties = seloger.run_scraper(max_pages=1)
    print(f"🏠 SeLoger: {len(properties)} propriétés extraites")
    for prop in properties[:2]:
        print(f"  - {prop['title']}: {prop['price']}€")
except Exception as e:
    print(f"❌ Erreur SeLoger scraper: {e}")

# Test LeBonCoin
try:
    leboncoin = LeBonCoinScraper()
    properties = leboncoin.run_scraper(max_pages=1)
    print(f"🏠 LeBonCoin: {len(properties)} propriétés extraites")
    for prop in properties[:2]:
        print(f"  - {prop['title']}: {prop['price']}€")
except Exception as e:
    print(f"❌ Erreur LeBonCoin scraper: {e}")

# Test CSV Importer
try:
    csv_importer = CSVImporter()
    # Création de fichiers d'exemple
    csv_importer.create_sample_files()

    # Test d'import
    properties = csv_importer.import_file("data/raw/sample_properties.csv")
    print(f"📁 CSV Importer: {len(properties)} propriétés importées")
    for prop in properties[:2]:
        print(f"  - {prop['title']}: {prop['surface']}m²")
except Exception as e:
    print(f"❌ Erreur CSV Importer: {e}")

# Test INSEE API
try:
    insee_importer = INSEEImporter()

    # Test simple
    print("\n📊 Test API INSEE...")
    test_data = insee_importer.get_test_data()
    for item in test_data[:2]:
        print(f"  - {item['title']}: {item['population']} habitants")

    # Test connexion
    connection_ok = insee_importer.test_api_connection()
    print(f"  Connexion API: {'✅ OK' if connection_ok else '❌ Échec'}")

except Exception as e:
    print(f"❌ Erreur INSEE Importer: {e}")

print("\n🎉 Test des scrapers C1 terminé !")
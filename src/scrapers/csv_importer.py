# CSV Importer (C1) - Import fichiers de données
import csv
import json
import pandas as pd
from typing import List, Dict, Optional
import logging
import time
from pathlib import Path

logger = logging.getLogger(__name__)

class CSVImporter:
    def __init__(self):
        self.supported_formats = ['.csv', '.json']

    def import_file(self, file_path: str) -> List[Dict]:
        """Import un fichier CSV ou JSON"""
        if not Path(file_path).exists():
            logger.error(f"Fichier non trouvé: {file_path}")
            return []

        file_extension = Path(file_path).suffix.lower()

        if file_extension == '.csv':
            return self._import_csv(file_path)
        elif file_extension == '.json':
            return self._import_json(file_path)
        else:
            logger.error(f"Format non supporté: {file_extension}")
            return []

    def _import_csv(self, file_path: str) -> List[Dict]:
        """Import un fichier CSV"""
        try:
            logger.info(f"Import CSV: {file_path}")

            # Détecter l'encodage
            encoding = self._detect_encoding(file_path)

            # Lecture avec validation
            df = pd.read_csv(file_path, encoding=encoding)

            # Validation des colonnes requises
            required_columns = ['title', 'price', 'surface']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                logger.error(f"Colonnes manquantes: {missing_columns}")
                return []

            # Nettoyage et validation
            df = self._validate_and_clean_data(df)

            # Conversion en dictionnaire
            properties = []
            for _, row in df.iterrows():
                property_data = self._format_property_data(row)
                if property_data:
                    properties.append(property_data)

            logger.info(f"Importé {len(properties)} propriétés depuis CSV")
            return properties

        except Exception as e:
            logger.error(f"Erreur import CSV: {e}")
            return []

    def _import_json(self, file_path: str) -> List[Dict]:
        """Import un fichier JSON"""
        try:
            logger.info(f"Import JSON: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Support de différents formats JSON
            if isinstance(data, list):
                properties = data
            elif isinstance(data, dict) and 'properties' in data:
                properties = data['properties']
            else:
                logger.error("Format JSON non reconnu")
                return []

            # Validation et nettoyage
            valid_properties = []
            for prop in properties:
                formatted_prop = self._validate_json_property(prop)
                if formatted_prop:
                    valid_properties.append(formatted_prop)

            logger.info(f"Importé {len(valid_properties)} propriétés depuis JSON")
            return valid_properties

        except Exception as e:
            logger.error(f"Erreur import JSON: {e}")
            return []

    def _detect_encoding(self, file_path: str) -> str:
        """Détecte l'encodage du fichier"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Lire les 10k premiers octets

            # Détection basique
            if b'\0' in raw_data:
                return 'utf-8'
            elif b'\xc3\xa9' in raw_data or b'\xc3\xa0' in raw_data:
                return 'latin-1'
            else:
                return 'utf-8'
        except:
            return 'utf-8'

    def _validate_and_clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Valide et nettoie les données du DataFrame"""
        # Suppression des lignes avec valeurs nulles critiques
        df = df.dropna(subset=['title', 'price', 'surface'])

        # Conversion des types
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['surface'] = pd.to_numeric(df['surface'], errors='coerce')

        # Suppression des valeurs invalides
        df = df.dropna(subset=['price', 'surface'])

        # Filtres de validité
        df = df[
            (df['price'] > 0) &
            (df['surface'] > 0) &
            (df['price'] <= 10000000) &  # Prix max raisonnable
            (df['surface'] <= 1000)         # Surface max raisonnable
        ]

        return df

    def _format_property_data(self, row) -> Optional[Dict]:
        """Formate une ligne en dictionnaire de propriété"""
        try:
            # Champs obligatoires
            title = str(row['title']).strip()
            price = int(float(row['price']))
            surface = int(float(row['surface']))

            # Champs optionnels avec valeurs par défaut
            postal_code = str(row.get('postal_code', '')).strip()
            city = str(row.get('city', 'Ville inconnue')).strip()

            if not all([title, price, surface]):
                logger.warning(f"Propriété incomplète ignorée: {row}")
                return None

            return {
                'title': title,
                'price': price,
                'surface': surface,
                'postal_code': postal_code or '75001',
                'city': city or 'Paris',
                'source': 'csv_import',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            logger.error(f"Erreur formatage propriété: {e}")
            return None

    def _validate_json_property(self, prop: Dict) -> Optional[Dict]:
        """Valide une propriété depuis JSON"""
        try:
            # Champs requis
            title = str(prop.get('title', '')).strip()
            price = int(float(prop.get('price', 0)))
            surface = int(float(prop.get('surface', 0)))

            if not all([title, price, surface]):
                return None

            return {
                'title': title,
                'price': price,
                'surface': surface,
                'postal_code': str(prop.get('postal_code', '')).strip() or '75001',
                'city': str(prop.get('city', '')).strip() or 'Paris',
                'source': 'json_import',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            logger.error(f"Erreur validation propriété JSON: {e}")
            return None

    def create_sample_files(self, output_dir: str = "data/raw"):
        """Crée des fichiers d'exemple pour tester"""
        Path(output_dir).mkdir(exist_ok=True)

        # Fichier CSV d'exemple
        sample_csv_data = [
            {
                'title': 'Appartement T3 Centre',
                'price': 450000,
                'surface': 80,
                'postal_code': '75001',
                'city': 'Paris'
            },
            {
                'title': 'Studio Montmartre',
                'price': 320000,
                'surface': 35,
                'postal_code': '75018',
                'city': 'Paris'
            }
        ]

        csv_path = Path(output_dir) / "sample_properties.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            if sample_csv_data:
                writer = csv.DictWriter(f, fieldnames=sample_csv_data[0].keys())
                writer.writeheader()
                writer.writerows(sample_csv_data)

        # Fichier JSON d'exemple
        json_path = Path(output_dir) / "sample_properties.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(sample_csv_data, f, ensure_ascii=False, indent=2)

        logger.info(f"Fichiers d'exemple créés dans {output_dir}")
        return csv_path, json_path

# Test de l'importer
if __name__ == "__main__":
    importer = CSVImporter()

    # Création de fichiers d'exemple
    csv_file, json_file = importer.create_sample_files()

    # Test import CSV
    print(f"\n📄 Test import CSV: {csv_file}")
    csv_properties = importer.import_file(str(csv_file))
    print(f"✅ {len(csv_properties)} propriétés importées du CSV")

    # Test import JSON
    print(f"\n📄 Test import JSON: {json_file}")
    json_properties = importer.import_file(str(json_file))
    print(f"✅ {len(json_properties)} propriétés importées du JSON")

    # Affichage des propriétés importées
    all_properties = csv_properties + json_properties
    print(f"\n🏠 Total: {len(all_properties)} propriétés importées")
    for prop in all_properties[:3]:
        print(f"- {prop['title']}: {prop['price']}€ ({prop['surface']}m²)")
import os
import re
import ollama

# =========================================================
# CONFIGURATION
# =========================================================
MODEL = "qwen2.5:3b"

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    BASE_DIR = os.getcwd()

OUTPUT_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "data", "raw"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Big Data context given to the LLM (No table names, no row limits)
BIG_DATA_CONTEXT = """
Vous êtes l'architecte de données pour le système Big Data du projet 'Move to Mars'.
Contexte :
La Terre envoie une grande population de colons sur Mars.
Nous devons construire une chaîne BI / Big Data à haute fréquence pour calculer le KPI principal :
'Taux de santé globale des colons' = (Nombre de colons ayant un état de santé normal / Nombre total de colons) * 100

Spécifications du système Big Data :
- Les données de santé proviennent de capteurs IoT biométriques connectés en continu (haute fréquence).
- La colonie enregistre en continu l'ensemble des événements, modules et métriques temporelles.
- Les volumes de données doivent refléter une véritable infrastructure Big Data à grande échelle.
"""

# =========================================================
# ÉTAPE 1 : LE LLM CONÇOIT L'ARCHITECTURE (PAGE BLANCHE)
# =========================================================
print("Interrogation du LLM pour concevoir l'architecture Big Data...\n")

prompt_architecte = """
En vous basant sur le contexte Big Data 'Move to Mars' et le KPI de santé à calculer :
Déterminez vous-même la liste complète des tables CSV nécessaires pour construire cette infrastructure.

Format de réponse STRICT :
Donnez uniquement la liste des noms de fichiers CSV séparés par des virgules (en majuscules), sans aucun texte explicatif.
"""

response_arch = ollama.chat(
    model=MODEL,
    messages=[
        {"role": "system", "content": BIG_DATA_CONTEXT},
        {"role": "user", "content": prompt_architecte},
    ]
)

raw_response = response_arch["message"]["content"].strip()
tables_generees = [
    item.strip().upper() if item.strip().upper().endswith(".CSV") else f"{item.strip().upper()}.CSV"
    for item in raw_response.split(",") if item.strip()
]

print(f"Architecture Big Data conçue par l'IA : {tables_generees}\n")

# =========================================================
# ÉTAPE 2 : DÉFINITION DYNAMIQUE DES SCHÉMAS ET RÈGLES
# =========================================================
def generate_big_data_table(filename):
    prompt_data = f"""
Vous devez concevoir la structure et générer le jeu de données Big Data pour la table '{filename}'.
Consignes :
1. Déterminez les colonnes appropriées (headers en ligne 1).
2. Adaptez la volumétrie au type de table : s'il s'agit d'une table de faits/capteurs IoT, générez un flux de données volumineux. S'il s'agit d'une dimension, générez la population complète.
3. Intégrez des pièges de Data Quality (espaces, mauvaises typologies, valeurs hors normes) pour tester notre pipeline d'ingestion ETL.

Formatage :
- Pas de balises Markdown (pas de ```csv).
- Aucun texte explicatif.
- Aucune virgule dans le contenu des cellules.
"""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": BIG_DATA_CONTEXT},
            {"role": "user", "content": prompt_data},
        ],
        options={"temperature": 0.3},
    )

    clean_text = re.sub(r"```[a-zA-Z]*", "", response["message"]["content"]).strip()
    lines = [l.strip() for l in clean_text.splitlines() if l.strip()]

    if not lines:
        return []

    # Validation dynamique du nombre de colonnes basée sur l'en-tête
    expected_cols = len(lines[0].split(","))
    valid_lines = [lines[0]]
    for l in lines[1:]:
        if len(l.split(",")) == expected_cols:
            valid_lines.append(l)

    return valid_lines


# Exécution de la génération
for filename in tables_generees:
    print(f"Génération de la table Big Data {filename} par le LLM...")
    data = generate_big_data_table(filename)
    
    file_path = os.path.join(OUTPUT_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(data) + "\n")
    print(f"   Fichier créé : {file_path}\n")

print("Infrastructure de données générée avec succès.")

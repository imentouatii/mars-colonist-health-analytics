# Move to Mars - Mars Colonist Health Analytics

## Project Overview

The **Move to Mars** project is an end-to-end Business Intelligence (BI) and Data Engineering pipeline designed to monitor, evaluate, and visualize the overall health of human colonists on Mars. 

The primary business objective is to compute and display the key performance indicator (KPI):

**Taux de santé globale (%)** = `(Nombre de colons en état de santé normal / Nombre total de colons) * 100`

### Health Assessment Criteria
A colonist is classified as having a **normal health state** if their medical metrics satisfy:
* **Oxygen Saturation (SpO2):** >= 95%
* **Heart Rate:** Between 60 and 100 BPM
* **Body Temperature:** <= 37.5 °C

---
## Interactive Dashboard

🔗 **[View Live Power BI Dashboard](https://app.powerbi.com/links/ZoHVBOTS60?ctid=b8c19512-2aed-471d-a8d1-9b06e7da786a&pbi_source=linkShare)** 

### Key Dashboard Features:
* **Global KPI Monitoring:** Real-time visibility into the overall colonist health status (Target: >= 90%).
* **Root Cause Diagnostics:** Immediate identification of primary health alerts (e.g., Low SpO2 anomaly distribution).
* **Cross-Dimensional Drill-Down:** Filterable matrix and charts by Habitat Module, Profession, Sol (Martian Day), Age, and Gender.

---

## Data Architecture & LLM Generation Approach

To guarantee 100% originality and simulate real-world data discovery, **no predefined database schemas or manual datasets were hardcoded**. Instead, an autonomous local LLM (`qwen2.5:3b` via **Ollama**) acted as the **Data Architect**.

### End-to-End Pipeline Strategy

```text
+-------------------------------------------------------+
|                   BUSINESS PROBLEM                    |
|    High-Frequency IoT Sensors & Colonist Health       |
+-------------------------------------------------------+
                            |
                            v
+-------------------------------------------------------+
|              LLM DATA ARCHITECT (Ollama)              |
|  1. Infers required relational tables & domain schema |
|  2. Generates CSV header structures dynamically       |
|  3. Injects Data Quality anomalies (for ETL testing)  |
+-------------------------------------------------------+
                            |
                            v
+-------------------------------------------------------+
|            PYTHON ENGINE (Data Generator)             |
|  1. Executes dynamic stream generation                |
|  2. Validates schema column consistency               |
|  3. Exports raw CSV datasets to data/raw/             |
+-------------------------------------------------------+
                            |
                            v
+-------------------------------------------------------+
|             TALEND ETL & POSTGRESQL DW                |
|  1. Data cleansing & type conversion                  |
|  2. Schema enrichment (Adds calculated ETL columns)   |
|  3. Loads clean tables into Data Warehouse            |
+-------------------------------------------------------+
                            |
                            v
+-------------------------------------------------------+
|                 POWER BI DASHBOARD                    |
|  1. Custom DAX Measures & Calculated Columns          |
|  2. Interactive KPI visualization & health monitoring |
|  3. Drill-down analysis by Module, Profession & Sol   |
+-------------------------------------------------------+
```

1. **Autonomous Schema Conception:** The LLM receives the high-level business problem and infers the necessary relational entities (e.g., IoT sensor measurements, colonist demographics, habitats, time dimension, critical scenarios).
2. **Scalable Volumetry:** The pipeline models continuous IoT sensor streams for medical measurements alongside event logs and core dimension tables.
3. **Data Quality Injection:** To stress-test our downstream ETL jobs (Talend) and Exploratory Data Analysis (EDA) notebooks, the generation script intentionally injects real-world data quality anomalies (untrimmed spaces, inconsistent date formats, missing fields, string units in numeric columns).

---

## Project Structure

```text

move-to-mars/
├── assets/                                # Image assets for documentation
│   └── schema.png                         # PostgreSQL ERD Screenshot
├── DATA_DOCUMENTATION.md                  # Complete Schema, Quality Audit & Transformation Specs
├── data/
│   ├── raw/                               # Generated raw CSV files (Input for ETL)
│   └── processed/                         # Cleaned CSV files (Output of ETL/Data Prep)
├── notebooks/
│   ├── data_quality_check.ipynb           # Data Quality Checks & Anomaly Audits
│   └── exploratory_data_analysis.ipynb    # Exploratory Data Analysis (EDA)
├── scripts/                               # Data Generation Scripts
│   └── generate_data.py                   # LLM-driven autonomous generator
├── talend/                                # Talend Open Studio ETL jobs & mappings
│   └── move_to_mars_etl.zip               # Exported Talend Job Items & Dependencies
├── sql/                                   # PostgreSQL DDL and Data Warehouse schemas
│   └── create_schema.sql                  # DDL schema definition script
├── power_bi/                              # Power BI Dashboards (.pbix) & Reports
│   └── Move To Mars.pbix
├── README.md                              # Main Project Overview
└── requirements.txt
```
---

## Datasets Summary

| Table Name | Description | Key Attributes / Metrics |
| :--- | :--- | :--- |
| `CONSTANTE_VITALE.csv` | High-frequency biometric IoT sensor data | `id_constante`, `id_colon`, `saturation_o2_pct`, `frequence_cardiaque_bpm`, `temperature_corporelle_c` |
| `SCENARIO.csv` | Colony critical event logs | `id_scenario`, `type_evenement`, `impact_sante`, `niveau_urgence` |
| `COLON.csv` | Colonist population records | `id_colon`, `nom`, `prenom`, `age`, `id_categorie_metier`, `id_module_habitation` |
| `DIM_TEMPS_MARS.csv` | Martian time dimension | `id_temps`, `datetime_terre`, `sol_mars`, `annee_mars` |
| `MODULE.csv` | Living and laboratory module infrastructure | `id_module`, `type_module`, `capacite`, `statut_module` |
| `CATEGORIE_METIER.csv` | Profession taxonomy on Mars | `id_categorie_metier`, `libelle_metier`, `famille_metier` |

> 📄 **Detailed Data Catalog:** For full column schemas, raw LLM data quality audit results, Talend ETL cleansing actions, and Power BI DAX logic, refer to [DATA_DOCUMENTATION.md](./DATA_DOCUMENTATION.md).

---

## Installation & Setup

### Prerequisites
* Python 3.10+
* Ollama with the qwen2.5:3b model installed locally:
  $ ollama pull qwen2.5:3b
* Power BI Desktop (for dashboard visualization)


### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/imentouatii/mars-colonist-health-analytics.git](https://github.com/imentouatii/mars-colonist-health-analytics.git)
   cd mars-colonist-health-analytics
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the synthetic data generator:
   ```bash
   python scripts/generate_data.py
   ```


---

## Data Pipeline Execution Flow

1. **Generation:** Run `scripts/generate_data.py` to populate raw CSV datasets in `data/raw/`.
2. **Exploratory Data Analysis:** Open `notebooks/data_quality_check.ipynb` to visually evaluate missing values, duplicate keys, and out-of-bound medical values in raw data.
3. **ETL Processing (Talend):** Import the Talend project from `talend/` to execute data cleansing, type conversions, schema enrichment (adding custom ETL columns), and loading into PostgreSQL.
4. **BI & DAX Analytics (Power BI):** Open `power_bi/Move To Mars.pbix` in Power BI Desktop or connect to PostgreSQL to execute dynamic DAX measures and interact with the dashboard.

---

## Key Technologies Used

* Language: Python 3.10 (Pandas, Re, OS)
* LLM Engine: Ollama (qwen2.5:3b)
* ETL Tool: Talend Open Studio (Cleansing, Schema Transformations & Loading)
* Database: PostgreSQL Data Warehouse
* Data Analysis: Jupyter Notebooks, Pandas
* Data Visualization & Analytics: Power BI (DAX Modeling & Reporting)

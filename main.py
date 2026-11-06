import time
import random
import pandas as pd
from typing import Dict, Any, List

# =====================================================================
# 1. LIVE DATA INGESTION ENGINE
# =====================================================================
class RegionalWaterTelemetryIngestor:
    """Simulates real-time telemetry gathering across multiple community sectors."""
    def __init__(self):
        self.sectors = ["Dehradun-North", "Dehradun-Sahaspur", "Dehradun-Vikasnagar", "Mussoorie-Suburbs"]

    def generate_batch_dataset(self, records_count: int = 20) -> pd.DataFrame:
        """Generates a structured Pandas DataFrame representing community water nodes."""
        data_pool = []

        for _ in range(records_count):
            sector = random.choice(self.sectors)
            scenario = random.choice(["pristine", "pristine", "heavy_runoff", "chemical_shift"])

            if scenario == "pristine":
                ph = round(random.uniform(7.0, 7.6), 2)
                tds = int(random.uniform(150, 300))
                turbidity = round(random.uniform(0.8, 2.0), 2)
            elif scenario == "heavy_runoff":
                ph = round(random.uniform(6.6, 7.2), 2)
                tds = int(random.uniform(520, 680))
                turbidity = round(random.uniform(5.5, 9.8), 2)
            elif scenario == "chemical_shift":
                ph = round(random.uniform(8.7, 9.4), 2)
                tds = int(random.uniform(320, 480))
                turbidity = round(random.uniform(1.5, 4.0), 2)

            data_pool.append({
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "Sector_ID": sector,
                "pH_Level": ph,
                "TDS_PPM": tds,
                "Turbidity_NTU": turbidity
            })

        return pd.DataFrame(data_pool)

# =====================================================================
# 2. AGENTIC ANALYSIS ENGINE (LOOP FRAMEWORK)
# =====================================================================
class WaterSafetyAnalystAgent:
    """Sub-Agent responsible for auditing physical water metrics via vector flags."""
    def evaluate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies algorithmic thresholds directly onto the tracking dataset."""
        processed_df = df.copy()

        # Categorize overall safety based on accepted institutional thresholds
        def calculate_safety_score(row: pd.Series) -> str:
            if row["TDS_PPM"] > 600 or row["Turbidity_NTU"] > 5.0:
                return "CRITICAL"
            elif row["pH_Level"] < 6.5 or row["pH_Level"] > 8.5 or row["TDS_PPM"] > 500:
                return "WARNING"
            return "SAFE"

        processed_df["Safety_Status"] = processed_df.apply(calculate_safety_score, axis=1)
        return processed_df

class RegionalTriageAgent:
    """Sub-Agent responsible for mapping system flags to field action alerts."""
    def assign_action_directives(self, df: pd.DataFrame) -> pd.DataFrame:
        processed_df = df.copy()

        action_map = {
            "SAFE": "Parameters regular. No immediate localized intervention required.",
            "WARNING": "Issue Boil Water Notice. Initiate minor tank filtration check.",
            "CRITICAL": "HALT MAIN LINE PIPELINE! Route sample splits immediately to testing laboratory."
        }

        processed_df["Field_Directive"] = processed_df["Safety_Status"].map(action_map)
        return processed_df

# =====================================================================
# 3. SYSTEM VERIFIER & EXPORTER
# =====================================================================
class ComplianceAuditEngine:
    """Orchestrates validation checks and handles saving clean records."""
    def run_security_check(self, df: pd.DataFrame) -> pd.DataFrame:
        verified_df = df.copy()
        # Enforce structural completeness check (verify that no analytical rows are null)
        assert verified_df["Safety_Status"].isnull().sum() == 0, "Analytical integrity check failed!"

        # Inject metadata audit tag
        verified_df["Audit_Verified"] = True
        return verified_df

    def export_report_to_csv(self, df: pd.DataFrame, filename: str = "water_grid_report.csv"):
        """Saves data into a clean, flat-file structure ready for field workers."""
        df.to_csv(filename, index=False)
        print(f"\n💾 System Report successfully exported to disk as: '{filename}'")

# =====================================================================
# 4. EXECUTION RUNNER
# =====================================================================
if __name__ == "__main__":
    print("🚀 Initializing Python Water Analytics Engine Core...")

    # Initialize pipeline elements
    ingestor = RegionalWaterTelemetryIngestor()
    analyst = WaterSafetyAnalystAgent()
    triage = RegionalTriageAgent()
    auditor = ComplianceAuditEngine()

    # 1. Fetch live telemetry stream data
    print("📥 Gathering records across regional distribution blocks...")
    raw_water_data = ingestor.generate_batch_dataset(records_count=10)

    # 2. Run analysis loop
    analyzed_data = analyst.evaluate_dataframe(raw_water_data)

    # 3. Inject actionable field directives
    triaged_data = triage.assign_action_directives(analyzed_data)

    # 4. Audit data and finalize records
    final_clean_report = auditor.run_security_check(triaged_data)

    # Display the final structured dataset inside the console terminal
    print("\n--- Live Processed Water Infrastructure Records ---")
    print(final_clean_report[["Sector_ID", "pH_Level", "TDS_PPM", "Turbidity_NTU", "Safety_Status"]])

    # 5. Save the report sheet to disk
    auditor.export_report_to_csv(final_clean_report)

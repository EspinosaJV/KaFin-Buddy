"""
KaFin-Buddy - Data Ingestion Stage

Responsibilities:
 - Read transactions.xlsx file
 - Verify that the file exists
 - Load the data into a pandas DataFrame
 - Display an ingestion summary

This module does NOT:
 - Validate data
 - Transform data
 - Save data
 - Generate reports
"""
# ===========================================================
# MODULE DEPENDENCIES
# ===========================================================

from pathlib import Path
import pandas as pd

# ===========================================================
# INGESTION
# ===========================================================

def ingest_data() -> pd.DataFrame:
    """
    Reads the raw transaction Excel file and returns a pandas DataFrame.

    Returns:
        pd.DataFrame: Raw transaction data.
    """

    # Project root directory
    base_dir = Path(__file__).resolve().parent.parent

    # Path to the raw transaction file
    raw_data_path = (
        base_dir
        / "data"
        / "raw"
        / "kafin-buddy_transactions.xlsx"
    )

    # Verify that the file exists
    if not raw_data_path.exists():
        raise FileNotFoundError(
            f"Transaction file not found:\n{raw_data_path}"
        )
    
    # Read the Excel file
    df = pd.read_excel(raw_data_path)

    # Display ingestion summary
    print("=" * 50)
    print("KaFin Buddy - Data Ingestion Summary")
    print("=" * 50)

    print(f"Rows Loaded : {len(df)}")
    print(f"Columns Detected : {len(df.columns)}")

    print("\nColumns")
    print("-" * 50)
    for column in df.columns:
        print(f" - {column}")

    print("\nData Types")
    print("-" * 50)
    print(df.dtypes)

    print("\nPreview")
    print("-" * 50)
    print(df.head())

    return df

# ===========================================================
# ENTRY POINT
# ===========================================================

if __name__ == "__main__":
    ingest_data()
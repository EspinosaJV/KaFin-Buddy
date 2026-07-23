"""
KaFin Buddy - Data Validation Stage

Responsibilities:
 - Validate the structure of the transaction DataFrame
 - Validate individual transaction rows
 - Identify invalid transactions
 - Generate validation errors
 - Return valid transactions & validation errors

This module DOES NOT:
 - Ingest raw files
 - Transform transaction data
 - Save data to SQLite
 - Generate Reports
"""

import pandas as pd
from config_loader import load_config 

def validate_schema(df: pd.DataFrame, rules: dict) -> list:
    """
    Validates that all required columns exist in the DataFrame.

    Args:
     - df (pd.DataFrame): Transaction DataFrame.
     - rules (dict): Validation rules.

    Returns:
     - list: Schema validation errors.
    """

    required_columns = rules["required_columns"]
    errors = []

    for column in required_columns:
        if column not in df.columns:
            errors.append({
                "column": column,
                "error": "Required column is missing"
            })

    return errors
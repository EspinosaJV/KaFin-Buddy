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

def validate_required_fields(df: pd.DataFrame, rules: dict) -> list:
    """
    Validates that all required fields contain values.

    Args:
     - df (pd.DataFrame): Transaction DataFrame.
     - rules (dict): Validation rules.
    
    Returns:
     - list: Required field validation errors
    """

    required_columns = rules["required_columns"]
    errors = []

    for index, row in df.iterrows():
        for column in required_columns:
            value = row[column]

            if pd.isna(value) or (isinstance(value, str) and value.strip() == ""):
                errors.append({
                    "row": index + 2,
                    "column": column,
                    "error": "Required field cannot be empty"
                })

    return errors

if __name__ == "__main__":

    df = pd.DataFrame({
        "Date": [""],
        "Source": ["BPI"],
        "Description": [""],
        "Category": ["Groceries"],
        "Amount": [137]
    })

    rules = load_config("validation_rules.json")

    errors = validate_required_fields(df, rules)

    print("Required Field Validation Errors:")
    print(errors)
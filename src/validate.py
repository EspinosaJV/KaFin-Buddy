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

def validate_data_types(df: pd.DataFrame, rules: dict) -> list:
    """
    Validates that transaction fields contain the expected data types.

    Args:
        df (pd.DataFrame): Transaction DataFrame.
        rules (dict): Validation rules.

    Returns:
        list: Data type validation errors.
    """

    data_type_rules = rules["data_types"]
    errors = []

    for index, row in df.iterrows():
        for column, expected_type in data_type_rules.items():
            value = row[column]
            if expected_type == "datetime":
                try:
                    pd.to_datetime(value)
                except (ValueError, TypeError):
                    errors.append({
                        "row": index + 2,
                        "column": column,
                        "value": value,
                        "error": "Value must be a valid date"
                    })
            elif expected_type == "numeric":
                try:
                    pd.to_numeric(value)
                except (ValueError, TypeError):
                    errors.append({
                        "row": index + 2,
                        "column": column,
                        "value": value,
                        "error": "Value must be numeric"
                    })
    return errors

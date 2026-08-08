"""
Kafin-Buddy - Data Transformation Stage

Responsibilities:
 - Standardize transaction column names
 - Standardize transaction dates
 - Standardize transaction amounts
 - Normalize text fields
 - Enrich transactions with category metadata
 - Generate transaction IDs
 - Add processing metadata

This module DOES NOT:
 - Ingest raw files
 - Validate raw data
 - Save raw data to SQLite
 - Generate reports
"""

import hashlib
from datetime import datetime

import pandas as pd

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes transaction column names.

    Args:
     - df (pd.DataFrame): Validated transaction DataFrame.

    Returns:
     - pd.DataFrame: DataFrame with standardized column names.
    """

    df = df.copy()

    df = df.rename(columns={
        "Date": "transaction_date",
        "Source": "source",
        "Description": "description",
        "Category": "category",
        "Amount": "amount",
        "Notes": "notes"
    })

    return df

def standardize_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts transaction dates into a standardized datetime format.

    Args:
     - df (pd.DataFrame): Validated transaction DataFrame.

    Returns:
     - pd.DataFrame: DataFrame with standardized transaction dates.
    """

    df = df.copy()

    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    return df

def standardize_amounts(df:pd.DataFrame) -> pd.DataFrame:
    """
    Converts transaction amounts into numeric values.

    Args:
     - df (pd.DataFrame): Validated transaction DataFrame

    Returns:
     - pd.DataFrame: DataFrame with standardized transaction amounts.
    """

    df = df.copy()

    df["amount"] = pd.to_numeric(df["amount"])

    return df

def normalize_text(df:pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes text fields by removing unnecessary whitespace.

    Args:
     - df (pd.DataFrame): Validated transaction DataFrame.

    Returns:
     - pd.DataFrame: DataFrame with normalized text fields.
    """

    df = df.copy()

    text_columns = [
        "source",
        "description",
        "category",
        "notes"
    ]

    for column in text_columns:
        df[column] = df[column].apply(lambda value: value.strip() if isinstance(value, str) else value)

    return df

def enrich_categories(df:pd.DataFrame, categories: dict) -> pd.DataFrame:
    """
    Adds category group and transaction type metadata.

    Args:
     - df (pd.DataFrame): Validated transaction DataFrame.
     - categories (dict): Category configuration.

    Returns:
     - pd.DataFrame: DataFrame enriched with category metadata.
    """

    df = df.copy()

    df["category_group"] = df["category"].map(lambda category: categories[category]["group"])

    df["transaction_type"] = df["category"].map(lambda category: categories[category]["type"])

    return df

def generate_transaction_id(row: pd.Series) -> str:
    """
    Generates a deterministic transaction ID from transaction attributes.

    Args:
     - row (pd.Series): Transaction row.
    
    Returns:
     - str: Deterministic transaction ID.
    """

    transaction_string = "|".join([
        str(row["transaction_date"]),
        str(row["source"]),
        str(row["description"]),
        str(row["category"]),
        str(row["amount"]),
        str(row["notes"])
    ])

    return hashlib.sha256(
        transaction_string.encode("utf-8")
    ).hexdigest()

def add_transaction_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds deterministic transaction IDs.

    Args:
     - df (pd.DataFrame): Validated transaction DataFrame.

    Returns:
     - pd.DataFrame: DataFrame with transaction IDs.
    """

    df = df.copy()

    df["transaction_id"] = df.apply(
        generate_transaction_id,
        axis=1
    )

    return df

def add_processing_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds processing metadata to the transaction DataFrame.

    Args:
     - df (pd.DataFrame): Transaction DataFrame.

    Returns:
     - pd.DataFrame: DataFrame with processing metadata.
    """

    df = df.copy()

    df["created_at"] = datetime.now()

    return df

def transform_data(
        df: pd.DataFrame,
        categories:dict
) -> pd.DataFrame:
    """
    Runs the complete transaction transformation pipeline.

    Args:
     - df (pd.DataFrame): Validated transaction DataFrame.
     - categories (dict): Category configuration.

    Returns:
     - pd.DataFrame: Fully transformed transaction DataFrame.
    """
    df = standardize_columns(df)

    df = standardize_dates(df)

    df = standardize_amounts(df)

    df = normalize_text(df)

    df = enrich_categories(df, categories)

    df = add_transaction_ids(df)

    df = add_processing_metadata(df)

    return df
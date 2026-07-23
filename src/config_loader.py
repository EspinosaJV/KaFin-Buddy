"""
KaFin Buddy - Configuration Loader

Responsibilities:
 - Load JSON configuration files
 - Return configuration as Python dictionaries

This module does NOT:
 - Validate data
 - Transform data
 - Access the database
 - Generate reports
"""

from pathlib import Path
import json

def load_config(filename: str) -> dict:
    """
    Loads a JSON configuration file.

    Args:
        filename (str): Name of the configuration file.

    Returns:
        dict: Configuration data
    """

    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / "config" / filename

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found:\n{config_path}"
        )

    with config_path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    return config

if __name__ == "__main__":
    sources = load_config("sources.json")

    print("Loaded configuration:")
    print(sources)

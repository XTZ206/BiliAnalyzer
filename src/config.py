import json
import os
from pathlib import Path
from typing import Dict

CONFIG_PATH = Path(__file__).parent.parent / "config.json"

def load_config() -> Dict:
    """Load user configuration. If the config file does not exist, 
    create it with default values and return the default configuration."""
    if not CONFIG_PATH.exists():
        # Create default configuration if file does not exist
        default_config = {"output_dir": "output/", "page_size": 20, "sort_order": "time"}
        save_config(default_config)
        print(f"Config file not found. Created default configuration at: {CONFIG_PATH}")
        return default_config
    
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        # Return default configuration if loading fails, but do not overwrite existing file
        return {"output_dir": "output/", "page_size": 20, "sort_order": "time"}

def save_config(config: Dict) -> None:
    """Save user configuration to file. 
    Creates the directory if it does not exist."""
    os.makedirs(CONFIG_PATH.parent, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"Configuration saved to: {CONFIG_PATH}")

def get_config_value(key: str, default=None):
    """Retrieve a configuration value by key.
    Returns the default value if the key is not found."""
    config = load_config()
    return config.get(key, default)
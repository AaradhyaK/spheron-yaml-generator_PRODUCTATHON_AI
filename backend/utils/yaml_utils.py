import yaml
from typing import Any, Dict

def load_yaml(yaml_str: str) -> Dict[str, Any]:
    """
    Loads a YAML string into a Python dictionary.
    
    Args:
        yaml_str (str): The YAML string to load.
        
    Returns:
        dict: The parsed YAML as a dictionary.
    """
    try:
        return yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {str(e)}")

def dump_yaml(yaml_data: Dict[str, Any]) -> str:
    """
    Converts a Python dictionary to a YAML string.
    
    Args:
        yaml_data (dict): The data to convert to YAML.
        
    Returns:
        str: The YAML string representation of the input data.
    """
    try:
        return yaml.dump(yaml_data, default_flow_style=False)
    except yaml.YAMLError as e:
        raise ValueError(f"Error generating YAML: {str(e)}")

def validate_required_fields(yaml_data: Dict[str, Any], required_fields: list) -> bool:
    """
    Validates that the required fields exist in the YAML data.
    
    Args:
        yaml_data (dict): The YAML data to validate.
        required_fields (list): List of required field names.
        
    Returns:
        bool: True if all required fields exist, False otherwise.
    """
    for field in required_fields:
        if field not in yaml_data:
            return False
    return True

def add_default_values(yaml_data: Dict[str, Any], defaults: Dict[str, Any]) -> Dict[str, Any]:
    """
    Adds default values to the YAML data if the values don't exist.
    
    Args:
        yaml_data (dict): The YAML data to modify.
        defaults (dict): The default values to insert.
        
    Returns:
        dict: The modified YAML data with defaults applied.
    """
    for key, value in defaults.items():
        if key not in yaml_data:
            yaml_data[key] = value
    return yaml_data

def extract_fields(yaml_data: Dict[str, Any], fields: list) -> Dict[str, Any]:
    """
    Extracts specific fields from the YAML data.
    
    Args:
        yaml_data (dict): The YAML data to extract fields from.
        fields (list): The list of fields to extract.
        
    Returns:
        dict: A dictionary with the extracted fields.
    """
    return {field: yaml_data.get(field) for field in fields}

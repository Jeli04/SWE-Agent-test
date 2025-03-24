import yaml

def load_yaml(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)  # safe_load prevents arbitrary code execution
            return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
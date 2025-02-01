import yaml
import re

def convert_memory(memory: str) -> str:
    """
    Converts memory values to binary units (Gi, Mi, Pi, Ti, Ki).
    """
    match = re.match(r"(\d+(\.\d+)?)\s*(KB|MB|GB|TB|PB)", memory, re.IGNORECASE)
    if match:
        value = int(match.group(1))
        unit = match.group(3).lower()

        if unit == "kb":
           unit = "Ki"  # KB -> Ki
        elif unit == "mb":
            unit = "Mi"  # MB -> Mi
        elif unit == "gb":
            unit = "Gi"  # GB -> Gi
        elif unit == "tb":
            unit = "Ti"  # TB -> Ti
        elif unit == "pb":
            unit = "Pi"  # PB -> Pi
        
        return f"{value}{unit}"  # Return the converted value with 2 decimal precision
    return memory  # Return the original memory if no match found

def generate_yaml(nlp_response: str) -> str:
    try:
        # Extract the generated text from the Hugging Face response
        generated_text = nlp_response  # Adjust based on Hugging Face API response format
        
        # First, extract replicas to ensure it doesn't interfere with other extractions
        replicas_match = re.search(r"(\d+)\s+replicas", generated_text)
        replicas = int(replicas_match.group(1)) if replicas_match else 1  # Default to 1 replica if not found
        
        # Remove the replica information from the generated text to avoid conflicts during other extractions
        generated_text = re.sub(r"(\d+)\s+replicas", "", generated_text)

        # Extract service type (Node.js, Python, etc.)
        service_type_match = re.search(r"(Node\.js|Python|Java|Go|Ruby|PHP|Rust)", generated_text, re.IGNORECASE)
        service_type = service_type_match.group(0) if service_type_match else "GenericService"  # Default if not found

        # If the service type is Node.js, replace it with nodejs for YAML naming conventions
        if service_type.lower() == "node.js":
            service_type = "nodejs"

        # Extract memory (e.g., 1Gi, 2GB, 512MB, 10TB)
        memory_match = re.search(r"(\d+(\.\d+)?\s*(KB|MB|GB|TB|PB))", generated_text, re.IGNORECASE)
        memory = memory_match.group(0) if memory_match else "1Gi"  # Default to 1Gi if not found

        # Convert memory unit to binary units (e.g., "GB" to "Gi")
        memory = convert_memory(memory.lower())  # Apply memory conversion

        # Remove memory from the generated text to avoid conflicts during port and CPU extraction
        generated_text = re.sub(r"(\d+(\.\d+)?\s*(KB|MB|GB|TB|PB))", "", generated_text, re.IGNORECASE)

        # Extract port (e.g., "on port 3000", "port 3000", etc.)
        port_match = re.search(r"(on\s+port\s+|\s*port\s*)(\d+)", generated_text, re.IGNORECASE)
        port = int(port_match.group(2)) if port_match else 3000  # Default to port 3000 if not found

        # Remove port information from the generated text to avoid conflicts during CPU extraction
        generated_text = re.sub(r"(on\s+port\s+|\s*port\s*)\d+", "", generated_text, re.IGNORECASE)

        # Now, extract CPU (e.g., 500m, 1, 1.5 cores) after removing replicas, memory, and port
        cpu_match = re.search(r"(\d+(\.\d+)?[mM]?|\d+)", generated_text)  # Match whole numbers, decimals, and optional "m"
        cpu = cpu_match.group(0) if cpu_match else "500m"  # Default to 500m if not found

        # Generate YAML based on the extracted data

        yaml_data = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": f"{service_type.lower()}-service"
            },
            "spec": {
                "replicas": replicas,
                "selector": {
                    "matchLabels": {
                        "app": service_type.lower()
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": service_type.lower()
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": f"{service_type.lower()}-container",
                                "image": f"{service_type.lower()}-image:latest",  # Placeholder for dynamic image if needed
                                "resources": {
                                    "requests": {
                                        "memory": memory,
                                        "cpu": cpu
                                    },
                                    "limits": {
                                        "memory": memory,
                                        "cpu": cpu
                                    }
                                },
                                "ports": [
                                    {
                                        "containerPort": port  # Port extracted from input
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }

        # Return the YAML configuration as a string
        return yaml.dump(yaml_data)
    
    except Exception as e:
        raise Exception(f"Error generating YAML: {str(e)}")

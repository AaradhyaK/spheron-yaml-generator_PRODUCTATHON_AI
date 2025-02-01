import yaml

def validate_yaml(yaml_str: str) -> tuple:
    try:
        # Try loading the YAML to check for validity
        yaml_data = yaml.safe_load(yaml_str)

        # Validate presence of required top-level fields
        required_fields = ['apiVersion', 'kind', 'metadata', 'spec']
        for field in required_fields:
            if field not in yaml_data:
                return False, f"Missing required field: {field}"

        # Validate specific fields under spec (Deployment and Autoscaler)
        if yaml_data['kind'] == 'Deployment':
            if 'replicas' not in yaml_data['spec']:
                return False, "Missing required field 'replicas' in Deployment."
            if 'template' not in yaml_data['spec'] or 'spec' not in yaml_data['spec']['template']:
                return False, "Missing 'template.spec' in Deployment."

            container_spec = yaml_data['spec']['template']['spec'].get('containers', [])
            if not container_spec:
                return False, "No containers specified in Deployment."
            
            for container in container_spec:
                if 'name' not in container:
                    return False, "Missing 'name' in container."
                if 'resources' not in container:
                    return False, "Missing 'resources' in container."
                if 'ports' not in container:
                    return False, "Missing 'ports' in container."
            
        elif yaml_data['kind'] == 'HorizontalPodAutoscaler':
            # Validate HorizontalPodAutoscaler fields
            if 'scaleTargetRef' not in yaml_data['spec']:
                return False, "Missing 'scaleTargetRef' in HorizontalPodAutoscaler."
            if 'minReplicas' not in yaml_data['spec']:
                return False, "Missing 'minReplicas' in HorizontalPodAutoscaler."
            if 'maxReplicas' not in yaml_data['spec']:
                return False, "Missing 'maxReplicas' in HorizontalPodAutoscaler."
        
        # Additional validations could be added here based on the complexity of the structure
        
        return True, ""  # If all checks pass

    except yaml.YAMLError as e:
        return False, f"YAML Error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected Error: {str(e)}"
    
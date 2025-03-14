import yaml
import logging
from flask import Flask, request, jsonify
from art import text2art

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Function to load configuration from YAML
def load_config():
    logging.debug("Loading configuration from api_config.yaml")
    with open("api_config.yaml", "r") as file:
        return yaml.safe_load(file)

# Load configuration from YAML file
config = load_config()

# Configure the server
port = config['server']['port']
base_url = config['server']['base_url']

# Function to validate headers
def validate_headers(headers_config):
    for header in headers_config:
        header_name = header['name']
        if header.get('required') and header_name not in request.headers:
            logging.warning(f"Header {header_name} is required and not present")
            return jsonify({"error": f"Header {header_name} is required"}), 400
    return None

# Function to validate query params
def validate_query_params(query_params_config):
    for param in query_params_config:
        param_name = param['name']
        if param.get('required') and param_name not in request.args:
            logging.warning(f"Query parameter {param_name} is required and not present")
            return jsonify({"error": f"Query parameter {param_name} is required"}), 400
    return None

# Function to validate path params
def validate_path_params(path_params_config):
    for param in path_params_config:
        param_name = param['name']
        if param.get('required') and param_name not in request.view_args:
            logging.warning(f"Path parameter {param_name} is required and not present")
            return jsonify({"error": f"Path parameter {param_name} is required"}), 400
    return None

# Function to get response code from headers
def get_response_code(default_response):
    response_code = int(request.headers.get('Response-Code', default_response))
    logging.debug(f"Response code obtained: {response_code}")
    return response_code

# Function to convert endpoint path
def convert_path(path):
    return path.replace("{", "<").replace("}", ">")

# Factory function to create endpoint function
def create_endpoint_func(endpoint):
    def endpoint_func(*args, **kwargs):
        logging.debug(f"Process endpoint: {endpoint['path']} with method: {endpoint['method'].upper()}")
        
        # Header validation
        header_validation = validate_headers(endpoint.get('headers', []))
        if header_validation:
            return header_validation

        # Query params validation
        query_param_validation = validate_query_params(endpoint.get('query_params', []))
        if query_param_validation:
            return query_param_validation

        # Path params validation
        path_param_validation = validate_path_params(endpoint.get('path_params', []))
        if path_param_validation:
            return path_param_validation

        # Get response code from headers
        response_code = get_response_code(endpoint.get('default_response',200))
        # Respond with the appropriate HTTP code
        response = endpoint['response'].get(response_code, {}).get('body', {})
        logging.debug(f"Response: {response}")
        return jsonify(response), response_code
    
    return endpoint_func

# Configure endpoints from YAML
for endpoint in config['endpoints']:
    logging.info(f"Configuring endpoint {endpoint['path']}")
    endpoint_path = base_url + convert_path(endpoint['path'])
    method = endpoint['method'].lower()

    # Create endpoint function using factory function
    endpoint_func = create_endpoint_func(endpoint)

    # Use a unique name for the endpoint and URL rule
    endpoint_name = f"{endpoint['method'].lower()}_{endpoint['path']}"
    app.add_url_rule(endpoint_path, endpoint_name, endpoint_func, methods=[method.upper()])

# Start the server
if __name__ == '__main__':
    # Print company name in ASCII
    ascii_art = text2art("Nubettix.com")
    print(ascii_art)
    logging.info(f"Starting server at port {port}")
    app.run(debug=True, host='0.0.0.0', port=port)
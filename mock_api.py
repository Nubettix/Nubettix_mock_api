import yaml
from flask import Flask, request, jsonify

app = Flask(__name__)

# Función para cargar la configuración del YAML
def load_config():
    with open("api_config.yaml", "r") as file:
        return yaml.safe_load(file)

# Cargar la configuración del archivo YAML
config = load_config()

# Configurar el servidor
port = config['server']['port']
base_url = config['server']['base_url']

# Función para validar los headers
def validate_headers(headers_config):
    for header in headers_config:
        header_name = header['name']
        if header.get('required') and header_name not in request.headers:
            return jsonify({"error": f"Header {header_name} is required"}), 400
    return None

# Función para validar los query params
def validate_query_params(query_params_config):
    for param in query_params_config:
        param_name = param['name']
        if param.get('required') and param_name not in request.args:
            return jsonify({"error": f"Query parameter {param_name} is required"}), 400
    return None

# Función para validar los path params
def validate_path_params(path, path_params_config):
    for param in path_params_config:
        param_name = param['name']
        if param.get('required') and param_name not in path:
            return jsonify({"error": f"Path parameter {param_name} is required"}), 400
    return None

# Configurar los endpoints desde el YAML
for endpoint in config['endpoints']:
    endpoint_path = base_url + endpoint['path']
    method = endpoint['method'].lower()

    def endpoint_func(endpoint=endpoint):
        # Validación de headers
        header_validation = validate_headers(endpoint.get('headers', []))
        if header_validation:
            return header_validation

        # Validación de query params
        query_param_validation = validate_query_params(endpoint.get('query_params', []))
        if query_param_validation:
            return query_param_validation

        # Validación de path params
        path_param_validation = validate_path_params(request.path, endpoint.get('path_params', []))
        if path_param_validation:
            return path_param_validation

        # Responder con el código HTTP adecuado
        response = endpoint['response'].get(200, {}).get('body', {})
        return jsonify(response)

    # Asociar el endpoint a su método HTTP
    if method == 'get':
        app.add_url_rule(endpoint_path, endpoint_path, endpoint_func, methods=['GET'])
    elif method == 'post':
        app.add_url_rule(endpoint_path, endpoint_path, endpoint_func, methods=['POST'])
    elif method == 'delete':
        app.add_url_rule(endpoint_path, endpoint_path, endpoint_func, methods=['DELETE'])

# Levantar el servidor
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
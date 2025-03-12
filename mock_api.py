import yaml
import logging
from flask import Flask, request, jsonify

# Configurar el logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Función para cargar la configuración del YAML
def load_config():
    logging.debug("Cargando configuración desde api_config.yaml")
    with open("api_config.yaml", "r") as file:
        return yaml.safe_load(file)

# Cargar la configuración del archivo YAML
config = load_config()

# Configurar el servidor
port = config['server']['port']
base_url = config['server']['base_url']

# Función para validar los headers
def validate_headers(headers_config):
    logging.debug("Validando headers")
    for header in headers_config:
        header_name = header['name']
        if header.get('required') and header_name not in request.headers:
            logging.warning(f"Header {header_name} es requerido y no está presente")
            return jsonify({"error": f"Header {header_name} is required"}), 400
    return None

# Función para validar los query params
def validate_query_params(query_params_config):
    logging.debug("Validando query params")
    for param in query_params_config:
        param_name = param['name']
        if param.get('required') and param_name not in request.args:
            logging.warning(f"Query parameter {param_name} es requerido y no está presente")
            return jsonify({"error": f"Query parameter {param_name} is required"}), 400
    return None

# Función para validar los path params
def validate_path_params(path_params_config):
    logging.debug("Validando path params")
    for param in path_params_config:
        param_name = param['name']
        if param.get('required') and param_name not in request.view_args:
            logging.warning(f"Path parameter {param_name} es requerido y no está presente")
            return jsonify({"error": f"Path parameter {param_name} is required"}), 400
    return None

# Función para obtener el código de respuesta desde los headers
def get_response_code():
    response_code = int(request.headers.get('Response-Code', 200))
    logging.debug(f"Código de respuesta obtenido: {response_code}")
    return response_code

# Función para convertir la ruta del endpoint
def convert_path(path):
    return path.replace("{", "<").replace("}", ">")

# Función de fábrica para crear la función del endpoint
def create_endpoint_func(endpoint):
    def endpoint_func(*args, **kwargs):
        logging.debug(f"Procesando endpoint: {endpoint['path']} con método: {endpoint['method'].upper()}")
        
        # Validación de headers
        header_validation = validate_headers(endpoint.get('headers', []))
        if header_validation:
            return header_validation

        # Validación de query params
        query_param_validation = validate_query_params(endpoint.get('query_params', []))
        if query_param_validation:
            return query_param_validation

        # Validación de path params
        path_param_validation = validate_path_params(endpoint.get('path_params', []))
        if path_param_validation:
            return path_param_validation

        # Obtener el código de respuesta desde los headers
        response_code = get_response_code()
        
        # Responder con el código HTTP adecuado
        response = endpoint['response'].get(response_code, {}).get('body', {})
        logging.debug(f"Respuesta generada: {response}")
        return jsonify(response)
    
    return endpoint_func

# Configurar los endpoints desde el YAML
for endpoint in config['endpoints']:
    logging.info(f"Configuring endpoint {endpoint['path']}")
    endpoint_path = base_url + convert_path(endpoint['path'])
    method = endpoint['method'].lower()

    # Crear la función del endpoint usando la función de fábrica
    endpoint_func = create_endpoint_func(endpoint)

    # Usar un nombre único para el endpoint y la URL en la regla
    endpoint_name = f"{endpoint['method'].lower()}_{endpoint['path']}"
    app.add_url_rule(endpoint_path, endpoint_name, endpoint_func, methods=[method.upper()])

# Levantar el servidor
if __name__ == '__main__':
    logging.info(f"Iniciando servidor en el puerto {port}")
    app.run(debug=True, host='0.0.0.0', port=port)
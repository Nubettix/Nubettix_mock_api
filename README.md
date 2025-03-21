# Nubettix_mock_api
This project allows you to create and simulate mock APIs for integration testing.

## Guide to Configure `api_config.yaml`

For detailed instructions on creating a YAML configuration file for Nubettix Mock API, please refer to the following guide:

[Guide to Creating a YAML Configuration for Nubettix Mock API](https://nubettix.com/en/guide-to-creating-a-yaml-configuration-for-nubettix-mock-api/)

# Instructions to set up the virtual environment and dependencies

## Create a virtual environment

1. Open a terminal and navigate to the project directory.

2. Run the following command to create a virtual environment:

```sh
python -m venv venv
```

3. Activate the virtual environment:

- On Windows:
  ```sh
  .\venv\Scripts\activate
  ```

- On macOS and Linux:
  ```sh
  source venv/bin/activate
  ```

## Install dependencies

With the virtual environment activated, run the following command to install Flask, PyYAML, and other required libraries:

```sh
pip install Flask pyyaml
pip install pyyaml flask
pip install art
```
or 

```sh
pip install -r requirements.txt
```

## Run the application

With the virtual environment activated and dependencies installed, you can run the application with the following command:

```sh
python mock_api.py
```

The application will run on `http://0.0.0.0:5000` by default.

## Deactivate the virtual environment

To deactivate the virtual environment, simply run the following command:

```sh
deactivate
```

## Create the executable with PyInstaller:
```sh
pyinstaller --onefile --name mock_api.exe mock_api.py
```

## YAML file structure

The YAML file defines the configuration of the Mock API. Below are the available options in the YAML configuration file.

### YAML file format
```yaml
server:
  port: <port>
  base_url: <base_url>

endpoints:
  - path: <endpoint_path>
    method: <http_method>
    query_params:
      - name: <param_name>
        required: <boolean>
    path_params:
      - name: <param_name>
        required: <boolean>
    default_response: <status_code>
    response:
      <status_code>:
        body:
          <json_structure>
    headers:
      - name: <header_name>
        required: <boolean>
```

### Configuration options description

1. **server**

Defines the server configuration:

- `port`: The port where the mock server will run (default is 5000).
- `base_url`: The base URL for all endpoints (e.g., /api/v1/).

Example:
```yaml
server:
  port: 5000
  base_url: "/api/v1/"
```

2. **endpoints**

Defines the endpoints of the Mock API. Each endpoint has several properties described below.

- **path** (Required): The endpoint path. Example: /items, /items/<item_id>.
- **method** (Required): The HTTP method of the endpoint. Can be one of the following: GET, POST, PUT, DELETE.
- **query_params** (Optional): List of query parameters to be validated in the endpoint. Each parameter has:
  - `name`: The name of the parameter.
  - `required`: Boolean indicating if the parameter is required (true or false).

Example:
```yaml
query_params:
  - name: "filter"
    required: true
```

- **path_params** (Optional): List of path parameters. Each parameter has:
  - `name`: The name of the parameter in the path (e.g., in /items/<item_id>, item_id is the parameter).
  - `required`: Boolean indicating if the parameter is required (true or false).

Example:
```yaml
path_params:
  - name: "item_id"
    required: true
```

- **body** (Optional): The request body for methods like POST, PUT, DELETE. Defines the expected structure of the body in JSON format.

Example:
```yaml
body:
  name: "string"
  description: "string"
```

- **response** (Required): Defines the mock responses for the endpoint, specifying the HTTP status codes and corresponding bodies. Each status code can have a different body.

Example:
```yaml
response:
  200:
    body:
      items:
        - id: 1
          name: "Item 1"
        - id: 2
          name: "Item 2"
  404:
    body:
      message: "Not Found"
```

- **headers** (Optional): List of HTTP headers to be validated. Each header has:
  - `name`: The name of the header.
  - `required`: Boolean indicating if the header is required (true or false).

Example:
```yaml
headers:
  - name: "Authorization"
    required: true
```

### Docker

#### Build the Docker Image

To build the Docker image for the Nubettix Mock API, run the following command:

```bash
docker build -t nubettix-mock-api .
```

#### Run the Docker Container

You can run the Docker container and pass the configuration file (`api_config.yaml`) from your local machine to the container using the following command:

```bash
docker run -p 4501:4501 -v $(pwd)/api_config.yaml:/app/api_config.yaml nubettix-mock-api
```

- **`-p 4501:4501`**: Maps port `4501` on your local machine to port `4501` in the container.
- **`-v $(pwd)/api_config.yaml:/app/api_config.yaml`**: Mounts the local `api_config.yaml` file into the container at `/app/api_config.yaml`.

This allows the container to use your local configuration file without needing to rebuild the image.

#### Notes:
- Ensure that the `api_config.yaml` file is in the current working directory when running the command.
- If you want to include the configuration file directly in the Docker image, you can modify the `Dockerfile` to copy it during the build process (see the Dockerfile section for details).

https://nubettix.com/mock-api/

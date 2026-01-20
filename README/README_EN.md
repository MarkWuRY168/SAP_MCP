# SAP MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Project Overview

SAP MCP (Model Context Protocol) Server is a platform for managing and controlling SAP systems, providing a series of tools and interfaces to facilitate user interaction with SAP systems.

## Features

### Core Functions

1. **Tool List Management**: Retrieve SAP_MCP tool list data
2. **Tool Detail Query**: Get tool details by tool ID, including input and output parameters
3. **Tool Execution**: Convert data to recognizable format based on tool details, call SAP_MCP tool to get execution results

### Web Management Interface

1. **Service Status Management**:
   - View MCP service running status
   - Start/Stop MCP service
   - View service logs in real-time
   - Port occupancy detection and conflict handling

2. **Configuration Management**:
   - SAP system configuration (Base URL, Client ID, username, password, timeout)
   - MCP server configuration (host, port, path)
   - Real-time configuration file saving

3. **Tool Management**:
   - Browse and search SAP MCP tools
   - View tool details and parameters
   - Execute tools with interactive forms

4. **Log Management**:
   - View logs with filtering options
   - Clear logs with confirmation
   - Real-time log updates

## Project Structure

```
SAP_MCP/
├── .gitignore                  # Git ignore file
├── LICENSE                     # MIT License
├── README.md                   # Project documentation
├── CHANGELOG.md                # Changelog
├── pyproject.toml            # Project configuration file
├── requirements.txt           # Project dependencies
├── config.py                 # Configuration file (not committed to version control)
├── config.example.py         # Configuration file example
├── server/                   # Server module
│   ├── __init__.py          # Package initialization file
│   ├── sap_mcp_server.py   # MCP server
│   ├── sap_mcp_client.py   # MCP client
│   └── http_client.py      # HTTP client
├── web/                      # Web management module
│   ├── static/               # Static files (CSS, JS)
│   ├── templates/            # HTML templates
│   └── main.py              # Web server entry file
├── log/                      # Log files directory
└── mcpDemo/                 # MCP example code
    ├── my_server.py        # Example server
    └── my_client.py        # Example client
```

## Technology Stack

- **Python**: >= 3.8
- **FastMCP**: MCP protocol implementation
- **httpx**: HTTP client
- **pydantic**: Data validation and settings management
- **FastAPI**: Web framework for management interface
- **Uvicorn**: ASGI server for FastAPI
- **Bootstrap 5**: Frontend CSS framework

## Installation Instructions

### System Requirements

- Python 3.8 or higher
- SAP system access permissions

### Installation Steps

1. **Clone the project**:
   ```bash
   git clone https://github.com/example/sap-mcp.git
   cd SAP_MCP
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**:
   ```bash
   cp config.example.py config.py
   # Edit config.py and fill in actual configuration information
   ```

## Configuration

### SAP Interface Configuration

Configure SAP interface information in the `config.py` file:

```python
SAP_CONFIG = {
    "base_url": "http://sap-s4d-app.example.com:8000/sap/zmcp",
    "client_id": "300",
    "sap-user": "YOUR_SAP_USER",
    "sap-password": "YOUR_SAP_PASSWORD",
    "timeout": 30
}
```

### MCP Server Configuration

```python
MCP_SERVER_CONFIG = {
    "host": "127.0.0.1",
    "port": 8000,
    "path": "/mcp"
}
```

## Usage

### Starting the Service

#### Method 1: Using Web Management Interface

1. Start Web management interface:
   ```bash
   python -m uvicorn web.main:app --reload --host 0.0.0.0 --port 8080
   ```

2. Open your web browser and navigate to `http://localhost:8080`

3. Click "Start Service" button in the web interface

#### Method 2: Command Line Start

1. Start MCP server:
   ```bash
   python server/sap_mcp_server.py
   ```

2. Server will run on `http://127.0.0.1:8000/mcp`

### Using Web Management Interface

1. **Service Management Page**:
   - View service running status
   - Start/Stop service
   - Check service configuration

2. **Tool Management Page**:
   - Browse and search SAP MCP tools
   - View tool details and parameters
   - Execute tools with interactive forms
   - View tool execution results

3. **Configuration Page**:
   - Modify SAP interface configuration
   - Modify MCP server configuration
   - Save configuration changes

4. **Logs Page**:
   - View service logs with filtering options
   - Clear logs with confirmation
   - Real-time log updates

### Client Connection Example

```python
import asyncio
from fastmcp import Client

async def main():
    client = Client("http://localhost:8000/mcp")
    async with client:
        # Get tool list
        result = await client.call_tool("get_tool_list", {})
        print(result)

asyncio.run(main())
```

### Tool Invocation Examples

1. **Get tool list**:
   ```python
   result = await client.call_tool("get_tool_list", {})
   ```

2. **Get tool details**:
   ```python
   result = await client.call_tool("get_tool_details", {"TOOL_ID": "TOOL_ID"})
   ```

3. **Use tool**:
   ```python
   result = await client.call_tool("use_tool", {
       "TOOL_ID": "TOOL_ID",
       "param1": "value1",
       "param2": "value2"
   })
   ```

## Development Guide

### Code Style

The project follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) code style guidelines.

Use the following tools for code formatting and checking:

```bash
# Code formatting
black .

# Code checking
flake8 .

# Type checking
mypy .
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests and generate coverage report
pytest --cov=server --cov-report=html
```

### Building and Publishing

```bash
# Build distribution package
python -m build

# Publish to PyPI
python -m twine upload dist/*
```

## Troubleshooting

### Common Issues

1. **Port Occupancy Error**:
   - Check if port 8000 is occupied by other programs
   - Modify port number in `config.py`

2. **SAP Interface Connection Failure**:
   - Confirm SAP server address is correct
   - Check network connection
   - Verify username and password

3. **Web Interface Unresponsive**:
   - Check if the web server is running
   - Verify the server logs for errors
   - Restart the web server application

## Developers

- **Product Design**: Mark (Wu Rangyu)
- **Developer**: Mark (Wu Rangyu)
- **Phone**: 18685095797
- **QQ**: 121980331
- **Email**: 121980331@qq.com

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork this project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## Changelog

For detailed changelog, please see [CHANGELOG.md](CHANGELOG.md).

## Support

If you have any questions or suggestions, please contact us via:

- Submit [Issue](https://github.com/example/sap-mcp/issues)
- Send email to: 121980331@qq.com

## Acknowledgments

Thanks to all developers who contributed to this project!

---

**Note**: Please do not commit configuration files containing sensitive information to version control system.

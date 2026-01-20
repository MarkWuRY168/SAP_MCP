# SAP MCP Server

## Features

### Core Functions

1. **AI-Powered Tool Management**: Utilizes AI technology to retrieve and manage SAP_MCP tool list data, enabling intelligent tool discovery and categorization
2. **Smart Tool Detail Query**: Leverages AI capabilities to get comprehensive tool details by tool ID, including structured input/output parameters and usage patterns
3. **AI-Enhanced Tool Execution**: Applies AI-driven data transformation to convert inputs into SAP-recognizable format, calling SAP_MCP tools to deliver optimized execution results

The project leverages AI technology to publish SAP system tools as MCP services, providing a viable solution for integrating cutting-edge AI capabilities into SAP systems.

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

## Docker Deployment

### Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

### Build and Run with Docker Compose

```bash
# Build and run all services
docker-compose up -d

# View logs for all services
docker-compose logs -f

# View logs for a specific service
docker-compose logs -f sap-mcp-web

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Services

- **sap-mcp-server**: SAP MCP Server running on port 8000
- **sap-mcp-web**: Web management interface running on port 8080

### Access the Application

1. **Web Management Interface**: Open your browser and navigate to `http://localhost:8080`
2. **MCP Server**: The server is available at `http://localhost:8000/mcp` for client connections

### Configuration

The `config.py` file is mounted as a volume in both containers, so you can modify it on the host machine and the changes will be reflected in the containers.

### Logs

Logs are stored in a Docker volume named `log_volume` and can be accessed from within the containers at `/app/log/sap_api.log`.

### Customization

You can customize the Docker configuration by modifying the following files:

- `Dockerfile`: For customizing the base image and build process
- `docker-compose.yml`: For customizing services, ports, volumes, and environment variables
- `.dockerignore`: For excluding files from the Docker build context

## Developers

- **Product Design**: Mark (Wu Rangyu)
- **Developer**: Mark (Wu Rangyu)
- **Phone**: 18685095797
- **QQ**: 121980331
- **Email**: 121980331@qq.com

## License

This project is licensed under the [MIT License](LICENSE).

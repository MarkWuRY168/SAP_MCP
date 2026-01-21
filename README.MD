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

## Deployment

### Prerequisites

- Python 3.8 or higher
- Git (optional, for cloning repository)
- Network connection (for installing dependencies)

### 1. Manual Deployment

#### 1.1 Get Project Code

**Method 1: Clone from Git repository**
```bash
git clone https://github.com/MarkWuRY168/SAP_MCP
cd SAP_MCP
```

**Method 2: Direct file copy**
- Copy the entire project folder to your server

#### 1.2 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

#### 1.3 Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install project
pip install -e .
```

#### 1.4 Configure Project

```bash
# Copy configuration example file
cp config.example.py config.py

# Edit configuration file (modify according to your environment)
# You can use any text editor, e.g.
# notepad config.py      # Windows
# vim config.py          # Linux/Mac
```

**Configuration file example:**
```python
# SAP interface configuration
SAP_CONFIG = {
    "base_url": "http://your-sap-server:port/sap/zmcp",
    "client_id": "your-client-id",
    "sap-user": "your-sap-username",
    "sap-password": "your-sap-password",
    "timeout": 30
}

# MCP server configuration
MCP_SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "path": "/mcp"
}
```

#### 1.5 Start Services

##### Method 1: Start MCP Server Only

```bash
# Start MCP server
python server/sap_mcp_server.py
```

##### Method 2: Start Web Management Interface

```bash
# Start Web management interface
python -m uvicorn web.main:app --host 0.0.0.0 --port 8080
```

### 2. Docker Deployment

#### 2.1 Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

#### 2.2 Build and Run with Docker Compose

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

#### 2.3 Offline Docker Deployment (For Network-Restricted Environments)

1. **Download images in a network-accessible environment:**
   ```bash
   # Pull Python base image
   docker pull python:3.10-slim
   
   # Save image to local file
   docker save python:3.10-slim -o python-3.10-slim.tar
   ```

2. **Transfer image file to target server** (using USB or other methods)

3. **Load image on target server:**
   ```bash
   docker load -i python-3.10-slim.tar
   ```

4. **Build and run:**
   ```bash
   # Build project image
   docker build -t sap-mcp .
   
   # Run container
   docker run -d -p 8000:8000 -p 8080:8080 sap-mcp
   ```

### 4. Important Notes for Docker Deployment

#### 4.1 Host Configuration for Docker

When running in Docker containers, it's crucial to configure the MCP server to listen on all network interfaces (0.0.0.0) instead of just localhost (127.0.0.1). This is already set correctly in the default configuration file, but if you modify it, ensure:

```python
# MCP server configuration
MCP_SERVER_CONFIG = {
    "host": "0.0.0.0",  # Important: Must be 0.0.0.0 for Docker deployment
    "port": 8000,
    "path": "/mcp"
}
```

If you set `host` to `127.0.0.1`, the MCP service will only be accessible within the container, not from outside.

#### 4.2 Port Mapping

Ensure that both the Web interface port (8080) and MCP service port (8000) are correctly mapped in your Docker configuration:

```yaml
# In docker-compose.yml
ports:
  - "8080:8080"  # Web management interface
  - "8000:8000"  # MCP service
```

### 5. Access the Application

- **Web Management Interface**: Open your browser and navigate to `http://server-ip:8080`
- **MCP Server**: The server is available at `http://server-ip:8000/mcp` for client connections

### 6. Common Issues

#### 6.1 Port Conflict

If ports are occupied, modify the port numbers in `config.py`:

```python
# Modify MCP server port
MCP_SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8001,  # Change to another port
    "path": "/mcp"
}
```

#### 6.2 Dependency Installation Failure

If dependency installation fails, try using a domestic mirror source:

```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

#### 6.3 Service Startup Failure

Check the log file `log/sap_api.log` for detailed error information:

```bash
# View log file
cat log/sap_api.log
```

#### 6.4 MCP Service Not Accessible from Outside Docker Container

**Issue**: After starting the MCP service through the Web management interface, the service is not accessible from outside the Docker container.

**Solution**: 
1. Ensure the MCP service is configured to listen on all network interfaces (`0.0.0.0`):
   ```python
   # In config.py
   MCP_SERVER_CONFIG = {
       "host": "0.0.0.0",  # Must be 0.0.0.0 for Docker deployment
       "port": 8000,
       "path": "/mcp"
   }
   ```
2. Ensure the port is correctly mapped in `docker-compose.yml`:
   ```yaml
   # In docker-compose.yml
   ports:
     - "8000:8000"  # Map MCP service port
   ```
3. Restart the Docker service after making changes

**Root Cause**: If the service listens only on `127.0.0.1`, it can only be accessed within the container, not from outside.

### 7. Service Management

#### 7.1 Stop Services

- **Press Ctrl+C** to stop running services
- Or use `kill` command to terminate processes

#### 7.2 Restart Services

Simply re-execute the startup commands.

### 8. Monitoring and Maintenance

- Regularly check log files: `log/sap_api.log`
- Periodically update dependencies: `pip install -r requirements.txt --upgrade`
- Regularly back up the configuration file: `config.py`

## Developers

- **Product Design**: Mark (Wu Rangyu)
- **Developer**: Mark (Wu Rangyu)
- **Phone**: 18685095797
- **QQ**: 121980331
- **Email**: 121980331@qq.com

## License

This project is licensed under the [MIT License](LICENSE).

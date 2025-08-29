# A2A Weather System

A demonstration of the Agent-to-Agent (A2A) protocol using a weather information system. This project showcases how AI agents can communicate seamlessly using standardized protocols, enhanced with AI-powered data processing.

## Features

- **A2A Protocol Implementation**: Standardized agent-to-agent communication
- **Weather Data Integration**: Real-time weather information via Tavily API
- **AI Enhancement**: Gemini AI processes raw data into user-friendly summaries
- **Client-Server Architecture**: Modular design with separate client and server components

## Project Structure

```
a2a-weather/
├── main.py              # Main entry point
├── pyproject.toml       # Project configuration
├── requirements.txt     # Python dependencies
├── uv.lock             # Dependency lock file
├── client/
│   └── weather_client.py   # A2A client implementation
└── server/
    └── weather_server.py    # A2A server implementation
```

## Quick Start

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone and setup the project:**
   ```bash
   mkdir a2a-weather
   cd a2a-weather
   
   # Initialize Python environment
   uv init
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

### Running the Application

1. **Start the server:**
   ```bash
   uv run python server/weather_server.py
   ```

2. **In a new terminal, run the client:**
   ```bash
   uv run python client/weather_client.py
   ```

## How A2A Protocol Works

The Agent-to-Agent protocol enables standardized communication between AI agents. Here's the complete flow:

### 1. **Agent Discovery**
```
GET /.well-known/agent.json
```
- Client discovers server capabilities
- Server returns supported operations and metadata

### 2. **Task Creation & Sending**
```
POST /tasks/send
```
- Client generates unique UUID for the task
- Query is wrapped in A2A message structure
- Server receives and processes the task

### 3. **Data Processing Pipeline**
- **Data Gathering**: Server extracts query and searches Tavily for weather data
- **AI Enhancement**: Gemini processes raw data into concise, formatted summaries
- **Response Formation**: Results wrapped in A2A-compliant JSON structure

### 4. **Response Handling**
- Server returns standardized A2A response with original message + AI-enhanced reply
- Client extracts and displays the processed information

## Benefits of A2A Protocol

- **Standardization**: Universal communication format across different agent systems
- **Interoperability**: Any A2A client can communicate with any A2A server
- **Scalability**: No custom integration code needed for new agent connections
- **Enhanced UX**: AI processing provides better, more accessible information

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/.well-known/agent.json` | GET | Agent capability discovery |
| `/tasks/send` | POST | Send task to agent for processing |

## Configuration

The system uses environment variables for configuration:
- API keys for external services (Tavily, Gemini)
- Server port and host settings
- Logging levels

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**The A2A protocol transforms agent communication from a complex integration challenge into a simple, standardized process. With just two endpoints and a consistent message format, you can build agents that work seamlessly with any A2A-compatible system.**
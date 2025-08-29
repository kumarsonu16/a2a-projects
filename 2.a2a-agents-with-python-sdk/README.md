# create virtual env using uv package manager
uv venv

# Activate virtual environment (On macOS/Linux)
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install Dependencies

uv pip install -r requirements.txt

# Environment Variables
 create .env file 

 ```bash

TAVILY_API_KEY=your_tavily_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

```

Starting the WeatherAgent Server:

# Navigate to your project directory
cd samples/a2a-python-sdk

# Ensure virtual environment is activated
source .venv/bin/activate

# Start the Weather agent server
uv run python -m agents.weather_agent --host localhost --port 10003


Starting the Client (in a new terminal):

# Open new terminal, navigate to project
cd samples/a2a-python-sdk

# Activate virtual environment
source .venv/bin/activate

# Start the dynamic client
uv run python -m client.client --agent-url http://127.0.0.1:10003


# Example Weather Interactions

# Single-turn Weather Interaction:

Weather query: What's the weather in Tokyo?

# Expected response flow:

Processing: What's the weather in Tokyo?

The weather in Tokyo is partly cloudy with a temperature of 27.2°C (81°F). The humidity is quite high at 89%, and there's a gentle breeze blowing from the NNE 
at 6.1 km/h. It feels like 30.4°C (86.7°F). Consider wearing light, breathable clothing due to the humidity. A light jacket might be useful for the evening. 
Enjoy your time in Tokyo! 🗼☁️


1. Task submitted
2. “Searching for current weather in Tokyo…”
3. “Processing weather data and formatting response…”
4. Rich weather report with temperature, conditions, humidity, wind, and recommendations


# Multi-turn Weather Interaction:

Weather query: What's the weather like?

# Agent response:
Processing: What's the weather like?

To give you the most accurate weather update, I need to know where you are! 🌍 Please tell me the city and state/country (e.g., 
"New York, NY" or "London, UK"). 📍


As you can see, the user query is unclear about the weather, i.e., which location he wants the weather details for; hence, the agent asks him to specify the location properly so that he can provide the weather details.


# Your reply: Bangalore, India


# Final result: Detailed weather report for Tokyo with beautiful formatting and local recommendations.

`OK! Here's the weather for Bangalore, India:

🌡️ Temperature: It's currently 24.4°C (75.9°F). Expect a high of around 29°C during the day and a low of 21°C tonight.
☁️ Conditions: Partly cloudy.
💨 Wind: From the Northwest at 18.4 kph.
💧 Humidity: 74%

It feels like 26°C. Consider wearing light, breathable clothing. A light jacket might be useful for the evening. Enjoy your day in
Bangalore! 🌆`


# You can also try out a few other Advanced Weather Queries:

- "Should I bring an umbrella in London today?"
- "What's the weather like for outdoor activities in Denver?"
- "Compare weather in Mumbai and Delhi"
- Press enter or click to view image in full size


#Conclusion

---

## 📦 Project Structure Overview

```
a2a-agents-with-python-sdk/
├── agents/
│   └── weather_agent/
│       ├── __main__.py          # Weather agent server entry point
│       ├── agent.py             # Core weather agent logic (LangChain, Gemini, Tavily)
│       └── agent_executor.py    # Bridges agent logic to A2A protocol (event-driven)
├── client/
│   └── client.py                # Dynamic A2A client (streaming, multi-turn)
├── main.py                      # Optional project runner
├── requirements.txt             # Dependencies
├── .env                         # API keys
└── README.md                    # Usage, examples, and documentation
```

---

## 🔄 Complete Flow Description

### 1. **User Interaction**
- The user runs the client (`client.py`) and enters a weather query (e.g., "What's the weather in Tokyo?").

### 2. **Client Communication**
- The client discovers the agent’s capabilities via the A2A protocol.
- It sends the query to the agent server using HTTP (JSON-RPC).

### 3. **Server Request Handling**
- The server (`__main__.py`) receives the request and passes it to the `WeatherAgentExecutor`.
- The executor manages the task lifecycle and event queue (streaming updates, multi-turn).

### 4. **Agent Logic**
- The executor calls the `WeatherAgent` (LangChain + Gemini + Tavily).
- The agent processes the query:
	- If location is missing, asks for clarification.
	- Uses Tavily for real weather data (or mock if API key missing).
	- Formats the response with actionable advice and emojis.

### 5. **Streaming Updates**
- The executor streams progress events (searching, processing, completed) back to the client.
- The client displays updates in real time (using `rich` for formatting).

### 6. **Multi-turn Conversation**
- If more info is needed (e.g., location), the agent requests it.
- The client prompts the user and continues the conversation until completion.

### 7. **Task Completion**
- The agent sends a final weather report.
- The client displays the result to the user.

---

## 💡 Key Concepts

- **A2A Protocol:** Event-driven, supports streaming and multi-turn conversations.
- **WeatherAgent:** Uses LangChain, Gemini, and Tavily for real-time weather info.
- **Executor:** Bridges agent logic to A2A protocol, manages events and tasks.
- **Client:** Discovers agent, sends queries, handles streaming updates, supports multi-turn.

---

## 📝 How to View the Diagram

- Paste the Mermaid diagram into a Markdown file or use a Mermaid live editor (https://mermaid-js.github.io/mermaid-live-editor/) to visualize.
- You can also use VS Code extensions like "Markdown Preview Mermaid Support" to view directly in your editor.

---

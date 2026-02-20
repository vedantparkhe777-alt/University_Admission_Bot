# 📚 Technical Documentation: University Admissions Bot

Welcome to the technical documentation for the **University Admissions Bot**. This document provides an in-depth look at the system architecture, core components, and design decisions behind the application.

---

## 1. System Architecture

The application is built on a modern AI stack designed for real-time data retrieval and conversational memory. The architecture follows a cyclical ReAct (Reasoning and Acting) pattern:

1. **User Input:** The user submits a query via the Streamlit interface.
2. **State Management:** Streamlit session state assigns or retrieves a unique `thread_id` to maintain conversation continuity.
3. **Agent Activation:** The LangGraph agent receives the prompt and the conversational history.
4. **Tool Execution:** The Gemini LLM determines if external knowledge is required. If yes, it triggers the Tavily Search API.
5. **Data Synthesis:** The agent synthesizes the retrieved web data with its system instructions (enforcing strict HTML formatting and exact deadlines).
6. **UI Rendering:** The final response is streamed back to the Streamlit UI and rendered with custom CSS.

---

## 2. Core Components

### The LLM Engine: Google Gemini 2.5 Flash
The application uses `ChatGoogleGenerativeAI` with the `gemini-2.5-flash` model. 
* **Temperature:** Set to `0.1` to ensure highly deterministic, factual responses (crucial for accurate admission dates and fees).
* **Role:** Acts as the central reasoning engine, deciding when to search and how to structure the final HTML output.

### The Agent Workflow: LangGraph (`create_react_agent`)
Instead of a simple linear prompt chain, the app uses LangGraph to create a robust ReAct agent.
* **System Prompt (State Modifier):** The agent is bound by strict rules: it must prioritize current academic year data, use the search tool to verify facts, and decline non-educational queries.
* **Streaming:** Responses are streamed using `stream_mode="values"` to provide real-time UI updates (e.g., "🎓 Researching and compiling...").

### Conversational Memory: `MemorySaver`
To allow users to ask follow-up questions (e.g., "What about their MBA program instead?"), the app integrates LangGraph's `MemorySaver`.
* A unique `uuid` is generated per user session and passed to the agent's configuration.
* The checkpointer saves the exact state of the graph after every interaction, ensuring the LLM has full context of previous messages.

### Live Web Search: Tavily API
The bot uses `TavilySearchResults` to combat LLM hallucinations and outdated training data.
* **Configuration:** Configured with `search_depth="advanced"` and a recent `start_date` parameter to prioritize the most up-to-date university portals and admission bulletins.

---

## 3. Project File Structure

```text
University_Admission_Bot/
│
├── .streamlit/
│   ├── config.toml         # Streamlit theme and server configurations
│   └── secrets.toml        # (Ignored in Git) Stores API keys securely
│
├── app.py                  # Main application logic and UI code
├── requirements.txt        # Python package dependencies
├── README.md               # Setup instructions and project overview
└── DOCUMENTATION.md        # Technical breakdown and architecture
```

---

## 4. UI Design & Custom Styling

The frontend heavily utilizes Streamlit's `st.markdown(unsafe_allow_html=True)` to inject custom CSS, transforming the default Streamlit layout into a vibrant, student-friendly interface.

* **Dynamic Chat Input:** The search bar features a custom CSS wrapper that transitions from a vibrant green border to a glowing coral pink upon focus.
* **Animated Elements:** Unordered lists (`<ul>`) are styled as "cards" with a hover effect (`transform: translateY(-5px)`) to make reading dense requirements more engaging.
* **HTML Structuring:** The LLM is strictly instructed to output responses using `<h3>`, `<ul>`, and `<b>` tags, which hook directly into the custom CSS framework.

---

## 5. Future Roadmap

Potential enhancements for future iterations of the bot:

* **Export Functionality:** Allow users to download their admission summaries as a structured PDF report.
* **Multi-Agent Setup:** Introduce specialized sub-agents (e.g., a "Financial Aid Agent" or "Visa/Immigration Agent" for international students).
* **Persistent Database:** Replace the in-memory `MemorySaver` with a PostgreSQL or Firebase backend to save user chat histories across different browser sessions.

---

**Author:** Vedant Parkhe

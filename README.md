# 🎓 University Admissions Bot

An intelligent, AI-powered conversational agent designed to help students quickly navigate the complex college application process. This bot actively searches the web to provide the most up-to-date information on application deadlines, eligibility requirements, fee structures, and entrance exams for the current academic year.

**[🚀 Try the Live Demo Here!](https://universityadmissionbot-vedantparkhe77.streamlit.app/)**

## ✨ Features

* **Real-Time Web Search:** Utilizes the Tavily Search API to scrape current, official university guidelines rather than relying on static or outdated training data.
* **Conversational Memory:** Powered by LangGraph's `MemorySaver`, allowing the bot to remember the context of the conversation across multiple messages.
* **Structured Output:** Delivers comprehensive, easy-to-read responses formatted with clean HTML and vibrant custom CSS styling.
* **Interactive UI:** Built with Streamlit, featuring a user-friendly chat interface with custom animations and dynamic visual states.

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **LLM Engine:** Google Gemini (`gemini-2.5-flash` via `langchain-google-genai`)
* **Agent Framework:** LangGraph (`create_react_agent`)
* **Search Tool:** Tavily Search API

## 🚀 Getting Started

Follow these steps to run the application on your local machine or deploy it live to the web.

### 1. Clone the Repository
```bash
git clone https://github.com/vedantparkhe777-alt/University_Admission_Bot.git
cd University_Admission_Bot
```

### 2. Install Dependencies

Ensure you have Python installed, then install the required libraries:

```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys (CRITICAL STEP)

This bot requires two free API keys to function:

1. **Google API Key:** Powers the Gemini AI engine. (Available at [Google AI Studio](https://aistudio.google.com/))
2. **Tavily API Key:** Powers the live web search. (Available at [Tavily](https://tavily.com/))

#### Option A: Running Locally on Your Computer

Create a file `secrets.toml` inside `.streamlit` folder inside your project directory :

```bash
mkdir .streamlit
touch .streamlit/secrets.toml
```

Open `.streamlit/secrets.toml` and paste your keys in this **exact TOML format** (including the quotation marks):

```toml
GOOGLE_API_KEY = "your_google_api_key"
TAVILY_API_KEY = "your_tavily_api_key"

```

#### Option B: Deploying to Streamlit Community Cloud

Do **not** upload your `.streamlit/secrets.toml` file to GitHub. Instead, use Streamlit's built-in secure dashboard:

1. Go to your Streamlit App Dashboard.
2. Click the three dots (`⋮`) next to your app and select **Settings**.
3. Go to the **Secrets** tab on the left menu.
4. Paste the exact same TOML code block from Option A directly into the text box.
5. Click **Save**.


### 4. Run the Application

Start the Streamlit server locally:

```bash
streamlit run app.py
```

## 👨‍💻 Author

**Vedant Parkhe**

* Student & Developer
* [GitHub](https://github.com/vedantparkhe777-alt)
* [LinkedIn](https://www.linkedin.com/in/vedant-parkhe-634b27310)

---

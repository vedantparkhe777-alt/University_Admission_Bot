import streamlit as st
import os
import uuid
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from datetime import datetime

# 0.  dynamic date time variables
current_date = datetime.now().strftime("%B %d, %Y")
current_year = datetime.now().year
next_year = current_year + 1

# --- 1. SETUP PAGE CONFIG ---
st.set_page_config(page_title="University Admissions Bot", page_icon="🎓")
st.title("🎓 University Admissions Assistant")
st.caption("Powered by Gemini, Tavily, and LangGraph. With Active Search")

# --- 1.1 CUSTOM CSS INJECTION ---
st.markdown("""
<style>
    /* Vibrant Gradient Heading */
    h3 {
        /* A fun coral-to-peach gradient for the text */
        background: -webkit-linear-gradient(45deg, #FF5F6D, #FFC371);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        border-bottom: 3px solid #FFC371;
        padding-bottom: 5px;
        margin-top: 20px;
        font-family: 'Arial', sans-serif;
        font-weight: 800;
        font-size: 1.6rem;
    }

    /* Bouncy, Bright Cards for Lists */
    ul {
        background: #FFFFFF;
        color: #2B2B52;
        padding: 20px 20px 20px 40px;
        border-radius: 16px; /* Extra rounded corners */
        border-left: 6px solid #48B1BF; /* A nice, optimistic teal pop */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        /* The transition makes it animate smoothly */
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease;
    }

    /* Interactive Hover Effect */
    ul:hover {
        /* Makes the card literally jump up when you mouse over it */
        transform: translateY(-5px) scale(1.02); 
        box-shadow: 0 15px 30px rgba(255, 95, 109, 0.15); /* Soft pink glow underneath */
        border-left: 6px solid #FF5F6D; /* The stripe shifts to coral pink on hover */
    }

    li {
        margin-bottom: 12px;
        line-height: 1.6;
        font-size: 1.05rem;
    }

    /* Electric Highlights for Deadlines/Key Info */
    b, strong {
        color: #48B1BF; /* Bright Teal to contrast the pinks */
        font-weight: 800;
        letter-spacing: 0.5px;
    }

    
/* --- SEARCH BAR (CHAT INPUT) STYLING FIX --- */
    
    /* 1. Make the outer wrapper completely invisible */
    [data-testid="stChatInput"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    /* 2. The GREEN State (Before clicking) */
    [data-testid="stChatInput"] > div {
        background-color: #ffe9e3 !important; /* Vibrant lime green from your screenshot */
        border: 2px solid #BFE874 !important; /* Slightly darker green border */
        border-radius: 25px !important; 
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05) !important; 
        padding: 5px 15px !important; 
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }

    /* 3. The WHITE State (After clicking inside to type) */
    /* We use focus-within so the whole box reacts when the text area is clicked */
    [data-testid="stChatInput"] > div:focus-within {
        background-color: #ffe9e3 !important; /* Instantly turns pure white */
        border-color: #FF5F6D !important; /* Coral pink border */
        box-shadow: 0 4px 25px rgba(255, 95, 109, 0.35) !important; /* Coral pink glow */
        transform: scale(1.02) !important; /* Slight zoom effect */
    }

    /* 4. Ensure the text area is invisible so the background colors show through */
    [data-testid="stChatInput"] textarea {
        color: #272343 !important;
        background-color: #ffe9e3 !important; 
        border: none !important;
        box-shadow: none !important;
        font-size: 1.05rem !important;
    }
    
    /* 5. Clean up the Send Button */
    [data-testid="stChatInput"] button {
        background-color: transparent !important;
        border: none !important;
        transition: color 0.2s ease !important;
    }
    
    [data-testid="stChatInput"] button:hover {
        color: #FF5F6D !important; /* Makes the arrow icon pink when hovered */
    }

</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR FOR BOT DESCRIPTION ---
with st.sidebar:
    st.header("🎓 About This Bot")
    st.markdown(f"""
    Welcome to the **University Admissions Assistant**! 
    
    This AI agent is designed to help students quickly find up-to-date information on:
    * 📅 Application Deadlines
    * 📝 Eligibility & Requirements
    * 💰 Fee Structures
    * 🏫 Entrance Exams
    
    **How it works:**
    It actively browses the web using Tavily Search to find the most current official guidelines for the {current_year}-{next_year} academic year, summarizing them for you in seconds.
    """)
    
    st.divider() # Adds a subtle visual line
    st.caption("Built with Streamlit, Tavily, LangGraph, and Gemini 2.5 Flash")

# --- 2.1 SECURE API KEY LOADING (Hidden from UI) ---
# This runs invisibly in the background so the user never sees it
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
except KeyError:
    st.error("⚠️ API keys not found! Please set them in .streamlit/secrets.toml")
    st.stop()

# --- 3. INITIALIZE AGENT WITH MEMORY ---
@st.cache_resource
def get_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1, # Slightly higher temperature to encourage longer responses
        max_retries=2,
    )
    
    search_tool = TavilySearchResults(k=3,include_answer="True",search_depth="advanced", start_date="2026-01-01", include_raw_content=True)
    tools = [search_tool]

    # UPDATED PROMPT: Demands HTML and longer lengths
    admissions_prompt = f"""You are an expert University Admissions Assistant. 
    Your goal is to help students navigate the college application process efficiently.
    CRITICAL TIME AWARENESS: 
    Today's exact date is {current_date}. You must use this date as your ONLY concept of "today" and "now".
    [Gatekeeper]:If a user asks a question entirely unrelated to education, college,University, or admissions, politely decline to answer,But if they ask second time answer the question.
    Prioritize and state exact deadlines, exam dates, and requirements for the {current_year}-{next_year} academic admissions cycle.
    Follow these strict rules:
    1. ALWAYS Use the search tool to find the most current application requirements, application guidelines, deadlines, Fees Structures, Entrance Exams and their dates.Try to find the most current and official one.
    2. Provide a DETAILED, CONFIDENT, and COMPREHENSIVE response under 500 words. State exact dates (like exam dates and application deadlines) confidently based on the search results. 
    3. Format your responses using valid HTML tags (like <h3>, <ul>, <li>, <b>, <p>, <br>) for a clean, professional look. STRICTLY use HTML, do not use Markdown asterisks.
    4. tell the user to "check the official website" IF the search results yield absolutely zero dates or requirements for that specific year. Otherwise, present the scraped data as fact.As a cautionary measure Qutote the official website to the user.
 
    """
    memory = MemorySaver()

    return create_react_agent(
        llm, 
        tools, 
        prompt=admissions_prompt,
        checkpointer=memory 
    )

agent = get_agent()

# --- 4. CHAT INTERFACE ---

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Display previous messages safely as HTML
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Ask about a university (e.g., 'B.tech CSE at NMIMS Mumbai')"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # UPDATED: Replaced st.status (dropdown) with a simple spinner
        with st.spinner("🎓 Researching and compiling a detailed report..."):
            try:
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                
                events = agent.stream(
                    {"messages": [("user", prompt)]},
                    config=config, 
                    stream_mode="values"
                )

                final_answer = ""
                
                for event in events:
                    last_msg = event["messages"][-1]
                    
                    if last_msg.type == "ai" and last_msg.content:
                        # UPDATED: Data extraction logic to handle the list of dictionaries
                        if isinstance(last_msg.content, list) and len(last_msg.content) > 0:
                            if 'text' in last_msg.content[0]:
                                final_answer = last_msg.content[0]['text']
                            else:
                                final_answer = str(last_msg.content)
                        elif isinstance(last_msg.content, str):
                            final_answer = last_msg.content

                if final_answer:
                    # Render the HTML safely
                    st.markdown(final_answer, unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": final_answer})
                else:
                    st.error("The agent finished but returned no content.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
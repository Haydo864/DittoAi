import streamlit as st
import requests
import google.generativeai as genai
from duckduckgo_search import DDGS
# ==========================================
# 1. DEFINE YOUR AGENT'S TOOLS
# ==========================================

def get_pokemon_info(pokemon_name: str) -> dict:
    """Fetches comprehensive data including types, abilities, and base stats for a specific Pokémon."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower().strip()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # 1. Loop through the stats array and pull out the name and value for each one
        base_stats = {}
        for stat in data["stats"]:
            stat_name = stat["stat"]["name"]
            stat_value = stat["base_stat"]
            base_stats[stat_name] = stat_value
            
        # 2. Return a much richer dictionary back to the AI
        return {
            "name": data["name"].capitalize(),
            "types": [t["type"]["name"] for t in data["types"]],
            "abilities": [a["ability"]["name"] for a in data["abilities"]],
            "height_meters": data["height"] / 10,  # PokéAPI gives height in decimeters
            "weight_kg": data["weight"] / 10,      # PokéAPI gives weight in hectograms
            "base_experience": data["base_experience"],
            "base_stats": base_stats               # This includes HP, Attack, Defense, Speed, etc.
        }
        
    return {"error": f"Could not find a Pokémon named '{pokemon_name}'. Check the spelling!"}

def get_wikipedia_summary(query: str) -> str:
    """Fetches a short summary of general knowledge, history, or science topics from Wikipedia."""
    url = f"https://pokemondb.net//api/rest_v1/page/summary/{query.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("extract", "No summary found.")
    return "Could not find information on that topic."

def search_the_web(query: str) -> str:
    """Searches the internet for current events, news, or general information. Use this if Wikipedia doesn't have the answer."""
    try:
        # Search DuckDuckGo and get the top 3 results
        results = DDGS().text(query, max_results=3)
        if not results:
            return "No results found on the web."
        
        # Format the results into a readable string for the AI
        formatted_results = "\n".join([f"- {res['title']}: {res['body']}" for res in results])
        return formatted_results
    except Exception as e:
        return f"An error occurred while searching: {e}"
# ==========================================
# 2. CONFIGURE THE AI
# ==========================================

# Pull the API key from Streamlit's secure secrets manager
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize the model and GIVE IT THE TOOLS. 
# gemini-1.5-flash is extremely fast and free-tier friendly.
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    tools=[get_pokemon_info, get_wikipedia_summary, search_the_web]
)

# Start a chat session that automatically handles the background tool-calling
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(enable_automatic_function_calling=True)

# Keep a clean log of messages for the UI
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 3. BUILD THE WEB INTERFACE
# ==========================================

st.set_page_config(page_title="DittoAi", page_icon="🤖")
st.title("Welcome to DittoAI")
st.markdown("Ask me anything about Pokemon!")

# Draw all past messages to the screen
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# The Chat Input Box
if prompt := st.chat_input("E.g., 'What is Charizard's ability?' or 'Who discovered electricity?'"):
    
    # 1. Display the user's prompt
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2. Send the prompt to the AI (it will use tools here if needed)
    with st.spinner("Ditto used think"):
        response = st.session_state.chat_session.send_message(prompt)
        
    # 3. Display the AI's final answer
    st.chat_message("assistant").write(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
import streamlit as st
import requests
import json
import os
from datetime import datetime
import re
from typing import List, Dict, Any

# Page configuration
st.set_page_config(
    page_title="MedBot - Medical Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .disclaimer-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .emergency-button {
        background-color: #e74c3c;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    
    .user-message {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border-left: 4px solid #2196f3;
    }
    
    .bot-message {
        background-color: #f1f8e9;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

class OpenRouterClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://streamlit.io",
            "X-Title": "Medical Chatbot"
        }
    
    def get_response(self, messages: List[Dict], model: str = "openai/gpt-3.5-turbo", temperature: float = 0.7) -> str:
        try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 1000
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error connecting to AI service: {str(e)}"

class MedicalChatbot:
    def __init__(self):
        self.system_prompt = """You are a helpful medical assistant chatbot. Your role is to:

1. Provide general health information and education
2. Help users understand symptoms and when to seek care
3. Offer wellness and prevention advice
4. Explain medical terms and procedures

IMPORTANT LIMITATIONS:
- You cannot diagnose medical conditions
- You cannot prescribe medications
- You cannot replace professional medical advice
- Always encourage users to consult healthcare providers for serious concerns

EMERGENCY SITUATIONS:
If a user describes severe symptoms like chest pain, difficulty breathing, severe bleeding, stroke symptoms, or suicidal thoughts, immediately advise them to call emergency services (911) or go to the nearest emergency room.

Be empathetic, informative, and always prioritize user safety. Ask clarifying questions when needed."""

    def is_emergency(self, message: str) -> bool:
        emergency_keywords = [
            "chest pain", "can't breathe", "difficulty breathing", "severe bleeding",
            "stroke", "heart attack", "suicide", "kill myself", "overdose",
            "severe headache", "unconscious", "seizure", "choking"
        ]
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in emergency_keywords)
    
    def get_emergency_response(self) -> str:
        return """🚨 **EMERGENCY ALERT** 🚨

Based on your message, this may be a medical emergency. Please:

1. **Call 911 immediately** or go to the nearest emergency room
2. If you're having thoughts of self-harm, call:
   - National Suicide Prevention Lifeline: 988
   - Crisis Text Line: Text HOME to 741741

This chatbot cannot handle emergency situations. Please seek immediate professional medical help.

Are you safe right now? If not, please contact emergency services immediately."""

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "age": None,
            "gender": None,
            "medical_conditions": [],
            "allergies": []
        }
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def main():
    # Initialize session state
    initialize_session_state()
    
    # Initialize chatbot
    chatbot = MedicalChatbot()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 MedBot - Your Medical Assistant</h1>
        <p>AI-powered health information and guidance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Medical Disclaimer
    st.markdown("""
    <div class="disclaimer-box">
        <h4>⚠️ Important Medical Disclaimer</h4>
        <p>This chatbot provides general health information only and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for medical concerns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Emergency Button
    if st.button("🚨 EMERGENCY - Get Help Now", key="emergency"):
        st.markdown("""
        <div class="emergency-button">
            🚨 For immediate medical emergencies, call 911<br>
            🔗 National Suicide Prevention Lifeline: 988<br>
            💬 Crisis Text Line: Text HOME to 741741
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Settings")
        
        # API Key Input
        api_key = st.text_input("OpenRouter API Key", type="password", help="Enter your OpenRouter API key")
        
        if not api_key:
            st.warning("Please enter your OpenRouter API key to start chatting.")
            st.info("Get your API key from: https://openrouter.ai/keys")
            return
        
        # Model Selection
        model_options = {
            "GPT-3.5 Turbo": "openai/gpt-3.5-turbo",
            "GPT-4": "openai/gpt-4",
            "Claude 3 Haiku": "anthropic/claude-3-haiku",
            "Claude 3 Sonnet": "anthropic/claude-3-sonnet"
        }
        
        selected_model_display = st.selectbox("Select AI Model", list(model_options.keys()))
        selected_model = model_options[selected_model_display]
        
        # Temperature
        temperature = st.slider("Response Creativity", 0.0, 1.0, 0.7, 0.1)
        
        st.header("👤 User Profile")
        
        # User Profile
        age = st.number_input("Age", min_value=0, max_value=120, value=st.session_state.user_profile.get("age", 0))
        gender = st.selectbox("Gender", ["Not specified", "Male", "Female", "Other"])
        
        st.session_state.user_profile["age"] = age if age > 0 else None
        st.session_state.user_profile["gender"] = gender if gender != "Not specified" else None
        
        # Quick Health Topics
        st.header("🔗 Quick Topics")
        quick_topics = [
            "General health checkup advice",
            "Symptoms of common cold",
            "When to see a doctor",
            "Healthy diet tips",
            "Exercise recommendations",
            "Stress management"
        ]
        
        for topic in quick_topics:
            if st.button(topic, key=f"topic_{topic}"):
                st.session_state.messages.append({"role": "user", "content": topic})
                st.rerun()
        
        # Clear Chat
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()
    
    # Main Chat Interface
    st.header("💬 Chat with MedBot")
    
    # Initialize OpenRouter client
    client = OpenRouterClient(api_key)
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bot-message">
                    <strong>MedBot:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask me about your health concerns...")
    
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Check for emergency
        if chatbot.is_emergency(user_input):
            emergency_response = chatbot.get_emergency_response()
            st.session_state.messages.append({"role": "assistant", "content": emergency_response})
        else:
            # Prepare messages for API
            api_messages = [{"role": "system", "content": chatbot.system_prompt}]
            
            # Add user profile context if available
            if st.session_state.user_profile["age"] or st.session_state.user_profile["gender"]:
                profile_context = f"User profile: Age: {st.session_state.user_profile.get('age', 'Not specified')}, Gender: {st.session_state.user_profile.get('gender', 'Not specified')}"
                api_messages.append({"role": "system", "content": profile_context})
            
            # Add conversation history
            api_messages.extend(st.session_state.messages)
            
            # Get AI response
            with st.spinner("MedBot is thinking..."):
                response = client.get_response(api_messages, selected_model, temperature)
                st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Save to chat history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.chat_history.append({
            "timestamp": timestamp,
            "user": user_input,
            "bot": st.session_state.messages[-1]["content"]
        })
        
        st.rerun()
    
    # Chat History Export
    if st.session_state.chat_history:
        st.header("📋 Export Chat History")
        if st.button("Download Chat History"):
            chat_text = "MedBot Chat History\n" + "="*50 + "\n\n"
            for chat in st.session_state.chat_history:
                chat_text += f"[{chat['timestamp']}]\n"
                chat_text += f"You: {chat['user']}\n"
                chat_text += f"MedBot: {chat['bot']}\n"
                chat_text += "-"*30 + "\n\n"
            
            st.download_button(
                label="💾 Download as Text File",
                data=chat_text,
                file_name=f"medbot_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
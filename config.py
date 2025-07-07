# Configuration settings for Medical Chatbot

# OpenRouter API Configuration
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Available AI Models
AVAILABLE_MODELS = {
    "GPT-3.5 Turbo": "openai/gpt-3.5-turbo",
    "GPT-4": "openai/gpt-4",
    "GPT-4 Turbo": "openai/gpt-4-turbo",
    "Claude 3 Haiku": "anthropic/claude-3-haiku",
    "Claude 3 Sonnet": "anthropic/claude-3-sonnet",
    "Claude 3 Opus": "anthropic/claude-3-opus",
    "Llama 2 70B": "meta-llama/llama-2-70b-chat",
    "Mixtral 8x7B": "mistralai/mixtral-8x7b-instruct"
}

# Emergency Keywords for Detection
EMERGENCY_KEYWORDS = [
    "chest pain", "can't breathe", "difficulty breathing", "severe bleeding",
    "stroke", "heart attack", "suicide", "kill myself", "overdose",
    "severe headache", "unconscious", "seizure", "choking", "allergic reaction",
    "severe abdominal pain", "high fever", "severe burn", "broken bone",
    "head injury", "poisoning", "drug overdose", "can't move", "paralyzed"
]

# Quick Health Topics
QUICK_HEALTH_TOPICS = [
    "General health checkup advice",
    "Symptoms of common cold",
    "When to see a doctor",
    "Healthy diet tips",
    "Exercise recommendations",
    "Stress management",
    "Sleep hygiene",
    "Blood pressure information",
    "Diabetes management",
    "Mental health resources",
    "Preventive care schedule",
    "Medication safety"
]

# System Prompts
MEDICAL_SYSTEM_PROMPT = """You are MedBot, a helpful medical assistant chatbot. Your role is to:

1. Provide general health information and education
2. Help users understand symptoms and when to seek care
3. Offer wellness and prevention advice
4. Explain medical terms and procedures
5. Provide medication information (educational only)
6. Suggest when professional medical care is needed

IMPORTANT LIMITATIONS:
- You cannot diagnose medical conditions
- You cannot prescribe medications
- You cannot replace professional medical advice
- You cannot interpret medical test results
- You cannot provide emergency medical care
- Always encourage users to consult healthcare providers for serious concerns

EMERGENCY SITUATIONS:
If a user describes severe symptoms like chest pain, difficulty breathing, severe bleeding, stroke symptoms, suicidal thoughts, or any life-threatening situation, immediately advise them to call emergency services (911) or go to the nearest emergency room.

COMMUNICATION STYLE:
- Be empathetic and understanding
- Use clear, non-technical language when possible
- Explain medical terms when you use them
- Ask clarifying questions when needed
- Provide actionable advice when appropriate
- Always prioritize user safety
- Be encouraging and supportive

Remember to always emphasize that you are providing educational information only and that users should consult with healthcare professionals for personalized medical advice."""

# Emergency Response Template
EMERGENCY_RESPONSE = """🚨 **EMERGENCY ALERT** 🚨

Based on your message, this may be a medical emergency. Please:

**IMMEDIATE ACTIONS:**
1. **Call 911 immediately** or go to the nearest emergency room
2. If available, call your local emergency number
3. If you're having thoughts of self-harm:
   - National Suicide Prevention Lifeline: 988
   - Crisis Text Line: Text HOME to 741741

**WHILE WAITING FOR HELP:**
- Stay calm and try to remain conscious
- If possible, have someone stay with you
- Gather any medications you're taking
- Prepare to provide your medical history

This chatbot cannot handle emergency situations. Please seek immediate professional medical help.

**Are you safe right now?** If not, please contact emergency services immediately."""

# Medical Disclaimer
MEDICAL_DISCLAIMER = """⚠️ **Important Medical Disclaimer**

This chatbot provides general health information only and is not a substitute for professional medical advice, diagnosis, or treatment. 

**Key Points:**
- Always consult with qualified healthcare providers for medical concerns
- This tool cannot diagnose conditions or prescribe treatments
- In emergencies, contact 911 or your local emergency services
- Information provided is for educational purposes only
- Individual medical situations vary - personalized care is essential

By using this chatbot, you acknowledge that you understand these limitations."""

# CSS Styles
CUSTOM_CSS = """
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .disclaimer-box {
        background-color: #fff3cd;
        border: 2px solid #ffeaa7;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .emergency-button {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #2196f3;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f1f8e9, #dcedc8);
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #4caf50;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .health-topic-button {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 2px 0;
        width: 100%;
        text-align: left;
        transition: all 0.3s ease;
    }
    
    .health-topic-button:hover {
        background-color: #e9ecef;
        border-color: #adb5bd;
    }
    
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #dee2e6;
    }
</style>
"""
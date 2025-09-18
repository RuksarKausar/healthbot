from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # Added CORS import
import uvicorn
import os
from datetime import datetime

app = FastAPI(title="Healthcare Chatbot API", version="1.0.0")

# Add CORS middleware - This fixes the connection error!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (websites) to call your API
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Healthcare knowledge base (lightweight)
HEALTH_RESPONSES = {
    "fever": {
        "en": "🌡️ **Fever Management:**\n• Rest and drink plenty of fluids\n• Take paracetamol as directed\n• See doctor if >101.3°F for >3 days\n⚠️ Emergency if breathing difficulty",
        "hi": "🌡️ **बुखार का इलाज:**\n• आराम करें और पानी पिएं\n• डॉक्टर की सलाह से पैरासिटामोल लें\n• 101.3°F से अधिक व 3 दिन से ज्यादा हो तो डॉक्टर को दिखाएं"
    },
    "vaccine": {
        "en": "💉 **Vaccination Schedule:**\n👶 Birth: BCG, Hepatitis B\n🍼 6 weeks: DPT-1, OPV-1\n📍 10 weeks: DPT-2, OPV-2\n🎯 14 weeks: DPT-3, OPV-3\n🏥 Find centers: Call 1075",
        "hi": "💉 **टीकाकरण कार्यक्रम:**\n👶 जन्म: BCG, हेपेटाइटिस B\n🍼 6 सप्ताह: DPT-1, OPV-1\n📍 10 सप्ताह: DPT-2, OPV-2\n🎯 14 सप्ताह: DPT-3, OPV-3\n🏥 केंद्र खोजें: 1075 पर कॉल करें"
    },
    "emergency": {
        "en": "🚨 **EMERGENCY - Call NOW:**\n📞 Ambulance: 102, 108\n🏥 For: Chest pain, breathing problems, severe bleeding\n⚠️ Don't wait - get help immediately!",
        "hi": "🚨 **आपातकाल - तुरंत कॉल करें:**\n📞 एम्बुलेंस: 102, 108\n🏥 के लिए: सीने में दर्द, सांस की तकलीफ, तेज खून बहना\n⚠️ इंतजार न करें - तुरंत मदद लें!"
    }
}

def detect_language(text):
    """Simple language detection"""
    hindi_chars = ['है', 'का', 'की', 'के', 'में', 'से', 'को', 'बुखार', 'दर्द', 'टीका']
    return 'hi' if any(char in text for char in hindi_chars) else 'en'

def get_health_response(message):
    """Get appropriate health response"""
    message_lower = message.lower()
    language = detect_language(message)
    
    # Symptom detection
    if any(word in message_lower for word in ['fever', 'बुखार', 'temperature']):
        return HEALTH_RESPONSES["fever"][language]
    
    elif any(word in message_lower for word in ['vaccine', 'vaccination', 'टीका', 'टीकाकरण']):
        return HEALTH_RESPONSES["vaccine"][language]
    
    elif any(word in message_lower for word in ['emergency', 'urgent', 'आपातकाल', 'chest pain']):
        return HEALTH_RESPONSES["emergency"][language]
    
    elif any(word in message_lower for word in ['headache', 'सिर दर्द', 'head pain']):
        return "💊 For headache: Rest in dark room, drink water, apply cold compress. See doctor if severe." if language == 'en' else "💊 सिर दर्द के लिए: अंधेरे कमरे में आराम करें, पानी पिएं, ठंडी पट्टी लगाएं।"
    
    elif any(word in message_lower for word in ['cough', 'खांसी']):
        return "😷 For cough: Warm liquids, honey, avoid cold. See doctor if persistent." if language == 'en' else "😷 खांसी के लिए: गर्म तरल, शहद लें, ठंडा न खाएं। लगातार खांसी हो तो डॉक्टर को दिखाएं।"
    
    # Default response
    if language == 'hi':
        return "नमस्ते! मैं आपका स्वास्थ्य सहायक हूं। मैं बुखार, सिर दर्द, खांसी और टीकाकरण के बारे में मदद कर सकता हूं।"
    else:
        return "Hello! I'm your healthcare assistant. I can help with fever, headaches, cough, and vaccination information."

@app.get("/")
async def root():
    return {
        "message": "Healthcare Chatbot API is running! 🏥",
        "version": "1.0.0",
        "features": ["Multilingual Support", "Symptom Checking", "Vaccination Info", "Emergency Guidance"],
        "endpoints": ["/", "/webhook", "/health"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/webhook")
async def webhook(request: Request):
    """Handle incoming health queries"""
    try:
        body = await request.json()
        user_message = body.get("message", "Hello")
        
        # Get appropriate response
        bot_response = get_health_response(user_message)
        
        # Log interaction (simple)
        print(f"📊 User: {user_message} | Bot: {bot_response[:50]}...")
        
        return {
            "status": "success",
            "user_message": user_message,
            "bot_response": bot_response,
            "language": detect_language(user_message),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

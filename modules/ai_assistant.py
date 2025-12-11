try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

class AIAssistant:
    def __init__(self, config):
        """Initialize AI Assistant / AI Assistant shuru karein"""
        self.config = config
        self.api_key = config.get('ai', {}).get('api_key', '')
        self.model_name = config.get('ai', {}).get('model', 'gpt-3.5-turbo')
        self.provider = config.get('ai', {}).get('provider', 'openai')
        self.client = None
        
        if self.provider == 'google':
             if not GOOGLE_AVAILABLE:
                 print("⚠️ Google GenAI not available - Install 'google-generativeai'")
                 return
             if self.api_key and self.api_key != 'YOUR_OPENAI_API_KEY':
                 try:
                     genai.configure(api_key=self.api_key)
                     self.model = genai.GenerativeModel('gemini-pro')
                     self.client = True # Mark as active
                     print("✅ Google Gemini Initialized")
                 except Exception as e:
                     print(f"Google AI error: {e}")
        
        elif self.provider == 'openai':
            if not OPENAI_AVAILABLE:
                print("⚠️ OpenAI not available - AI Assistant disabled")
                return
            
            if self.api_key and self.api_key != 'YOUR_OPENAI_API_KEY':
                try:
                    openai.api_key = self.api_key
                    self.client = openai
                    print("✅ OpenAI Initialized")
                except Exception as e:
                    print(f"AI Assistant initialization error: {e}")
    
    def process_query(self, query):
        """Process a user query / User ka sawal hal karein"""
        if not self.client:
            return "AI Assistant not configured. Please add your API key."
        
        try:
            if self.provider == 'google':
                 # System Prompt for Richard Persona / Richard ka kirdaar
                 system_prompt = (
                     "You are Richard, a helpful smart mirror assistant. "
                     "Answer directly and naturally. "
                     "Do NOT say 'The AI says' or 'Here is the response'. "
                     "Be concise."
                 )
                 full_prompt = f"{system_prompt}\nUser: {query}\nRichard:"
                 
                 response = self.model.generate_content(full_prompt)
                 return response.text
                 
            elif self.provider == 'openai':
                response = self.client.ChatCompletion.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful smart mirror assistant."},
                        {"role": "user", "content": query}
                    ],
                    max_tokens=150
                )
                return response.choices[0].message.content
                
            elif self.provider == 'ollama':
                import requests
                import json
                
                url = self.config.get('ai', {}).get('api_url', 'http://localhost:11434/api/generate')
                # Use model from config, default to llama3 as requested
                model = self.config.get('ai', {}).get('model', 'llama3') 
                
                # System Prompt for Richard Persona (Ollama)
                system_prompt = "You are Richard, a concise helpful assistant. Answer directly in first person and never say 'AI response'."
                
                # Construct payload as per user snippet
                payload = {
                    "model": model,
                    "prompt": f"System: {system_prompt}\nUser: {query}\nAssistant:",
                    "stream": False, # Ensure non-streaming for simple parsing
                    "max_tokens": 512,
                    "temperature": 0.2
                }
                
                try:
                    response = requests.post(url, json=payload, timeout=60)
                    response.raise_for_status()
                    data = response.json()
                    # Parse response as per user snippet (result or response or content)
                    return data.get("response", data.get("result", data.get("content", ""))).strip()
                except Exception as e:
                    return f"Ollama Connection Error: {e}"
        except Exception as e:
            return f"Error: {str(e)}"


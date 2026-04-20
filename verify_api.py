
import os
import sys

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

try:
    from dotenv import load_dotenv
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    # Load .env from backend directory
    env_path = os.path.join(os.getcwd(), 'backend', '.env')
    print(f"Loading .env from: {env_path}")
    load_dotenv(env_path)
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        print("ERROR: GEMINI_API_KEY is missing or is still a placeholder in backend/.env")
        sys.exit(1)
        
    print(f"Testing API Key: {api_key[:10]}...{api_key[-5:]}")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.3
    )
    
    print("Sending test request to Gemini...")
    response = llm.invoke("Hello, say 'API IS WORKING'")
    print(f"Response: {response.content}")
    
    if "API IS WORKING" in response.content.upper():
        print("\nSUCCESS: Your Gemini API key is working perfectly!")
    else:
        print(f"\nWARNING: API returned unexpected content: {response.content}")

except Exception as e:
    print(f"\nERROR: API Key test failed!")
    print(f"Details: {str(e)}")

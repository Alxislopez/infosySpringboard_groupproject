import os
import json
import pandas as pd

try:
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

def get_market_summary(industry="Technology", budget=0):
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not LLM_AVAILABLE or not api_key or api_key == "your_groq_api_key_here":
        return _mock_market_summary()
        
    try:
        llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.2)
        prompt = ChatPromptTemplate.from_template(
            "You are a top-tier market research analyst. Estimate realistic market metrics for a new startup in the '{industry}' industry with an initial budget of ${budget}.\n"
            "Return ONLY a valid JSON object with the following keys exactly (no markdown formatting, no code blocks, just raw JSON):\n"
            "{{\n"
            "  \"tam\": (float, Total Addressable Market in Billions),\n"
            "  \"sam\": (float, Serviceable Addressable Market in Millions),\n"
            "  \"som\": (float, Serviceable Obtainable Market in Millions),\n"
            "  \"market_growth\": (float, year-over-year percentage growth rate),\n"
            "  \"years\": [2020, 2021, 2022, 2023, 2024, 2025, 2026],\n"
            "  \"market_values\": [(7 floats representing the market size in Billions corresponding to the years, showing an upward trend)]\n"
            "}}"
        )
        res = (prompt | llm).invoke({"industry": industry, "budget": budget})
        
        content = res.content.strip()
        if content.startswith("```json"): content = content[7:-3].strip()
        elif content.startswith("```"): content = content[3:-3].strip()
        
        data = json.loads(content)
        
        # Validate keys exist
        required_keys = ["tam", "sam", "som", "market_growth", "years", "market_values"]
        for k in required_keys:
            if k not in data:
                return _mock_market_summary()
                
        return data
    except Exception as e:
        print(f"Error generating market summary: {e}")
        return _mock_market_summary()

def _mock_market_summary():
    return {
        "tam": 2.4,
        "sam": 0.85,
        "som": 0.012,
        "market_growth": 8.2,
        "years": [2020, 2021, 2022, 2023, 2024, 2025, 2026],
        "market_values": [120, 145, 175, 205, 245, 280, 320]
    }

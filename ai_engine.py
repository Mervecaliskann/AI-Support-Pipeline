
"""
AI SUPPORT SYSTEM - AI ENGINE
Author: Merve Caliskan
Description: This module leverages Large Language Models (LLM) via Groq Cloud API 
             to perform automated sentiment analysis, ticket categorization, 
             and priority assignment for incoming customer support queries.
Tech Stack: Groq (gpt-oss-120b), NLP, JSON Parsing.
"""

import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class SupportAI:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def analyze_message(self, user_message):
        prompt = f"""
        Analyze the following support message. 
        Return ONLY a JSON object with: 
        'category' (Technical, Billing, or General), 
        'sentiment' (Positive, Negative, or Neutral), 
        'priority' (1 to 5).

        Message: {user_message}
        """
        
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
            response_format={"type": "json_object"} # JSON dönmesi için zorluyoruz
        )
        
        return json.loads(response.choices[0].message.content)
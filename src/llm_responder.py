import os
from openai import OpenAI

def generate_dm_response(comment_text: str, fallback_message: str) -> str:
    """
    Generate a dynamic, LLM-powered response via OpenRouter.
    Falls back to `fallback_message` if the API call fails or times out.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return fallback_message

    # Initialize OpenAI client with OpenRouter's URL schema
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    system_prompt = (
        "You are a friendly, concise customer service assistant for a campus ID card printing service. "
        "A user has commented on our Instagram reel. Acknowledge their comment warmly in 1-2 short sentences "
        "and provide this link to submit their photo and details: https://campus-id.example.com. "
    )

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User's Comment: {comment_text}"}
            ],
            max_tokens=150,
            temperature=0.6,
            timeout=10 # Fail fast to prevent stalling the main Instagram polling thread
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM Generation Error: {e}. Falling back to default static message.")
        return fallback_message

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

    # OpenAI client with OpenRouter's URL schema
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    system_prompt = (
        "You are a friendly, concise assistant for our Instagram account. "
        "A user has commented on our reel. Acknowledge their comment warmly in 1-2 short sentences "
        f"and provide them with this exact link/message: '{fallback_message}'. "
    )
    
    # 8-Tier Free Model Fallback Waterfall (Ranked by speed/quality ratio)
    models = [
        "meta-llama/llama-3.3-70b-instruct:free",
        "openai/gpt-oss-120b:free",
        "qwen/qwen3-next-80b-a3b-instruct:free",
        "nvidia/nemotron-3-super-120b-a12b:free",
        "mistralai/mistral-small-3.1-24b-instruct:free",
        "arcee-ai/trinity-large-preview:free",
        "stepfun/step-3.5-flash:free",
        "meta-llama/llama-3-8b-instruct:free"
    ]

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User's Comment: {comment_text}"}
                ],
                max_tokens=150,
                temperature=0.6,
                timeout=10 # Fail fast to cleanly cycle down the waterfall
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[{model}] failed: {e}. Cascading...")
            continue
            
    print("All LLM models in waterfall failed. Firing native static message.")
    return fallback_message

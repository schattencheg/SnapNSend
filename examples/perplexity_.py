import os
from perplexity import Perplexity

API_KEY = os.environ.get("PERPLEXITY_API_KEY")

client = Perplexity(api_key=API_KEY)

resp = client.chat.completions.create(
    model="sonar",  # или sonar-pro / pplx-70b-online и т.п.
    messages=[
        {"role": "user", "content": "Протестируй, что API у меня жив."}
    ],
)

print(resp)

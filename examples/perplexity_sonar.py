from perplexity import Perplexity
import os

client = Perplexity(
    api_key=os.environ["PPLX_API_KEY"],  # or paste your key directly
)


N = 5  # how many images you want to keep

completion = client.chat.completions.create(
    model="sonar",             # or sonar-pro / another Sonar model
    return_images=True,        # this enables image results
    messages=[
        {"role": "user", "content": f"Show me at least {N} images of Mount Everest"}
    ],
)

print(completion)

# Depending on SDK version, adapt field access; this pattern is typical:
images = getattr(completion, "images", None) or []

# Take first N images
selected_images = images[:N]

for i, img in enumerate(selected_images, start=1):
    # Each item usually has at least a URL; inspect `img` to confirm names
    url = getattr(img, "url", None) or img.get("url") or img.get('image_url')
    print(f"Image #{i}: {url}")

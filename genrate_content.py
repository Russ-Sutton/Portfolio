import os
import pandas as pd
import openai
from dotenv import load_dotenv
import json

# Load environment variables (for API key)
load_dotenv()

# --- Configuration ---
# Get API key from environment variable
# Check if OPENAI_API_KEY is set, if not, try ANTHROPIC_API_KEY
if os.getenv("OPENAI_API_KEY"):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    MODEL_NAME = "gpt-3.5-turbo" # Or "gpt-4", "gpt-4o" for better quality
elif os.getenv("ANTHROPIC_API_KEY"):
    # If you decide to use Anthropic, you'd need to import anthropic and
    # initialize it differently. This example focuses on OpenAI first.
    # For Anthropic, you'd do:
    # import anthropic
    # client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    # MODEL_NAME = "claude-3-haiku-20240307" # Or "claude-3-opus-20240229"
    print("Anthropic API key found, but the current script is set up for OpenAI. "
          "Please adapt the API call for Anthropic or set OPENAI_API_KEY.")
    exit()
else:
    raise ValueError("No OPENAI_API_KEY or ANTHROPIC_API_KEY found in .env file.")

INPUT_CSV_FILE = 'books.csv'
OUTPUT_JSON_FILE = 'output_marketing_content.json'

# --- LLM Interaction Functions ---

def generate_blurb(book_info):
    prompt = f"""
    You are a professional book copywriter. Write a compelling, concise book blurb (max 150 words) for the following book:

    Title: {book_info['Title']}
    Author: {book_info['Author']}
    Genre: {book_info['Genre']}
    Key Themes: {book_info['Key Themes']}
    Target Audience: {book_info['Target Audience']}

    Focus on intrigue, the core conflict/journey, and what makes the book unique.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating blurb for {book_info['Title']}: {e}")
        return "Error generating blurb."

def generate_social_media_post(book_info, platform="Twitter"):
    prompt = f"""
    You are a social media manager for a book publisher. Write a short, engaging {platform} post (max 280 characters for Twitter, longer for Instagram) for the following book.
    Include emojis and relevant hashtags.

    Title: {book_info['Title']}
    Author: {book_info['Author']}
    Genre: {book_info['Genre']}
    Key Themes: {book_info['Key Themes']}
    Target Audience: {book_info['Target Audience']}

    Make it exciting and encourage clicks/engagement.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating social post for {book_info['Title']}: {e}")
        return "Error generating social post."

def generate_hashtags(book_info):
    prompt = f"""
    Suggest 5-7 highly relevant and popular hashtags for the following book:

    Title: {book_info['Title']}
    Genre: {book_info['Genre']}
    Key Themes: {book_info['Key Themes']}

    Provide them as a comma-separated list.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=60
        )
        return [tag.strip() for tag in response.choices[0].message.content.strip().split(',')]
    except Exception as e:
        print(f"Error generating hashtags for {book_info['Title']}: {e}")
        return []

# --- Main Script Logic ---
if __name__ == "__main__":
    if not os.path.exists(INPUT_CSV_FILE):
        print(f"Error: Input CSV file '{INPUT_CSV_FILE}' not found. "
              "Please create it or use 'example_books.csv' as a template.")
        exit()

    try:
        books_df = pd.read_csv(INPUT_CSV_FILE)
    except Exception as e:
        print(f"Error reading {INPUT_CSV_FILE}: {e}")
        exit()

    generated_content = []

    print(f"Processing {len(books_df)} books...")
    for index, row in books_df.iterrows():
        book_info = row.to_dict()
        print(f"Generating content for: {book_info['Title']} by {book_info['Author']}")

        blurb = generate_blurb(book_info)
        twitter_post = generate_social_media_post(book_info, "Twitter")
        instagram_post = generate_social_media_post(book_info, "Instagram (longer caption)")
        hashtags = generate_hashtags(book_info)

        generated_content.append({
            'Title': book_info['Title'],
            'Author': book_info['Author'],
            'Genre': book_info['Genre'],
            'Original Key Themes': book_info['Key Themes'],
            'Generated Blurb': blurb,
            'Generated Twitter Post': twitter_post,
            'Generated Instagram Post': instagram_post,
            'Suggested Hashtags': hashtags
        })
        print(f"  Content generated for {book_info['Title']}")

    # Save all generated content to a JSON file
    with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(generated_content, f, indent=4, ensure_ascii=False)

    print(f"\nContent generation complete! Output saved to '{OUTPUT_JSON_FILE}'")

Book Marketing Content Generator (AI-Powered)

This project demonstrates an AI-powered Python script designed to assist publishing and marketing teams in generating various promotional content for books. It takes structured book metadata as input and leverages large language models (LLMs) to produce engaging book blurbs, social media posts, and relevant hashtags.

Features

* **Book Blurb Generation:** Creates concise and compelling book descriptions suitable for online retailers or back-cover copy.
* **Social Media Post Creation:** Generates short, attention-grabbing posts tailored for platforms like Twitter or Instagram.
* **Hashtag Suggestion:** Identifies relevant hashtags to increase discoverability.
* **Structured Input/Output:** Processes book data from a CSV/JSON file and outputs generated content in an organized format.
* **API Integration:** Connects with the OpenAI API (or other LLM providers) for content generation.

How It Works

The script reads book details (Title, Author, Genre, Key Themes, Target Audience) from an input `books.csv` (or `books.json`) file. For each book, it constructs a series of targeted prompts for an LLM (e.g., OpenAI's GPT-3.5 or GPT-4). The LLM then generates the requested content, which is then compiled and saved.

Technologies Used

* **Python 3.x**
* **OpenAI Python Library** (or `anthropic` if using Claude)
* **`pandas`** (for CSV handling)
* **`json`** (for JSON handling)

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [Your GitHub Repo URL]
    cd book-marketing-generator
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install openai pandas python-dotenv
    ```
    *(Note: `python-dotenv` is good practice for managing API keys securely.)*

## ⚙️ Configuration

1.  Obtain an API key from [OpenAI](https://platform.openai.com/account/api-keys) (or your chosen LLM provider).
2.  Create a `.env` file in the root directory of the project and add your API key:
    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    ```
    *(If using Anthropic, it would be `ANTHROPIC_API_KEY="..."`)*

## 💡 Usage

1.  **Prepare your input data:**
    * Edit the `books.csv` (or `books.json`) file to include details for the books you want to generate content for. See `example_books.csv` for the expected format.

2.  **Run the script:**
    ```bash
    python generate_content.py
    ```

3.  **View the output:**
    * Generated content will be saved to `output_marketing_content.json` (or `output_marketing_content.csv`).

## 📁 Project Structure
├── .env # Environment variables (API key) 
├──


## 🤝 Contributing

Feel free to fork this repository, suggest improvements, or submit pull requests.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

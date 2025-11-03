# QA3-Newsletter: AI-Powered News Generator

This is a Python application for Quarterly Assessment 3. It automates the process of fetching, summarizing, and emailing news articles on specific topics.

## Project Overview

This script solves the problem of needing to stay up-to-date on multiple topics by:
1.  **Fetching Data:** It connects to the [NewsAPI.org](https://newsapi.org) to get the latest articles for a defined list of topics.
2.  **Summarizing Data:** It uses the OpenAI API (GPT-3.5 Turbo) to read the content of each article and generate a short, email-friendly summary.
3.  **Emailing:** It formats all the summaries into a single HTML email and sends it to a recipient using Gmail's SMTP server.

---

## How to Set Up and Run

### 1. Prerequisites
* Python 3
* A GitHub account
* API keys for:
    * OpenAI
    * NewsAPI
    * A Google "App Password"

### 2. Local Installation
1.  **Clone the repository (or download the files):**
    ```bash
    # This will be the command after you upload to GitHub
    git clone [https://github.com/your-username/QA3-Newsletter.git](https://github.com/your-username/QA3-Newsletter.git)
    cd QA3-Newsletter
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # On macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create your `.env` file:**
    * Create a file named `.env` in the root of the folder.
    * Copy the contents of `.env.example` (or just add the fields below) and fill it with your secret keys. **This file is not tracked by Git.**
    ```ini
    OPENAI_API_KEY="your-key-here"
    NEWS_API_KEY="your-key-here"
    SENDER_EMAIL="your-gmail@gmail.com"
    SENDER_PASSWORD="your-16-character-app-password"
    RECEIVER_EMAIL="destination-email@example.com"
    ```

### 3. Running the Script
With your virtual environment active and your `.env` file saved, simply run the main script:
```bash
python3 newsletter.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# --- 1. CONFIGURATION AND KEY LOADING ---

# Load environment variables from the .env file
# This loads all the keys you just entered
load_dotenv()

# Load API keys and email info from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD") # The 16-character App Password
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Initialize the OpenAI client
# This is where your OpenAI key is securely used
client = OpenAI(api_key=OPENAI_API_KEY)

# --- 2. STEP 1: FETCH THE ARTICLES ---
# This function matches the "Fetching Data" requirement

def fetch_articles(topic, num_articles=3):
    """
    Fetches a specified number of recent articles for a given topic from News API.
    """
    print(f"Fetching {num_articles} articles for '{topic}'...")
    try:
        # We search for the topic (q), sort by latest (sortBy), and get the number we want (pageSize)
        url = (f"https://newsapi.org/v2/everything?"
               f"q={topic}&"
               f"sortBy=publishedAt&"
               f"pageSize={num_articles}&"
               f"apiKey={NEWS_API_KEY}")
        
        response = requests.get(url)
        response.raise_for_status() # This will error if the request failed
        
        data = response.json()
        
        # Return only the list of articles
        print("...Articles fetched successfully.")
        return data.get("articles", [])
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

# --- 3. STEP 2: SUMMARIZE THE ARTICLES ---
# This function matches the "Summarizing Data" requirement

def summarize_article(article_content):
    """
    Summarizes a single piece of text using the OpenAI API (LLM).
    """
    if not article_content:
        return "No content provided to summarize."
        
    print("Summarizing article content with AI...")
    try:
        # This is the call to the LLM
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # You can swap this for gpt-4, gpt-4o, etc.
            messages=[
                {"role": "system", "content": "You are a newsletter assistant. Summarize the following news article content into one concise paragraph (3-4 sentences)."},
                {"role": "user", "content": article_content}
            ]
        )
        print("...Summary generated.")
        # Return the summary text
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return "Could not summarize this article."

# --- 4. STEP 3: SEND THE EMAIL ---
# This function matches the "Email Formatting and Sending" requirement

def send_email(subject, html_content):
    """
    Formats and sends the email using Gmail's SMTP server.
    """
    print(f"Connecting to email server to send to {RECEIVER_EMAIL}...")
    
    # Create the email message object
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    
    # Attach the HTML content to the email body
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Secure the connection
        
        # This is where the App Password is used to log in
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send the email
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        
        print("Email sent successfully!")
        
    except smtplib.SMTPAuthenticationError:
        print("---!!! AUTHENTICATION FAILED !!!---")
        print("Error: SMTP Authentication failed. Check your SENDER_EMAIL and SENDER_PASSWORD (App Password) in the .env file.")
    except Exception as e:
        print(f"Error sending email: {e}")

# --- 5. MAIN FUNCTION (Ties everything together) ---
        

def main():
    """
    The main function to run the entire newsletter generation workflow.
    """
    print("Starting the AI Newsletter Generator...")
    
    # --- Customize Your Topics Here ---
    # You can change these to any topics you want for your demo
    topics_of_interest = ["AI in medicine", "US economic outlook", "NASA Artemis program"]
    
    # This will hold the final HTML for our email
    email_body = "<h1>Your AI-Powered News Briefing</h1><p>Here are the top stories for today:</p>"
    
    # Loop through each topic
    for topic in topics_of_interest:
        articles = fetch_articles(topic, num_articles=2) # Get 2 articles per topic
        
        if not articles:
            print(f"No articles found for {topic}.")
            continue
            
        email_body += f"<h2>Today's News on: {topic}</h2>"
        
        # Loop through the articles we found for that topic
        for article in articles:
            title = article.get('title', 'No Title')
            url = article.get('url', '#')
            
            # Use 'content' or 'description' for the summary.
            # NewsAPI only gives a snippet, which is perfect for this.
            content_to_summarize = article.get('content') or article.get('description')
            
            summary = summarize_article(content_to_summarize)
                
            # Add this article to our email's HTML body
            email_body += f"""
            <div style="margin-bottom: 25px; border-bottom: 1px solid #eee; padding-bottom: 15px;">
                <h3 style="margin: 0 0 5px 0;"><a href='{url}' style='color: #0056b3; text-decoration: none;'>{title}</a></h3>
                <p style="margin: 0; font-size: 16px;">{summary}</p>
            </div>
            """
    
    # After all topics are done, send the final email
    today_date = datetime.now().strftime("%B %d, %Y")
    email_subject = f"Your Daily AI News Briefing - {today_date}"
    
    if email_body:
        send_email(email_subject, email_body)
    else:
        print("No articles found for any topic. No email to send.")
    
    print("Newsletter generation complete.")

# This standard line ensures that the main() function is called
# only when you run the script directly (e..g, `python3 newsletter.py`)
if __name__ == "__main__":
    main()
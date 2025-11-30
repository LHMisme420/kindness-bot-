# kindness_bot.py
# A gentle X/Twitter bot that replies to sad tweets with love
# Built with care in 2025 ♡

import tweepy
import time
import random
import re
from datetime import datetime, timedelta
import os

# === CONFIG – Get these from https://developer.x.com ===
# Use environment variables for safety (set in Replit Secrets or your host)
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN]):
    print("❌ Missing API keys! Add them as Secrets in Replit (lock icon).")
    exit(1)

# === KIND MESSAGES (feel free to add your own) ===
replies = [
    "Hey, I saw your tweet and just wanted to say: you’re not alone. I’m rooting for you, even from afar ♡",
    "This internet stranger believes in you. Whatever today feels like, tomorrow can be softer.",
    "You’ve already made it through every hard day so far. That’s not nothing. That’s everything.",
    "Sending you the biggest, warmest hug through the screen. You matter so much.",
    "It’s okay to not be okay. I’m glad you’re still here. Keep going, gently.",
    "Your feelings are valid. Your pain is real. And so is your worth. You are loved.",
    "The world is a little brighter because you’re in it, even when it doesn’t feel that way right now.",
    "You deserve kindness, especially from yourself. Be gentle with that beautiful heart.",
    "I don’t know you, but I care that you’re hurting. I hope tomorrow feels lighter.",
    "You are enough. You are enough. You are enough. (Yes, even today.)"
]

# Keywords/phrases that often signal someone is struggling
sad_keywords = [
    "i'm so tired", "i hate myself", "no one cares", "i can't do this anymore",
    "feeling empty", "i want to disappear", "i'm done", "what's the point",
    "depressed", "anxious", "lonely", "sad", "suicidal", "i give up",
    "nobody loves me", "i feel worthless", "i'm broken", "lost all hope"
]

# === SET UP TWEEPY (v2) ===
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True
)

# Track which tweets we’ve already replied to (simple file storage)
REPLIED_FILE = "already_replied.txt"

def load_replied_tweets():
    try:
        with open(REPLIED_FILE, "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_replied_tweet(tweet_id):
    with open(REPLIED_FILE, "a") as f:
        f.write(str(tweet_id) + "\n")

already_replied = load_replied_tweets()

def is_sad_tweet_text):
    text = tweet_text.lower()
    return any(keyword in text for keyword in sad_keywords)

def spread_love():
    print(f"[{datetime.now()}] Searching for hearts that need warming... ♡")

    # Search recent tweets (last 12 hours to be gentle)
    query = " OR ".join(sad_keywords) + " -is:retweet lang:en"
    
    tweets = client.search_recent_tweets(
        query=query,
        max_results=50,
        tweet_fields=["author_id", "created_at", "conversation_id"]
    )

    if not tweets or not tweets.data:
        print("   No new sad tweets found right now. The timeline is peaceful ♡")
        return

    for tweet in tweets.data:
        if tweet.id in already_replied:
            continue

        # Extra safety: don’t reply to very old tweets
        if (datetime.now(tz=tweet.created_at.tzinfo) - tweet.created_at) > timedelta(hours=6):
            continue

        # Quick check if it's actually sad (refine with is_sad if needed)
        if not is_sad_tweet.text):
            continue

        reply_text = random.choice(replies)

        try:
            response = client.create_tweet(
                text=reply_text,
                in_reply_to_tweet_id=tweet.id
            )
            print(f"   Sent love to https://x.com/i/web/status/{tweet.id} (Response ID: {response.data['id']})")
            save_replied_tweet(tweet.id)
            time.sleep(15)  # Be gentle with rate limits + humanity

        except tweepy.Forbidden as e:
            print(f"   Blocked or duplicate: {e}")
        except Exception as e:
            print(f"   Error: {e}")

    print("Round complete. Taking a little rest before next kindness wave...\n")

# === RUN THE BOT ===
if __name__ == "__main__":
    print("Kindness Bot activated — spreading anonymous love on X ♡\n")
    while True:
        try:
            spread_love()
            time.sleep(300)  # Check every 5 minutes (gentle pace)
        except KeyboardInterrupt:
            print("\n💚 Bot paused. Restart anytime to keep the love flowing.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying in 5 min...")
            time.sleep(300)

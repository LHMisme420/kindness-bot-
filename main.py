# main.py – works on Replit Autoscale + Reserved VM + normal Run button
import os
import threading
import time
import random
from datetime import datetime, timedelta
import tweepy
from flask import Flask   # ← tiny web server so Replit is happy

app = Flask(__name__)

@app.route("/")
def home():
    return "Kindness Bot is alive and spreading love ♡", 200

# ─────── Your kindness bot (unchanged) runs in background ───────
replies = [
    "Hey, I saw your tweet and just wanted to say: you’re not alone. I’m rooting for you, even from afar ♡",
    "This internet stranger believes in you. Whatever today feels like, tomorrow can be softer.",
    "You’ve already made it through every hard day so far. That’s everything.",
    "Sending you the biggest, warmest hug through the screen. You matter so much.",
    "It’s okay to not be okay. I’m glad you’re still here. Keep going, gently.",
    # (add the rest of the messages you like)
]

sad_keywords = ["i'm so tired", "i hate myself", "depressed", "lonely", "sad", "anxious", "i give up", "feeling empty"]

client = tweepy.Client(
    bearer_token=os.getenv("BEARER_TOKEN"),
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
    wait_on_rate_limit=True,
)

REPLIED_FILE = "replied.txt"
replied = set(open(REPLIED_FILE).read().splitlines() if os.path.exists(REPLIED_FILE) else [])

def bot_loop():
    while True:
        print(f"[{datetime.now()}] Searching for hearts that need warming... ♡")
        query = " OR ".join(sad_keywords) + " -is:retweet lang:en"
        tweets = client.search_recent_tweets(query=query, max_results=30, tweet_fields=["created_at"])
        if tweets.data:
            for tweet in tweets.data:
                if str(tweet.id) in replied or (datetime.utcnow() - tweet.created_at).total_seconds() > 21600:
                    continue
                msg = random.choice(replies)
                try:
                    client.create_tweet(text=msg, in_reply_to_tweet_id=tweet.id)
                    print(f"   Love sent → https://x.com/i/status/{tweet.id}")
                    replied.add(str(tweet.id))
                    with open(REPLIED_FILE, "a") as f:
                        f.write(str(tweet.id) + "\n")
                    time.sleep(20)
                except Exception as e:
                    print("   ", e)
        time.sleep(300)  # every 5 minutes

# Start the kindness bot in background
threading.Thread(target=bot_loop, daemon=True).start()

# Start Flask web server (keeps Replit alive)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

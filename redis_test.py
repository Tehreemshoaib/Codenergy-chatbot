import redis
import json

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# Clear our previous test conversation
r.delete("chat:user1")

# User message
user_message = {
    "role": "user",
    "content": "What services do you provide?"
}

# Bot message
bot_message = {
    "role": "assistant",
    "content": "We provide Development, SEO, Marketing, and Technical Support."
}

# Store messages in Redis
r.rpush("chat:user1", json.dumps(user_message))
r.rpush("chat:user1", json.dumps(bot_message))

# Retrieve conversation
messages = r.lrange("chat:user1", 0, -1)

# Convert JSON strings back into Python dictionaries
for message in messages:
    print(json.loads(message))
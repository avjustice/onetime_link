import redis

conn = redis.Redis(host='localhost', port=6379, decode_responses=True)

import redis

redis_pool = redis.ConnectionPool(host='localhost', port=6379)
  
async def get_redis_connection():
    """Get a connection from the pool."""
    return redis.StrictRedis(connection_pool=redis_pool)



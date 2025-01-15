import dramatiq
from dramatiq.brokers.redis import RedisBroker


redis_broker = RedisBroker(host="redis")
dramatiq.set_broker(redis_broker)



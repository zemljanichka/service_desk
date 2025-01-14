import dramatiq
from dramatiq.brokers.redis import RedisBroker


redis_broker = RedisBroker(host="localhost")
dramatiq.set_broker(redis_broker)



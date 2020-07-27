import redis


class Ops_log_redis(object):
    """ save ops log """

    def redis_conn(self, *args, **kwargs):
        conn = redis.Redis(host="10.6.85.178", port=6379, password="myRedis", decode_responses=True)
        return conn

    def lpush_insert(self, key, values, *args, **kwargs):
        conn = self.redis_conn()
        conn.set(key, values)
        return True

    def lpush_get(self, key, *args, **kwargs):
        conn = self.redis_conn()
        return conn.get(key)

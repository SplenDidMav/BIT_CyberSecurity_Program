import redis
redispool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.StrictRedis(redispool)
r.set('test', 'aaa')
print(r.get('test'))
x = 0
for x in range(0, 11):
    r.lpush('list', x)
    x = x + 1
print(r.lrange('list', '0', '10'))
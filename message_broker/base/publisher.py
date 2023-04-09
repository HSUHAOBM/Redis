import redis

# 建立 Redis 連線
r = redis.Redis(host='localhost', port=6379, db=0)

# 發布訊息
while True:
    message = input('請輸入訊息 (輸入 "stop" 中斷): ')

    # 發布訊息
    r.publish('example-channel', message)

    # 當收到中止訊息時中斷
    if message == 'stop':
        print('中止發布...')
        break
import redis
import time

# 建立 Redis 連線
r = redis.Redis(host='localhost', port=6379, db=0)

# 清空當前資料庫
# r.flushdb()

# 訂閱頻道
p = r.pubsub()
p.subscribe('example-channel')

# 監聽訊息
for message in p.listen():
    if message['type'] == 'message':
        data = message['data'].decode('utf-8') # bytes 轉成字串

        if data == 'stop': # 當收到中止訊息時中斷
            print('中止訂閱...')
            break
        print(data)

    # 降低 CPU 占用率
    time.sleep(0.001)
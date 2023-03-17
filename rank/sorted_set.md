

# redis-cli

新增 ZADD
```
ZADD user_scores 80 ABC123
ZADD user_scores 99999999 iamone
```

修改
即在新增一次
```
ZADD user_scores 987654321 iamone
```

增加 ABC123 , 10 分
分數可為負數
```
ZINCRBY user_scores 10 ABC123
```


全部對應的資料
```
ZRANGE user_scores 0 -1 WITHSCORES
```

查資料筆數 ZCARD
```
zcard user_scores
```

查分數 min~max 的數量 ZCOUNT
```
ZCOUNT user_scores 1 999999
```

查n筆
```
ZRANGE user_scores 0 -1 WITHSCORES
```

Zinterstore, test1 test2 2個有序集的交集
ZUNIONSTORE
```
ZINTERSTORE new_test 2 test1 test2
```

ZUNIONSTORE out 2 zset1 zset2 WEIGHTS 2 3
聯集權重並配合權重


找80~100分的 10名
```
ZRANGEBYSCORE user_scores 80 100 WITHSCORES LIMIT 0 10
81~100
ZRANGEBYSCORE user_scores (80 100 WITHSCORES LIMIT 0 10
```
大於80分
ZRANGEBYSCORE user_scores 80 +inf
ZRANGEBYSCORE user_scores -inf 80

Zlexcount 'b' ~ 'f'
```
ZLEXCOUNT myset [b [f
ZRANGEBYLEX myset [b [f
```


全部用戶排名
```
ZRANGE user_scores 0 -1 WITHSCORES  小到大
ZREVRANGE user_scores 0 -1 WITHSCORES 大到小
```
特定用戶的排名與分數
```
zscore user_scores iamone
zrevrank user_scores iamone 大到小
zrank user_scores iamone  小到大
```
逆排序  1000~200
```
ZREVRANGEBYSCORE user_scores 1000 200
ZREVRANGEBYSCORE user_scores 1000 200 WITHSCORES LIMIT 0 10
```
順排序 找80~100分的 10名
```
ZRANGEBYSCORE user_scores 80 100 WITHSCORES LIMIT 0 10
81~100
ZRANGEBYSCORE user_scores (80 100 WITHSCORES LIMIT 0 10
```
大於80分
```
ZRANGEBYSCORE user_scores 80 +inf
ZRANGEBYSCORE user_scores -inf 80
```

移除特定用戶
```
ZREM user_scores iamone.
```
移除第 0筆到 ~ 第 1筆資料
```
ZREMRANGEBYRANK user_scores 0 1
```
移除分數1500~3500的資料
```
ZREMRANGEBYSCORE user_scores 1500 3500
```

zscan 遍歷
```
ZSCAN user_scores 0 MATCH "R*"
ZSCAN user_scores 0 MATCH *8* COUNT 100
ZSCAN user_scores 0
```
```
while True:
    cursor, results = redis_client.zscan('my_sorted_set', cursor)
    for member, score in results:
        pass
    if cursor == 0:
        break
```
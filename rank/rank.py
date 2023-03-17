import redis
import random
import string

#  Redis DB
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# 隨機用户名
def generate_username():
    return ''.join(random.choice(string.ascii_letters) for i in range(10))

# 加入有序集合
def add_user_score(user_id, score):
    redis_client.zadd('user_scores', {user_id: score})

# 100 個假資料
for i in range(100):
    username = generate_username()
    score = random.randint(1, 10000)
    add_user_score(username, score)

# 排行榜 前 n 的數據
def get_top_users(n):
    print(f"Top {n} users:")

    user_scores = redis_client.zrevrange('user_scores', 0, n-1, withscores=True)
    top_users = []
    for user_id, score in user_scores:
        user_info = {'user_id': user_id.decode('utf-8'), 'score': score}
        top_users.append(user_info)
    return top_users

# 指定用戶的數據
def get_user_rank_and_score(user_id):
    rank = redis_client.zrevrank('user_scores', user_id)
    score = redis_client.zscore('user_scores', user_id)
    if rank is not None:
        rank += 1
    return rank, score


# 新增測資
redis_client.zadd('user_scores', {'iamone': 99999})

# 查詢 前 n 名用户
for user_info in get_top_users(5):
    print(user_info)

# 查詢 指定用戶的資料
user_id = 'iamone'
rank, score = get_user_rank_and_score(user_id)
if rank is not None:
    print(f"{user_id} 的排名为 {rank}，分数为 {score}")
else:
    print(f"{user_id} 不在前 100 名")





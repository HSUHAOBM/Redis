# import redis
# r = redis.StrictRedis(host='127.0.0.1', port='6379')

from redis import Redis


AUTO_COMPLETE_SET = 'complete'
RANGE_LENGTH = 50

r = Redis(host='127.0.0.1', port=6379)

def insert_words(words):
    for word in words:
        for index in range(1, len(word)+1):
            prefix = word[0:index]
            r.zadd(AUTO_COMPLETE_SET, {prefix : 0})

        # ZADD AUTO_COMPLETE_SET 0 word+'*'
        # +* , 來源有此值
        r.zadd(AUTO_COMPLETE_SET, {word+'*' : 0} )


def autocomplete(query, count=10):

    candidates = []
    # 排序位置
    # ZRANK AUTO_COMPLETE_SET query
    start_index = r.zrank(AUTO_COMPLETE_SET, query)

    if not start_index:
        return []

    while len(candidates) <= count:

        # zrange "complete" 0
        possible_candidates = r.zrange(
            AUTO_COMPLETE_SET,
            start_index,
            start_index+RANGE_LENGTH-1
        )
        start_index += RANGE_LENGTH

        if not possible_candidates:
            break

        # 解碼後 加 list
        possible_candidates = [
            candidate.decode('utf-8') for candidate in possible_candidates
        ]

        for candidate in possible_candidates:
            # 測試 測 -> 1
            minlen = min(len(candidate), len(query))

            # 不相關字 回傳
            # 華碩->華 != 測 -> return
            if candidate[0:minlen] != query[0:minlen]:
                return candidates

            # 有來源資料的 加進輸出list
            if candidate[-1] == "*":
                candidates.append(candidate[0:-1])

    return candidates


if __name__ == '__main__':

    # 增加值
    # insert_words(['測試', '測試完成', '中國', '華人', '華碩'])

    print(autocomplete('華'))
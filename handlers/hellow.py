from models.redis_conn import rds_conn

def test():
    a = {"a": 1, "b": 2}
    rds_conn.hmset("ios_review", {"name": "pcl", "age": 18})
    a["data1"] = rds_conn.hgetall("ios_review")
    return a
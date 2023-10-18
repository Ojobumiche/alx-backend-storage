from pymongo import MongoClient

def log_stats():
    """ log_stats.
    """
    client = MongoClient("mongodb://127.0.0.1:27018")

    logs_collection = client.logs.nginx

    total = logs_collection.count_documents({})
    get = logs_collection.count_documents({"method": "GET"})
    post = logs_collection.count_documents({"method": "POST"})
    put = logs_collection.count_documents({"method": "PUT"})
    patch = logs_collection.count_documents({"method": "PATCH"})
    delete = logs_collection.count_documents({"method": "DELETE"})

    """Use a dictionary to store methods and iterate over it"""
    methods = {"GET": get, "POST": post, "PUT": put, "PATCH": patch, "DELETE": delete}

    print(f"{total} logs")
    print("Methods:")  
    for method, count in methods.items():
        print(f"\tmethod {method}: {count}")

    path = logs_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{path} status check")

    print("IPs:")
    """Use a pipeline to aggregate and sort IPs directly in MongoDB"""
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    sorted_ips = logs_collection.aggregate(pipeline)

    for s in sorted_ips:
        print(f"\t{s['_id']}: {s['count']}")

if __name__ == "__main__":
    log_stats()


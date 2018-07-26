import random
import math
import json
import sys

from couchbase.bucket import Bucket

num_products_per_run = 100
num_stores = 100
num_groups = 10

run_number = 0

if len(sys.argv) == 2:
    run_number = int(sys.argv[1])

products_start_at = run_number * num_products_per_run

def num_store_price_changes_per_product():
    return random.randint(1, 10)

def num_store_group_price_changes_per_product():
    return random.randint(1, 10)

num_documents = num_products_per_run * num_stores

price_reasons = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG"]

def make_price_change():
    return {
        "date": random.randint(10000, 100000),
        "reason": random.choice(price_reasons),
        "price": random.uniform(1, 10)
    }

def make_store_product(store_id, product_id):
    return {
        "type": "store_product",
        "store_group_id": int(math.ceil(float(store_id)/num_groups)),
        "store_id": store_id,
        "product_id": product_id,
        "store_prices": [make_price_change() 
                            for i in range(num_store_price_changes_per_product())]
    }

def make_sp_name(sp):
    return "store::" + str(sp["store_id"]) + "::" + "product::" + str(sp["product_id"])

def make_sgp_name(sp):
    return "store_group::" + str(sp["store_group_id"]) + "::" + "product::" + str(sp["product_id"])

def make_store_group_product(store_group_id, product_id):
    return {
        "type": "store_group_product",
        "store_group_id": store_group_id,
        "product_id": product_id,
        "store_group_prices": [make_price_change() 
                                for i in range(num_store_group_price_changes_per_product())]
    }

def store_products_gen(sid, pid, n):
    so_far = 0
    while so_far < n:
        yield make_store_product(sid, pid)
        s_far += 1


from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
cluster = Cluster('couchbase://ec2-18-130-244-207.eu-west-2.compute.amazonaws.com')
authenticator = PasswordAuthenticator('pricing', 'g0ne8ang')
cluster.authenticate(authenticator)
cb = cluster.open_bucket('pricing3')

for sid in range(1, num_stores + 1):
    for pid in range(1, num_products_per_run + 1):
        doc = make_store_product(sid, pid + products_start_at)
        cb.insert(make_sp_name(doc), doc)

for gid in range(1, num_groups + 1):
    for pid in range(1, num_products_per_run + 1):
        doc = make_store_group_product(gid, pid + products_start_at)
        cb.insert(make_sgp_name(doc), doc)

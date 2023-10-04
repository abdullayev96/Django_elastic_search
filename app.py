from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
from gevent.pywsgi import WSGIServer
from datetime import datetime


# #
# app = Flask(__name__)
#
#
# @app.route("/")
# def home():
#     #return "Hello python "
#     return render_template("index.html")
#
#
# @app.route("/search")
# def search_autocomplete(post_titles):
#     query = request.args["q"].lower()
#     tokens = query.split(" ")
#     print(tokens)
#     index_name = 'url_index'
#     for post_title in post_titles:
#         payload = {
#             "query": {
#                 "match": {
#                     "post_title": post_title
#                 }
#             }
#         }
#
#         result = es.search(index=index_name, query=payload)
#
#         post = result['hits']['hits'][0]
#         post_permalink = post['_source']['post_permalink']
#
#         post_titles = ['Car details v3.csv']
#
#         return post_titles



# def URL_Extractor(post_titles):
#     #es = Elasticsearch(['http://95.217.208.18:1997'])
#     es = Elasticsearch(hosts=["http://127.0.0.1:9200"])
#
#
# URL_Extractor(post_titles)
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
#


# @app.route("/search")
# def search_autocomplete():
#     query = request.args["q"].lower()
#     tokens = query.split(" ")
#
#     print(tokens)
#
#
#
# if __name__ == "__main__":
#     app.run(debug=True)




#client = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# client = Elasticsearch(hosts=["http://127.0.0.1:9200"])
#
# app = Flask(__name__)
#
#
# @app.route("/")
# def home():
#     #return "Hello python "
#     return render_template("index.html")
#
#
# @app.route("/search")
# def search_autocomplete():
#     query = request.args["q"].lower()
#     tokens = query.split(" ")
#     print(tokens)
#
#     index_name = "cars"
#     payload = {
#         "settings": {
#             "number_of_shards": 1,
#             "number_of_replicas": 2
#         },
#
#         "mappings": {
#             "properties": {
#                 "make": {"type": "text"},
#                 "model": {"type": "text"},
#                 "year": {"type": "integer"}
#
#             }
#         }
#     }
#
#     res=client.indices.create(index=index_name, query=payload)
#     print(res)
#
#
# if __name__ == "__main__":
#     app.run(debug=True)




es = Elasticsearch(hosts=["http://127.0.0.1:9200"])
#print(f"Connected to ElasticSearch cluster `{es.info().body['cluster_name']}`")



app = Flask(__name__)

MAX_SIZE = 300


@app.route("/")
def home():
    #return "Hello python "
    return render_template("index.html")



@app.route("/search")
def search_autocomplete():
    query = request.args["q"].lower()
    tokens = query.split(" ")
    print(tokens)
    index_name = "cars"
    #index_name = 'url_index'

    clauses = [
        {
            "span_multi": {
                "match": {"fuzzy": {"name": {"value": i, "fuzziness": "AUTO"}}}
            }
        }
        for i in tokens
    ]

    payload = {
        # "size":MAX_SIZE,
        # "query":{
        "bool": {
            "must": [{"span_near": {"clauses": clauses, "slop": 0, "in_order": False}}
                     ]
        }
    }
    try:
        resp = es.search(index=index_name, query=payload, size=MAX_SIZE)
        return resp
    except Exception as e:
        print(e)


    for result in resp['hits']['hits']:
        print(result)

    return [result['_source']['name'] for result in resp['hits']['hits']]


if __name__ == "__main__":
    app.run(debug=True)


    # http_server = WSGIServer(("127.0.0.1", 8080), app)
    # http_server.serve_forever()

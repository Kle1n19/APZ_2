import hazelcast
import threading

def run_client(client_id):
    client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"]
    )
    distributed_map = client.get_map("map").blocking()
    if client_id == 0:
        for i in range(1000):
            distributed_map.put(str(i), f"{i}")

    def increment_map():
        for _ in range(10000):
            value = distributed_map.get("counter") or 0
            distributed_map.put("counter", value + 1)

    increment_map()
    client.shutdown()

threads = []
for i in range(3):
    t = threading.Thread(target=run_client, args=(i,))
    t.start()
    threads.append(t)
for t in threads:
    t.join()
final_client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"]
)
final_map = final_client.get_map("map").blocking()
print("Final value of 'counter':", final_map.get("counter"))

final_client.shutdown()

import hazelcast
import threading

def run_client_with_lock(client_id):
    client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"]
    )
    distributed_map = client.get_map("map").blocking()
    if client_id == 0:
        for i in range(1000):
            distributed_map.put(str(i), f"{i}")

    def increment_map_with_lock():
        for _ in range(10000):
            distributed_map.lock("counter")
            try:
                value = distributed_map.get("counter") or 0
                distributed_map.put("counter", value + 1)
            finally:
                distributed_map.unlock("counter")

    increment_map_with_lock()

    client.shutdown()

threads = []
for i in range(3):
    t = threading.Thread(target=run_client_with_lock, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

final_client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"]
)
final_map = final_client.get_map("map").blocking()

print("Final value with pessimistic locking:", final_map.get("counter"))

final_client.shutdown()

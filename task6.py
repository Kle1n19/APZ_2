import hazelcast
import threading
import time

def run_client_with_optimistic_lock(client_id):
    client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"]
    )
    distributed_map = client.get_map("map").blocking()

    if client_id == 0:
        for i in range(1000):
            distributed_map.put(str(i), f"{i}")

    def increment_map_with_optimistic_lock():
        for _ in range(10000):
            while True:
                old_value = distributed_map.get("counter") or 0
                if distributed_map.replace_if_same("counter", old_value, old_value + 1):
                    break

    increment_map_with_optimistic_lock()

    client.shutdown()

start_time = time.time()

threads = []
for i in range(3):
    t = threading.Thread(target=run_client_with_optimistic_lock, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

final_client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"]
)
final_map = final_client.get_map("map").blocking()

final_value = final_map.get("counter")
print("Final value with optimistic locking:", final_value)

end_time = time.time()
print(f"Time taken: {end_time - start_time:.2f} seconds")

final_client.shutdown()

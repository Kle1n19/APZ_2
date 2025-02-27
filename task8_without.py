import hazelcast
import time


def producer(client):
    queue = client.get_queue("queue").blocking()
    for i in range(1, 101):
        while queue.size() >= 10:
            time.sleep(0.1)
        queue.put(i)
        print(f"Produced: {i}")
        time.sleep(0.1)

client1 = hazelcast.HazelcastClient(cluster_name="dev")
producer(client1)
client1.shutdown()

import hazelcast
import threading
import time

def run_client_with_bounded_queue():
    client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=["127.0.0.1:5701", "127.0.0.1:5702", "127.0.0.1:5703"]
    )

    queue = client.get_queue("bounded-queue").blocking()

    done = threading.Event()

    def producer():
        for i in range(1, 101):
            while queue.size() >= 10:
                time.sleep(0.1)

            queue.put(i)
            print(f"Prod {i}")

        done.set()

    def consumer():
        while not done.is_set() or queue.size() > 0:
            if not queue.is_empty():
                value = queue.take()
                print(f"Consume {value}")
            else:
                time.sleep(0.1)

    start_time = time.time()

    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t3 = threading.Thread(target=consumer)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")

    client.shutdown()

run_client_with_bounded_queue()

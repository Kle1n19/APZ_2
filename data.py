import hazelcast
client = hazelcast.HazelcastClient()

distributed_map = client.get_map("my-map").blocking()

for i in range(1000):
    distributed_map.put(str(i), f"Value-{i}")

print("Done")

client.shutdown()

import hazelcast
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Configure the Hazelcast client
client = hazelcast.HazelcastClient(
    cluster_members=[
        "127.0.0.1:5701",  # Node 1
        "127.0.0.1:5702",  # Node 2
        "127.0.0.1:5703"   # Node 3
    ],
    cluster_name="dev",  # Ensure this matches your Hazelcast cluster name
)

print("✅ Connected to Hazelcast cluster.")

distributed_map = client.get_map("test-map").blocking()

# Insert 1000 key-value pairs
for i in range(1000):
    distributed_map.put(str(i), f"Value-{i}")

print("🔹 Inserted 1000 key-value pairs into the distributed map.")

# Shutdown the client
client.shutdown()
print("🔴 Client disconnected.")

# Hazelcast Queue with Producer-Consumer

This project demonstrates the usage of a Hazelcast distributed queue with producer and consumer threads, while ensuring that the queue size remains bounded (max size = 10).

## Features
- **Producer thread**: Produces 100 items and adds them to a Hazelcast queue with a maximum size of 10.
- **Consumer threads**: Consumes items from the queue, with two consumers running concurrently.
- **Thread synchronization**: The producer waits until there is space in the queue, and the consumers stop once all items have been consumed.

## Requirements
- Hazelcast installed and running on the specified ports (5701, 5702, 5703).
- Python 3.x
- Install the Hazelcast Python client: `pip install hazelcast`

## How to Run

1. **Start Hazelcast cluster** (ensure the nodes are running at `127.0.0.1:5701`, `127.0.0.1:5702`, and `127.0.0.1:5703`).
2. **Run the Python script**:
   ```bash
   python hazelcast_queue.py

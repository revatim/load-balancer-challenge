# What I Learned Building a Load Balancer
In this project, I had the opportunity to build a simple load balancer (LB) and backend (BE) servers using Python's socket programming. Here are some key takeaways from this experience:

## Understanding Sockets
Sockets provide a way for two programs to communicate with each other, usually over a network. In Python, the `socket` library provides a low-level networking interface that's relatively easy to use. I used this library to create the LB and BE servers.

## Load Balancer (LB)
The LB's job is to distribute incoming network traffic across multiple servers to ensure no single server is overwhelmed. This is crucial for maintaining the performance and reliability of applications.
In my LB implementation, I used a simple round-robin algorithm to distribute incoming requests evenly across the BE servers. I am also learning about more complex load balancing algorithms, such as least connections and least time, which can provide better performance in certain scenarios.

Here is a short summary:
### Round-Robin Algorithm
The round-robin algorithm is one of the simplest methods for load balancing. It works by **distributing incoming requests in a circular order, sequentially**, across all servers in the pool. After it sends a request to the last server in the list, it starts again from the first server.
This algorithm doesn't consider the current load of each server or their response times. <br>
**When to use this ?** <br>
When all your backend servers are of similar specification and the tasks they perform are roughly equal in terms of required resources and processing time.
However, in situations where the servers or the requests are not uniform, round-robin can lead to imbalances where some servers are heavily loaded while others are underutilized. In such cases, more dynamic load balancing methods like least connections or least time might be more appropriate.

### Least Connections Algorithm
Dynamic load balancing method. Works by tracking the number of active connections to each server and routing new requests to the server with the fewest active connections. <br>
**When to use this ?** <br>
When the servers have similar capabilities and the requests take a long time to process. It ensures that the load is distributed more evenly across the servers, reducing the likelihood that any single server will become a bottleneck.

### Least Time Algorithm
Dynamic load balancing method. Works by tracking the response times and the number of active connections of each server. New requests are routed to the server with the fewest active connections and the lowest average response time.  <br>
**When to use this ?** <br>
When the servers have varying capabilities and the network conditions are unpredictable. It ensures that the load is distributed in a way that minimizes the overall response time, providing a better user experience.

## Backend (BE) Servers
Each BE server simply echoes back whatever data it receives.

#### Handling Incoming Data in My Load Balancer
Understanding `client_conn.recv()`

Blocking Operation: Waits until data arrives or the connection closes, potentially stalling the program.
Fixed Buffer Size: It attempts to receive data in chunks of the specified size (e.g., 1024 bytes). This assumes the client sends data in multiples of that size, which might not always be true.

**Initial Approach and the Pitfall**

```python
data = client_conn.recv(1024)
while data:
    be_sock.sendall(data)
    data = client_conn.recv(1024)
```
<br>
Initially, I used a loop to receive data in 1024-byte chunks. This approach could lead to an infinite loop if the client sent all its data in a single 1024-byte chunk. Here's why:

Subsequent calls to client_conn.recv(1024) would still receive empty strings due to the fixed buffer size.
The loop condition (while data:) interprets empty strings as non-empty, causing an infinite wait for more data. <br>
**Improved Solution and Key Takeaway**

To address this, I modified the code to check the received data's length:

```python
while chunk := client_conn.recv(1024):
    be_sock.sendall(chunk)
    if len(chunk) < 1024:
        # Assumes we have received the last chunk
        break
```

This approach checks if a chunk is smaller than the buffer size, indicating the likely arrival of the last chunk. This allows the loop to break and prevents infinite waiting.
<hr>

## Potential Unresolved Problems
Assumption: received the last chunk based solely on the condition` len(chunk) < 1024`

**Partial Final Chunk**: The client could potentially send the final chunk of data in a size smaller than 1024 bytes, but it might not be the final last chunk. There could be additional data following that chunk.

**Network Delays and Fragmentation**: Network conditions can introduce delays between data packets. It's possible that the remaining data might be arriving in separate packets that are smaller than 1024 bytes each. In this scenario, the code would break prematurely, missing the remaining data.

These limitations can lead to incomplete data being received on the server side if the actual last chunk happens to be smaller than 1024 bytes or if there are network delays fragmenting the data.


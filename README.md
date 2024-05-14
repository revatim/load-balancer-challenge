# Load Balancer Challenge
This project is a simple implementation of a load balancer and backend servers. 

## Prerequisites
- Python 3.x

## How to Run
1. Clone the repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Run the backend servers. You can start a servers on a multiple ports by running `python3 start_be_servers.py`. You can configure details for the instances in `config.json`.
4. Run the load balancer by running `python3 lb.py`.

## How to Test
1. Send a request to the load balancer from a separate terminal window. You can do this by running `curl localhost:<load_balancer_port>`.
2. The load balancer should forward your request to one of the backend servers and then forward the server's response back to you.

## Technical Details 
### Round-Robin Load Balancing
The load balancer utilizes a round-robin algorithm to evenly distribute incoming requests among the available servers. This ensures each server gets an equal share of the load, preventing any single server from becoming a bottleneck.

### Health Checks
WIP

### Logging
WIP

### Note
For a detailed reflection on the development process and key learnings from this project, check out [LearningExperience.md](./LearningExperience.md). <br>
This is a basic implementation of a load balancer and does not include many features that a real-world load balancer would have, such as health checks, session persistence, and SSL termination.

## Credits
This project is a solution to the Load Balancer challenge on Coding Challenges. 

## License
This project is licensed under the terms of the MIT license.

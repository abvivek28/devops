# Exercise 4: Docker Networking with Multiple Containers

## Objective
Understand Docker networking by creating a custom bridge network and connecting multiple containers to enable communication between them.

## Scenario
Configure a multi-container environment consisting of:
- **Flask:** Web application providing a REST API.
- **MySQL:** Database container.
- **Redis:** Cache container.

## Implementation

### 1. Create a Bridge Network

```powershell
docker network create --driver bridge my-bridge-net
```

**Purpose:** Creates a custom bridge network that allows containers connected to it to communicate with one another.

### 2. Verify the Network

```powershell
docker network ls
```

**Purpose:** Lists Docker networks and verifies that `my-bridge-net` has been created.

### 3. Inspect the Network

```powershell
docker network inspect my-bridge-net
```

**Purpose:** Displays network configuration, including its driver, subnet, gateway, and connected containers.

### 4. Create the Flask Application

Create `app.py`:

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/about', methods=['GET'])
def about():
    return jsonify({
        "name": "Simple REST API",
        "version": "1.0",
        "description": "This is a simple REST API built with Flask."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
```

Create `requirements.txt`:

```text
Flask==2.0.1
```

**Purpose:** Implements a REST endpoint at `/about` that returns information about the application. Binding to `0.0.0.0` allows the application to accept connections through the container's network interface.

### 5. Create the Dockerfile

Create a file named `Dockerfile`:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
COPY app.py .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5001
CMD ["python", "app.py"]
```

**Purpose:** Defines the container environment, installs Flask, copies the application files, and configures the startup command.

### 6. Build the Flask Docker Image

```powershell
docker build -t flask-api .
```

**Purpose:** Builds a Docker image named `flask-api` containing the Flask application.

### 7. Launch the Containers

```powershell
docker run -d --name mysql --network my-bridge-net mysql:latest
docker run -d --name redis --network my-bridge-net redis:latest
docker run -d --name flask --network my-bridge-net -p 5001:5001 flask-api
```

**Purpose:** Starts the MySQL, Redis, and Flask containers in detached mode and connects them to the same bridge network. The `-p` option publishes Flask's port 5001 on the host.

### 8. Test Container Connectivity

Enter the Flask container:

```powershell
docker exec -it flask bash
```

Test connectivity to MySQL:

```bash
ping mysql
```

Test connectivity to Redis:

```bash
ping redis
```

**Purpose:** Verifies that containers on the custom bridge network can resolve one another by container name and communicate over the network.

### 9. Test the Flask API

From the host machine, run:

```powershell
curl.exe http://localhost:5001/about
```

**Purpose:** Sends an HTTP request to the Flask application through the published port and verifies that the REST endpoint returns a JSON response.

### 10. Clean Up Resources

Stop and remove the containers:

```powershell
docker stop mysql redis flask
docker rm mysql redis flask
```

Remove the custom bridge network:

```powershell
docker network rm my-bridge-net
```

**Purpose:** Releases the containers and network created for the exercise.

## Expected Result
- A custom bridge network named `my-bridge-net` is created.
- Flask, MySQL, and Redis containers are connected to the same network.
- The Flask container can resolve the MySQL and Redis container names.
- The Flask REST API responds successfully at `http://localhost:5001/about`.
- All exercise resources can be removed after testing.

## Questions and Answers

**1. What is the purpose of the `--network` flag in `docker run`?**

It specifies the Docker network to which a container should connect.

**2. How do containers communicate with each other on the same network?**

Containers on a user-defined bridge network can communicate using container names or IP addresses.

**3. What is the difference between a bridge network and a host network?**

A bridge network provides an isolated network for containers, while a host network shares the host's network stack.

**4. How can you expose a container's port to the host machine?**

Use the `-p` option, such as `-p 5001:5001`, to map a host port to a container port.

## Conclusion
Successfully created a custom Docker bridge network, launched multiple containers, verified container-to-container connectivity, exposed a Flask REST API to the host, and cleaned up the resources.
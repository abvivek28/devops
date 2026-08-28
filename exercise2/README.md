# Exercise 2: Deploy a Flask Application on Minikube

## Objective
Deploy a Python Flask application on a local Kubernetes cluster using Minikube, Docker, and Kubernetes YAML configuration. Expose the application through a NodePort Service and verify its accessibility.

## Prerequisites
- Docker Desktop installed and running
- Minikube installed
- Kubernetes CLI (`kubectl`) available
- Python and Docker basics

## Implementation

### 1. Start the Minikube Cluster

```powershell
minikube start --driver=docker
```

**Purpose:** Starts a local Kubernetes cluster using Docker as the driver.

### 2. Create the Flask Application

Create `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask on Kubernetes!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000)
```

**Purpose:** Creates a Flask web application that responds to requests on port `15000`.

### 3. Create the Dockerfile

Create a file named `Dockerfile`:

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install flask
CMD ["python", "app.py"]
```

**Purpose:** Defines the environment and instructions required to package the Flask application into a Docker image.

### 4. Build the Docker Image

Configure the Docker CLI to use Minikube's Docker daemon and build the image:

```powershell
minikube docker-env
```

On Linux or macOS, configure the environment using:

```bash
eval $(minikube docker-env)
docker build -t flask-app .
```

**Purpose:** Builds the `flask-app` image in Minikube's Docker environment so Kubernetes can use the locally available image.

### 5. Create the Kubernetes Deployment

Create `flask-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
        - name: flask-app
          image: flask-app:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 15000
```

**Purpose:** Defines a Deployment that manages one Flask Pod. The `imagePullPolicy: Never` setting instructs Kubernetes to use the locally available image instead of pulling it from a registry.

### 6. Deploy the Application

```powershell
kubectl apply -f flask-deployment.yaml
```

**Purpose:** Creates the Kubernetes Deployment using the YAML configuration.

### 7. Verify the Deployment and Pod

Check the Deployment:

```powershell
kubectl get deployments
```

Check the Pod:

```powershell
kubectl get pods -l app=flask-app
```

**Purpose:** Verifies that the Deployment has the expected replica count and that the Flask Pod is running.

### 8. Inspect Deployment Details and Logs

Describe the Deployment:

```powershell
kubectl describe deployment flask-app
```

View the application logs:

```powershell
kubectl logs <pod-name>
```

Replace `<pod-name>` with the actual Pod name obtained from `kubectl get pods`.

**Purpose:** Inspects Deployment status, events, and configuration, and checks the Flask application logs for successful startup.

### 9. Expose the Application Through a Service

Update `flask-deployment.yaml` to include the following Service definition after the Deployment:

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  selector:
    app: flask-app
  ports:
    - port: 15000
      targetPort: 15000
  type: NodePort
```

Apply the updated configuration:

```powershell
kubectl apply -f flask-deployment.yaml
```

**Purpose:** Creates a NodePort Service that routes requests to the Flask Pod.

- `port`: The port exposed by the Service.
- `targetPort`: The port on which the Flask application listens.
- `type: NodePort`: Exposes the Service through a port on the Kubernetes node.

### 10. Access and Test the Application

Check the available Services:

```powershell
kubectl get services
```

Obtain the Service URL:

```powershell
minikube service flask-app-service --url
```

Use the URL returned by the command to test the application:

```powershell
curl <service-url>
```

**Purpose:** Retrieves an accessible URL for the Service and verifies that the Flask application responds successfully.

## Expected Result

The application returns the following response when accessed through the Service URL:

```text
Hello from Flask on Kubernetes!
```

## Conclusion

Successfully containerized and deployed a Python Flask application on Minikube using a Kubernetes Deployment and YAML configuration. Exposed the application through a NodePort Service and verified its accessibility using the generated Service URL.
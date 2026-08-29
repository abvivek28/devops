# Exercise 3: Scaling a Flask Application Using ReplicaSets

## Objective
Deploy a Flask-based flash-sale application on a single-node Kubernetes cluster using Minikube. Understand ReplicaSets, scale the application from 3 to 5 replicas, and observe automatic Pod replacement and Pod distribution.

## Real-Life Use Case
During an e-commerce flash sale, traffic can increase dramatically. Kubernetes ReplicaSets maintain the desired number of application Pods, helping improve availability and accommodate increased demand.

## Implementation

### 1. Build the Docker Image

Create a Dockerfile for the Flask application using Python and Gunicorn.

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir flask gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "1", "--threads", "2"]
```

Build and push the image to Docker Hub:

```bash
docker build -t <your-dockerhub-username>/flashsale:1.0 .
docker push <your-dockerhub-username>/flashsale:1.0
```

**Purpose:** Packages the Flask application into a Docker image that Kubernetes can run.

### 2. Start the Minikube Cluster

```bash
minikube start --nodes=1
kubectl get nodes
```

**Purpose:** Starts a single-node Kubernetes cluster and verifies that the node is ready.

### 3. Create the ReplicaSet and Service

Create `flashsale-replicaset.yaml` with a ReplicaSet configured for 3 replicas and a ClusterIP Service.

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: flashsale-rs
  labels:
    app: flashsale
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flashsale
  template:
    metadata:
      labels:
        app: flashsale
    spec:
      containers:
        - name: flashsale-container
          image: <your-dockerhub-username>/flashsale:1.0
          ports:
            - containerPort: 5000
          readinessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 2
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 10
            periodSeconds: 10
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: flashsale-svc
spec:
  selector:
    app: flashsale
  ports:
    - name: http
      port: 80
      targetPort: 5000
  type: ClusterIP
```

**Purpose:** Defines three identical application Pods, health probes, resource limits, and a Service for internal communication with the Pods.

### 4. Apply the Configuration

```bash
kubectl apply -f flashsale-replicaset.yaml
```

**Purpose:** Creates the ReplicaSet and Service in Kubernetes.

### 5. Verify the ReplicaSet and Pods

```bash
kubectl get rs
kubectl get pods
```

**Purpose:** Confirms that the ReplicaSet maintains the desired three Pods.

### 6. Scale the ReplicaSet to Five Replicas

```bash
kubectl scale rs flashsale-rs --replicas=5
```

Verify the updated state:

```bash
kubectl get rs
kubectl get pods
```

**Purpose:** Increases the desired replica count from three to five. Kubernetes creates two additional Pods.

### 7. Delete a Pod and Observe Self-Healing

```bash
kubectl delete pod <pod-name>
kubectl get pods
```

Replace `<pod-name>` with the name of one of the existing Pods.

**Purpose:** Demonstrates self-healing: the ReplicaSet automatically creates a replacement Pod to restore the desired replica count of five.

### 8. Observe Pod Distribution

```bash
kubectl get pods -o wide
```

**Purpose:** Displays Pod IP addresses and node assignments, demonstrating that all five Pods run on the single Kubernetes node.

### 9. Inspect the ReplicaSet and Application Logs

```bash
kubectl describe rs flashsale-rs
kubectl logs <pod-name>
```

**Purpose:** Examines ReplicaSet events, replica status, and application logs for troubleshooting and verification.

## Expected Result
- Three Pods are initially created by the ReplicaSet.
- Scaling increases the number of Pods to five.
- Deleting a Pod triggers automatic replacement.
- All five Pods run on the single Minikube node.
- The Service selects Pods labeled `app: flashsale`.

## Key Learnings
- **ReplicaSets:** Maintain a specified number of Pod replicas.
- **Scalability:** Increase or decrease replicas to adjust application capacity.
- **Self-healing:** Replace deleted Pods to maintain the desired state.
- **Service Discovery:** Route requests to matching application Pods through a Kubernetes Service.
- **Resource Management:** Configure CPU and memory requests and limits for containers.

## Conclusion
Successfully deployed and scaled a Flask flash-sale application using a Kubernetes ReplicaSet on Minikube. Verified replica scaling, automatic Pod replacement, and Pod distribution across a single node.
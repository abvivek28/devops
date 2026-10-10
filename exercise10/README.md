# Exercise 10: Multi-Node Kubernetes Cluster with Multiple Applications and ReplicaSets

## Objective

To deploy multiple Python Flask applications on a multi-node Kubernetes cluster using Minikube. The exercise demonstrates replica management, pod distribution across nodes, service exposure, and application testing.

## Scenario

An e-commerce platform requires two services:

- **Product Catalog (AppA):** Provides information about available products, with 2 replicas.
- **Shopping Cart (AppB):** Manages shopping cart operations, with 3 replicas.

The applications are deployed across multiple Kubernetes nodes to improve availability and fault tolerance.

## Prerequisites

- Docker Desktop installed and running.
- Minikube and kubectl installed.
- Docker and Kubernetes fundamentals.
- Python and Flask for local application development.
- A terminal with access to Minikube and Docker commands.

## Implementation

### Step 1: Set Up a Multi-Node Minikube Cluster

Stop and delete any existing Minikube cluster if it is no longer required.

```bash
minikube stop
minikube delete
```

Create a three-node cluster using a dedicated profile.

```bash
minikube start --nodes 3 -p devops-multinode --driver=docker
```

Verify the cluster nodes.

```bash
kubectl --context=devops-multinode get nodes
```

### Step 2: Create the Product Catalog Application

Create `product_catalog.py` to return a list of available products.

```python
from flask import Flask, jsonify

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Phone", "price": 800},
    {"id": 3, "name": "Headphones", "price": 150}
]

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

### Step 3: Create the Shopping Cart Application

Create `shopping_cart.py` to retrieve and add items to a shopping cart.

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

cart = []

@app.route("/cart", methods=["GET"])
def get_cart():
    return jsonify(cart)

@app.route("/cart", methods=["POST"])
def add_to_cart():
    item = request.json
    cart.append(item)
    return jsonify(cart), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

### Step 4: Dockerize the Applications

Create `Dockerfile.product` for the Product Catalog.

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY product_catalog.py /app/
RUN pip install flask
CMD ["python", "product_catalog.py"]
```

Create `Dockerfile.shopping` for the Shopping Cart.

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY shopping_cart.py /app/
RUN pip install flask
CMD ["python", "shopping_cart.py"]
```

Build the Docker images.

```bash
docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .
```

Verify that the images have been created.

```bash
docker images
```

### Step 5: Load the Images into Minikube

Load both images into the Minikube cluster.

```bash
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest
```

Verify that the images are available.

```bash
minikube -p devops-multinode ssh -- docker images
```

### Step 6: Deploy the Product Catalog

Create `product_catalog_deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-catalog
spec:
  replicas: 2
  selector:
    matchLabels:
      app: product-catalog
  template:
    metadata:
      labels:
        app: product-catalog
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: product-catalog
              topologyKey: kubernetes.io/hostname
      containers:
        - name: product-catalog-container
          image: product-catalog:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 80
```

The Deployment maintains two replicas. Required pod anti-affinity instructs Kubernetes to place them on different nodes.

### Step 7: Deploy the Shopping Cart

Create `shopping_cart_deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shopping-cart
spec:
  replicas: 3
  selector:
    matchLabels:
      app: shopping-cart
  template:
    metadata:
      labels:
        app: shopping-cart
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: shopping-cart
              topologyKey: kubernetes.io/hostname
      containers:
        - name: shopping-cart-container
          image: shopping-cart:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 80
```

The Deployment maintains three replicas and requires each replica to be scheduled on a different node.

Apply both Deployment manifests.

```bash
kubectl apply -f product_catalog_deployment.yaml
kubectl apply -f shopping_cart_deployment.yaml
```

### Step 8: Expose the Applications Using Services

Create `product_catalog_service.yaml`.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: product-catalog-service
spec:
  selector:
    app: product-catalog
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort
```

Create `shopping_cart_service.yaml`.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: shopping-cart-service
spec:
  selector:
    app: shopping-cart
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort
```

Apply both Service manifests.

```bash
kubectl apply -f product_catalog_service.yaml
kubectl apply -f shopping_cart_service.yaml
```

### Step 9: Verify Pod Distribution

Check the status of the Pods and identify the node on which each Pod is running.

```bash
kubectl get pods -o wide
```

Check the Deployments and Services.

```bash
kubectl get deployments
kubectl get services
kubectl get nodes
```

**Expected result:**

- Two Product Catalog Pods should be running on separate nodes.
- Three Shopping Cart Pods should be running, one on each node.
- Both Deployments should report all desired replicas as available.

### Step 10: Access the Applications

Open separate terminals and run the following commands.

For the Product Catalog:

```bash
minikube -p devops-multinode service product-catalog-service
```

For the Shopping Cart:

```bash
minikube -p devops-multinode service shopping-cart-service
```

Minikube displays the accessible URL for each Service. Keep the terminal open while using the forwarded URL if Minikube requires the tunnel to remain active.

### Step 11: Test the Product Catalog

Send a GET request to the Product Catalog endpoint using the URL provided by Minikube.

```bash
curl http://127.0.0.1:<product-port>/products
```

Expected response:

```json
[
  {"id": 1, "name": "Laptop", "price": 1200},
  {"id": 2, "name": "Phone", "price": 800},
  {"id": 3, "name": "Headphones", "price": 150}
]
```

Replace `<product-port>` with the port from the URL displayed by Minikube.

### Step 12: Test the Shopping Cart

Retrieve the current cart.

```bash
curl http://127.0.0.1:<cart-port>/cart
```

Expected response for a newly started application:

```json
[]
```

Add an item to the cart.

```bash
curl -X POST http://127.0.0.1:<cart-port>/cart -H "Content-Type: application/json" -d "{\"id\":1,\"name\":\"Laptop\",\"quantity\":1}"
```

Expected response:

```json
[
  {"id": 1, "name": "Laptop", "quantity": 1}
]
```

Replace `<cart-port>` with the port displayed for the Shopping Cart Service.

## Expected Outcome

| Component | Expected Result |
|---|---|
| Minikube cluster | Three nodes created |
| Product Catalog | Two replicas running on separate nodes |
| Shopping Cart | Three replicas distributed across all three nodes |
| Kubernetes Services | Both applications exposed through NodePort Services |
| Product endpoint | Returns the product list |
| Cart endpoints | Supports retrieving and adding cart items |

## Key Learnings

- Creating and managing multi-node Kubernetes clusters with Minikube.
- Packaging Python applications into Docker images.
- Deploying applications using Kubernetes Deployments.
- Managing replicas and distributing Pods with pod anti-affinity.
- Exposing applications through Kubernetes Services.
- Verifying application functionality using HTTP requests.

## Conclusion

Successfully deployed two Flask applications on a three-node Minikube cluster. The Product Catalog runs with two replicas, while the Shopping Cart runs with three replicas. Kubernetes Services provide access to both applications, and pod anti-affinity distributes replicas across separate nodes to improve availability.


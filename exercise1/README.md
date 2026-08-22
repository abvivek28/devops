# Exercise 1: Hello Pod

## Objective
Deploy an Nginx container as a Kubernetes Pod using Minikube and expose it through a NodePort Service to access it from a web browser.

## Prerequisites
- Docker Desktop installed and running.
- Minikube installed.
- `kubectl` available through Minikube.

## Implementation

### 1. Start the Kubernetes Cluster
```powershell
minikube start --driver=docker
```
**Purpose:** Starts a local Kubernetes cluster using Docker as the driver.

### 2. Create an Nginx Pod
```powershell
minikube kubectl -- run hello-k8s --image=nginx --port=80
```
**Purpose:** Creates a Pod named `hello-k8s` using the official Nginx image and declares port 80.

### 3. Verify the Pod
```powershell
minikube kubectl -- get pods
```
**Purpose:** Checks the Pod's status and confirms that it is running.

### 4. Expose the Pod as a Service
```powershell
minikube kubectl -- expose pod hello-k8s --type=NodePort --port=80
```
**Purpose:** Creates a NodePort Service to provide access to the Nginx Pod.

### 5. Access the Application
```powershell
minikube service hello-k8s
```
**Purpose:** Opens the Service endpoint in a browser to access the Nginx welcome page.

## Expected Result
The Nginx welcome page is displayed in the browser, confirming that the Pod is running and accessible through the Kubernetes Service.

## Conclusion
Successfully deployed an Nginx Pod on a local Kubernetes cluster using Minikube and exposed the application through a NodePort Service.

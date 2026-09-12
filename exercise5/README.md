# Exercise 5: Docker Security with AppArmor and Python

## Objective
Secure a Dockerized Flask application using AppArmor profiles. Apply security restrictions through Docker CLI and the Docker SDK for Python, and test restricted file access and binary execution.

## Prerequisites
- Docker installed and running
- Python installed
- AppArmor enabled on a supported Linux system
- `apparmor-utils` installed
- Docker SDK for Python installed

## Implementation

### 1. Install AppArmor Utilities

```bash
sudo apt-get update
sudo apt-get install apparmor-utils
```

**Purpose:** Installs the utilities required to manage and load AppArmor profiles.

### 2. Create the Flask Application

Create `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is a secure Flask application running inside a Docker container!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Purpose:** Creates a Flask web application that listens on port 5000.

### 3. Containerize the Application

Create a `Dockerfile`:

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install flask
EXPOSE 5000
CMD ["python", "app.py"]
```

Build the Docker image:

```bash
docker build -t flask-apparmor .
```

**Purpose:** Packages the Flask application and its dependencies into a Docker image.

### 4. Create and Load the AppArmor Profile

Create `/etc/apparmor.d/my-apparmor-profile`:

```text
#include <tunables/global>

/usr/bin/python3 {
    deny /etc/** r,
    deny /var/** rw,

    network inet stream,

    /app/** rwk,

    deny /bin/** rmix,
    deny /usr/bin/** rmix,

    capability net_bind_service,
    deny capability sys_admin,
}
```

Load the profile:

```bash
sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
```

**Purpose:** Defines restrictions on filesystem access, binary execution, networking, and system administration capabilities.

### 5. Run the Container with AppArmor

```bash
docker run --security-opt="apparmor=my-apparmor-profile" -p 5000:5000 flask-apparmor
```

**Purpose:** Starts the Flask container with the specified AppArmor profile and publishes port 5000 on the host.

### 6. Apply AppArmor Using the Docker SDK for Python

Install the Docker SDK:

```bash
pip install docker
```

Create `apply_apparmor.py`:

```python
import docker

client = docker.from_env()

client.images.build(path=".", tag="flask-apparmor")

container = client.containers.run(
    "flask-apparmor",
    ports={'5000/tcp': 5000},
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True
)

print(f"Container started: {container.short_id}")

container_info = client.api.inspect_container(container.id)
apparmor_profile = container_info['HostConfig']['SecurityOpt']

print(f"AppArmor profile applied: {apparmor_profile}")

container.stop()
```

Execute the script:

```bash
python apply_apparmor.py
```

**Purpose:** Builds the image, starts the container with the AppArmor profile, verifies the configured security option, and stops the container.

### 7. Test Restricted Actions

Create `test_restricted_actions.py`:

```python
import docker

client = docker.from_env()

container = client.containers.run(
    "flask-apparmor",
    ports={'5000/tcp': 5000},
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True
)

exit_code, output = container.exec_run("cat /etc/passwd")
print(f"Attempt to read /etc/passwd: Exit Code {exit_code}, Output: {output.decode()}")

exit_code, output = container.exec_run("/bin/bash")
print(f"Attempt to execute /bin/bash: Exit Code {exit_code}, Output: {output.decode()}")

container.stop()
print("Container stopped")
```

Execute the script:

```bash
python test_restricted_actions.py
```

**Purpose:** Tests whether the configured security policy restricts access to `/etc/passwd` and execution of `/bin/bash`.

### 8. Verify the Security Configuration

Inspect the container's security options using the Docker CLI:

```bash
docker inspect <container-id>
```

Or use the Docker SDK:

```python
container_info = client.api.inspect_container(container.id)
print(container_info['HostConfig']['SecurityOpt'])
```

**Purpose:** Checks the configured security options to verify that the AppArmor profile was requested for the container.

## Expected Result
- The Flask application is containerized successfully.
- The AppArmor profile is loaded and specified when the container starts.
- The Docker SDK reports the configured AppArmor security option.
- Restricted file access and binary execution are tested.
- The container can be stopped after testing.

## Conclusion
Successfully configured a Dockerized Flask application with an AppArmor security profile, applied the profile through Docker CLI and the Docker SDK for Python, and tested restricted operations to understand container security enforcement.
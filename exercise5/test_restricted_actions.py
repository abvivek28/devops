import docker

client = docker.from_env()
container = None

try:
    container = client.containers.run(
        "flask-apparmor",
        ports={"5000/tcp": 5001},
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True,
    )

    print("Testing restricted actions under my-apparmor-profile...")

    exit_code, output = container.exec_run(["cat", "/etc/passwd"])
    print(
        f"Attempt to read /etc/passwd: Exit Code {exit_code}, "
        f"Output: {output.decode(errors='replace').strip()}"
    )

    exit_code, output = container.exec_run(["/bin/bash"])
    print(
        f"Attempt to execute /bin/bash: Exit Code {exit_code}, "
        f"Output: {output.decode(errors='replace').strip()}"
    )

finally:
    if container is not None:
        container.stop()
        print("Container stopped.")
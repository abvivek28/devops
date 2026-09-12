import docker

client = docker.from_env()

print("Building image from Dockerfile...")
image, build_logs = client.images.build(path=".", tag="flask-apparmor")

for log in build_logs:
    if "stream" in log:
        for line in log["stream"].splitlines():
            print("[INFO]", line)

print("[INFO] Successfully built flask-apparmor")

print("\nRunning container with AppArmor profile...")
container = None

try:
    container = client.containers.run(
        "flask-apparmor",
        ports={"5000/tcp": 5001},
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True,
    )

    print("\nContainer started:", container.short_id)
    print("\nInspecting container to verify AppArmor profile...")
    container.reload()
    security_options = container.attrs["HostConfig"]["SecurityOpt"]
    print("AppArmor profile applied:", security_options)

finally:
    if container is not None:
        print("\nStopping the container...")
        container.stop()
        print("Container stopped.")
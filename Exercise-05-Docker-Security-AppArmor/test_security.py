import docker
from docker.errors import DockerException, NotFound

CONTAINER_NAME = "apparmor-secure-container"


def main():
    client = None

    try:
        client = docker.from_env()
        client.ping()

        try:
            container = client.containers.get(CONTAINER_NAME)
        except NotFound:
            print("ERROR: Secure container was not found.")
            print("Run apply_apparmor.py in a suitable Linux environment first.")
            return

        container.reload()

        if container.status != "running":
            print(f"ERROR: Container status is {container.status}.")
            print("Inspect the container logs before continuing.")
            return

        security_options = (
            container.attrs.get("HostConfig", {}).get("SecurityOpt") or []
        )

        print("Docker security configuration:")
        print(security_options or "No custom security options configured.")

        if not any("apparmor=" in option.lower() for option in security_options):
            print("\nRESULT: NOT VERIFIED")
            print("No custom AppArmor profile was requested.")
            return

        print("\nA custom AppArmor profile was requested.")
        print("This alone does not prove the profile is loaded or enforcing.")

        tests = [
            ("Read /etc/passwd", ["cat", "/etc/passwd"]),
            ("Execute /bin/bash", ["/bin/bash", "-c", "echo bash-executed"]),
        ]

        for description, command in tests:
            print(f"\nTest: {description}")
            result = container.exec_run(command)
            output = result.output.decode(errors="replace").strip()

            print(f"Exit code: {result.exit_code}")
            print(f"Output: {output or '(no output)'}")

            if result.exit_code == 0:
                print("Result: ACTION SUCCEEDED")
            else:
                print("Result: ACTION FAILED — cause not yet established")

        print(
            "\nFINAL STATUS: AppArmor enforcement is NOT VERIFIED by these "
            "command results alone. On Linux, check the active profile and "
            "kernel audit logs for matching AppArmor DENIED events."
        )

    except DockerException as error:
        print(f"Docker operation failed: {error}")

    finally:
        if client is not None:
            client.close()


if __name__ == "__main__":
    main()

import docker
from docker.errors import DockerException, NotFound

IMAGE_NAME = "flask-apparmor"
CONTAINER_NAME = "apparmor-secure-container"
PROFILE_NAME = "my-apparmor-profile"


def main():
    client = None

    try:
        client = docker.from_env()
        client.ping()
        print("Connected to Docker successfully.")

        print(f"\nBuilding image: {IMAGE_NAME}")
        image, build_logs = client.images.build(
            path=".",
            dockerfile="Exercise-05-Docker-Security-AppArmor/Dockerfile",
            tag=IMAGE_NAME,
            rm=True,
        )

        for log in build_logs:
            if "stream" in log:
                print(log["stream"], end="")

        print(f"\nImage built: {image.tags}")

        try:
            old_container = client.containers.get(CONTAINER_NAME)
            old_container.remove(force=True)
            print(f"Removed previous container: {CONTAINER_NAME}")
        except NotFound:
            pass

        security_options = client.info().get("SecurityOptions", [])
        print("\nDocker security options:")
        for option in security_options:
            print(f"  {option}")

        if not any("apparmor" in option.lower() for option in security_options):
            print(
                "\nRESULT: NOT VERIFIED — Docker does not report AppArmor "
                "support in its security options."
            )
            print(
                "This environment cannot verify custom AppArmor enforcement. "
                "Use a suitable Linux host."
            )
            return

        print(f"\nStarting container with profile: {PROFILE_NAME}")
        container = client.containers.run(
            IMAGE_NAME,
            name=CONTAINER_NAME,
            ports={"5000/tcp": 5055},
            detach=True,
            security_opt=[f"apparmor={PROFILE_NAME}"],
        )

        container.reload()

        print(f"Container started: {container.short_id}")
        print(f"Container status: {container.status}")

        actual_options = (
            container.attrs.get("HostConfig", {}).get("SecurityOpt") or []
        )
        print(f"Configured security options: {actual_options}")
        print(
            "\nNOTE: Docker configuration alone does not prove the profile "
            "is loaded or enforcing restrictions."
        )

    except DockerException as error:
        print(f"Docker operation failed: {error}")

    finally:
        if client is not None:
            client.close()


if __name__ == "__main__":
    main()

# Exercise 05: Docker Security with AppArmor and Python

## Objective

Containerize a Flask application, request an AppArmor profile through the
Docker SDK for Python, and test restricted operations inside the container.

## Technologies

- Python and Flask
- Docker
- Docker SDK for Python
- AppArmor on Linux

## Project Structure

    Exercise-05-Docker-Security-AppArmor/
    ├── app.py
    ├── requirements.txt
    ├── Dockerfile
    ├── my-apparmor-profile
    ├── apply_apparmor.py
    ├── test_security.py
    ├── README.md
    └── .gitignore

## 1. Build the Docker Image

Run from the repository root:

    docker build -t flask-apparmor ./Exercise-05-Docker-Security-AppArmor

## 2. Run the Flask Application

    docker run --rm -d --name flask-apparmor-demo -p 5055:5000 flask-apparmor

Test the endpoints:

    curl http://localhost:5055/
    curl http://localhost:5055/health

Stop the demonstration container:

    docker rm -f flask-apparmor-demo

## 3. Install Python Dependencies

From the repository root:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r Exercise-05-Docker-Security-AppArmor/requirements.txt

On Windows PowerShell, activate the environment with:

    .\.venv\Scripts\Activate.ps1

The Python scripts below should be run from the repository root.

## 4. Apply the AppArmor Profile Using Python

    python Exercise-05-Docker-Security-AppArmor/apply_apparmor.py

The script builds the image and checks the Docker daemon's reported security
options. When AppArmor is reported as available, it requests the custom profile
when starting the container.

Docker's security configuration records the requested options. It does not
independently prove that the profile is loaded or enforcing.

## 5. Configure AppArmor on Linux

AppArmor enforcement requires a suitable Linux environment. Docker Desktop on
macOS and Windows may not expose custom AppArmor enforcement to containers.

On a supported Ubuntu/Debian Linux host, install the utilities:

    sudo apt-get update
    sudo apt-get install -y apparmor apparmor-utils

Check the host status:

    sudo aa-status

Copy the profile to the system profile directory:

    sudo cp Exercise-05-Docker-Security-AppArmor/my-apparmor-profile /etc/apparmor.d/my-apparmor-profile

Validate and load it:

    sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile

Check the status again:

    sudo aa-status

If parsing fails, fix the profile before proceeding. The profile must also be
compatible with the actual container image and application. Restrictions on
system directories and executable paths can prevent the application from
starting, so test changes in a disposable environment.

## 6. Test Restricted Actions

After a container has started with the profile in a suitable Linux environment:

    python Exercise-05-Docker-Security-AppArmor/test_security.py

The script attempts to:
1. Read `/etc/passwd`.
2. Execute `/bin/bash`.

A non-zero exit code means an operation failed, but does not by itself prove
that AppArmor blocked it. Check executable availability, the active profile,
and Linux kernel audit logs for matching AppArmor `DENIED` events.

For example:

    sudo journalctl -k --since "10 minutes ago" | grep -i apparmor

Depending on the distribution, relevant events may instead be recorded in
`/var/log/syslog` or `/var/log/audit/audit.log`.

## Platform Limitation

The Docker image has been built on macOS, but custom AppArmor enforcement was
not verified in this Docker Desktop environment. Use a suitable Linux host or
virtual machine for enforcement tests. On Windows, do not assume that Docker
Desktop or WSL automatically provides a usable custom AppArmor environment.

## Questions and Answers

### 1. What is the purpose of using AppArmor with Docker containers?

AppArmor provides mandatory access control for Linux processes. It confines
applications according to defined security policies, adding a layer of
protection alongside Docker's container isolation.

### 2. How do AppArmor profiles help secure a Docker container?

Profiles define permitted and denied operations involving files, executable
programs, capabilities, and supported network behavior. This limits what an
application can access or do if it is compromised.

### 3. Why restrict access to `/etc/` and `/var/`?

These directories may contain system configuration, credentials, logs, and
other sensitive information. Restricting unnecessary access reduces the
potential impact of a compromised application. Policies must still permit
the legitimate operations the application needs.

### 4. What other capabilities can be restricted using AppArmor?

AppArmor can restrict capabilities such as `CAP_SYS_ADMIN`, as well as file
access, executable operations, and supported network behavior. The exact
restrictions depend on the policy and application requirements.

### 5. How can you verify that an AppArmor profile is applied?

Inspect the Docker container's security options, check active profiles using
`aa-status`, and examine Linux kernel audit logs for matching AppArmor denial
events. Docker configuration alone does not prove actual enforcement.

## Verification Status

The Docker image build and Python syntax checks succeeded on macOS. Custom
AppArmor enforcement remains unverified and must be demonstrated on a suitable
Linux host before the security tests can be marked as passed.

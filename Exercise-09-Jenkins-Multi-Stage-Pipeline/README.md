# Exercise 9 — Jenkins Multi-Stage Pipeline

## Objective
Automate the build, test, and deployment preparation stages for a Python Flask application.

## Files
- `app.py` — Flask application.
- `requirements.txt` — Python dependencies.
- `test_app.py` — unit test for the home route.
- `Jenkinsfile` — declarative Jenkins pipeline.

## Pipeline stages
1. Build — install Python dependencies.
2. Test — execute unit tests.
3. Deploy — copy the application files to `python-app-deploy` in the Jenkins workspace.

## Expected test result
The home route returns HTTP 200 and:
`Hello, Jenkins Multi-Stage Pipeline!`

## Jenkins setup
Create a Pipeline job and select **Pipeline script from SCM**, choose Git, and enter the repository URL. Set the script path to:
`Exercise-09-Jenkins-Multi-Stage-Pipeline/Jenkinsfile`

The Jenkins runtime must have Python 3 and pip installed for the pipeline to run.

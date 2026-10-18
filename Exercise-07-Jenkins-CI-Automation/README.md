# Exercise 7 — Jenkins CI Automation

## Objective
Understand Continuous Integration (CI) and use Jenkins to execute an automated pipeline.

## Concepts Covered
- Continuous Integration and its benefits
- Jenkins jobs, builds, pipelines, and plugins
- Pipeline stages and automated execution
- Build status and console output

## Implementation
Created a Jenkins Pipeline job named `Exercise-07-CI-Automation`.

The pipeline contains three stages:
1. **Checkout** — prints the exercise details.
2. **Build** — verifies the build stage executes.
3. **Test** — prints the CI check result.

## Verification
- Jenkins is running at http://localhost:8080.
- Build #1 completed successfully.
- Build duration: approximately 2.3 seconds.
- A green success indicator was visible in Jenkins.

## Run
Open Jenkins, select `Exercise-07-CI-Automation`, and click **Build Now**.

## Note
The current pipeline demonstrates Jenkins stage execution. It does not yet perform a Git checkout, compile an application, or run automated unit tests.

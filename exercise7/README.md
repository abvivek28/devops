# Exercise 7: Introduction to Continuous Integration (CI) and Jenkins Installation

## Objective
Understand the fundamentals of Continuous Integration (CI), explore popular CI/CD tools, and install Jenkins using Docker. Access the Jenkins dashboard and complete the initial setup.

## 1. Introduction to Continuous Integration

Continuous Integration is a software development practice in which developers frequently integrate code changes into a shared repository. Automated builds and tests help identify integration issues early and provide rapid feedback.

### Key Features of CI
- **Frequent Integration:** Regularly merge code changes into a shared repository.
- **Automated Builds:** Build the application automatically after code changes.
- **Automated Testing:** Run tests to validate application functionality.
- **Immediate Feedback:** Identify errors early and simplify debugging.

### Benefits of CI
- Early bug detection
- Improved collaboration
- Faster development cycles
- Improved software quality and reduced regressions

### CI Workflow
1. A developer commits and pushes code to a version control system.
2. The CI server detects the changes and triggers a build.
3. Automated tests validate the code.
4. The CI server reports the build and test results.

## 2. Overview of CI/CD Tools

Popular tools used for continuous integration and delivery include:

| Tool | Key Features |
|---|---|
| GitLab CI/CD | Integrated pipelines and YAML-based configuration |
| CircleCI | Container-based builds, parallelism, and caching |
| Travis CI | Automated builds and testing |
| Bamboo | Integration with Atlassian tools |
| TeamCity | Build management and plugin support |
| Azure DevOps | CI/CD pipelines and Microsoft ecosystem integration |
| GitHub Actions | Repository-integrated workflow automation |
| Spinnaker | Multi-cloud application delivery |
| Buildkite | Self-hosted build agents with cloud-managed pipelines |
| Drone | Container-based pipeline execution |

## 3. Introduction to Jenkins

Jenkins is an open-source automation server used to automate software building, testing, and deployment. It supports Continuous Integration and Continuous Delivery through pipelines and plugins.

### Key Jenkins Concepts
- **Job/Project:** A task or process executed by Jenkins.
- **Build:** An execution of a job.
- **Pipeline:** A sequence of automated stages.
- **Plugins:** Extensions that integrate Jenkins with other tools.
- **Nodes:** Machines that execute Jenkins workloads, including the controller and agents.

## 4. Install Jenkins Using Docker

Run the following command to download the Jenkins image and start a container:

```powershell
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
```

**Purpose:** Runs Jenkins in a Docker container and publishes its web interface on port `8080` and its agent communication port on `50000`.

### Verify the Container

```powershell
docker ps -a
```

**Purpose:** Confirms that the Jenkins container has been created and checks its status and port mappings.

## 5. Retrieve the Initial Administrator Password

Open a shell inside the Jenkins container:

```powershell
docker exec -it jenkins bash
```

Retrieve the initial administrator password:

```bash
cat /var/jenkins_home/secrets/initialAdminPassword
```

Copy the password displayed in the terminal, then exit the container:

```bash
exit
```

**Purpose:** Retrieves the initial password required to unlock Jenkins during the first-time setup.

## 6. Access Jenkins

Open the following URL in a web browser:

[http://localhost:8080](http://localhost:8080)

Enter the initial administrator password to unlock Jenkins.

Complete the initial setup by installing the recommended plugins or selecting the required plugins, then create the administrator account and finish the configuration.

**Purpose:** Completes the initial Jenkins configuration and provides access to the Jenkins dashboard.

## Expected Result
- Jenkins is running inside a Docker container.
- The initial administrator password is retrieved successfully.
- The Jenkins web interface is accessible at `http://localhost:8080`.
- The initial setup is completed and the Jenkins dashboard is available.

## Conclusion
Successfully explored the fundamentals of Continuous Integration, reviewed popular CI/CD tools, and installed Jenkins using Docker. Retrieved the initial administrator password and completed the initial Jenkins setup to prepare the environment for automated build and deployment pipelines.
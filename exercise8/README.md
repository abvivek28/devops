# Exercise 8: Creating a Hello World Jenkins Job

## Objective
Create a GitHub repository containing a shell script, configure Jenkins to retrieve the script from the repository, execute it through a Freestyle project, and verify the build output.

## Prerequisites
- Git installed and configured
- GitHub account
- Jenkins installed and running
- Jenkins Git plugin installed
- Access to a Jenkins build environment that supports shell execution

## Implementation

### 1. Create a GitHub Repository

Create a public repository named `devops-sample-code` on GitHub.

Generate a fine-grained Personal Access Token (PAT) if authentication is required for Git operations.

**Purpose:** Provides a remote repository to store the shell script and make it accessible to Jenkins.

### 2. Create the Shell Script

Create a file named `hello-world.sh`:

```bash
#!/bin/bash
echo "Hello, Jenkins!"
```

Make the script executable:

```bash
chmod +x hello-world.sh
```

**Purpose:** Defines a simple shell script that prints a message when executed.

### 3. Initialize the Git Repository

Configure Git if it has not already been configured:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Initialize the repository and stage the script:

```bash
git init
git add hello-world.sh
git status
```

Commit the changes:

```bash
git commit -m "Add hello-world.sh"
```

**Purpose:** Tracks the script using Git and creates the initial commit.

### 4. Connect the Local Repository to GitHub

Add the GitHub repository as the remote:

```bash
git remote add origin https://github.com/<your-GitHub-username>/devops-sample-code.git
```

Push the commit to GitHub:

```bash
git branch -M main
git push -u origin main
```

Replace `<your-GitHub-username>` with your GitHub username.

**Purpose:** Publishes the script to GitHub so Jenkins can retrieve it during the build.

### 5. Verify the Repository

Open the GitHub repository and confirm that `hello-world.sh` is present.

**Purpose:** Ensures the script is available in the remote repository before configuring Jenkins.

### 6. Access Jenkins

Open Jenkins in your browser:

[http://localhost:8080](http://localhost:8080)

Log in using your Jenkins credentials.

**Purpose:** Accesses the Jenkins dashboard to create and configure the job.

### 7. Create a Freestyle Project

1. Click **New Item** on the Jenkins dashboard.
2. Enter `HelloWorld` as the job name.
3. Select **Freestyle project**.
4. Click **OK**.

**Purpose:** Creates a Jenkins job that can retrieve source code and execute build steps.

### 8. Configure the Jenkins Job

Under **General**, add the description:

```text
Hello World! Jenkins job.
```

Under **Source Code Management**:

1. Select **Git**.
2. Enter the repository URL:

```text
https://github.com/<your-GitHub-username>/devops-sample-code.git
```

3. Configure credentials if the repository requires authentication.

Under **Build Steps**:

1. Click **Add build step**.
2. Select **Execute shell**.
3. Enter the following command:

```bash
sh hello-world.sh
```

**Purpose:** Configures Jenkins to retrieve the script from GitHub and execute it during the build.

### 9. Save and Execute the Job

Click **Save**, then select **Build Now** on the job page.

**Purpose:** Starts the Jenkins job and executes the configured build step.

### 10. Verify the Build Output

1. Open the job's **Build History**.
2. Select the latest build number.
3. Click **Console Output**.

The output should include:

```text
Hello, Jenkins!
Finished: SUCCESS
```

**Purpose:** Confirms that Jenkins successfully executed the shell script.

## Expected Result
- A public GitHub repository contains `hello-world.sh`.
- A Jenkins Freestyle project retrieves the script from GitHub.
- The build executes the shell script successfully.
- The Console Output displays `Hello, Jenkins!`.
- The Jenkins build finishes with a `SUCCESS` status.

## Conclusion
Successfully integrated GitHub with Jenkins by configuring a Freestyle project to retrieve and execute a shell script. Verified the automated build through Jenkins Console Output, demonstrating the basic principles of source code integration and build automation.
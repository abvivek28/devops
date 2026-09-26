# Exercise 9: Jenkins Multi-Stage Pipeline — Deploying a Python Application

## Objective

To design and execute a multi-stage Jenkins CI/CD pipeline for a Python Flask application. The pipeline automates dependency setup, unit testing, deployment to a designated directory, application execution, and post-deployment testing.

## Scenario

A Python Flask application is integrated with Jenkins to automate the following stages:

1. **Build:** Set up the Python environment and install dependencies.
2. **Test:** Execute unit tests to verify application functionality.
3. **Deploy:** Copy the application to a deployment directory.
4. **Run Application:** Start the deployed Flask application.
5. **Test Application:** Verify the deployed application using the test suite.

## Prerequisites

- Jenkins running locally or on a server.
- Pipeline plugin installed in Jenkins.
- Git and a GitHub repository.
- Python 3 and pip installed in the Jenkins execution environment.
- Required Python dependencies specified in `requirements.txt`.

## Implementation

### Step 1: Create the Python Application

Create a project directory and navigate into it.

```bash
mkdir python-flask-app
cd python-flask-app
```

Create the following files.

**`app.py`**

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Jenkins Multi-Stage Pipeline!"

if __name__ == "__main__":
    app.run(debug=True)
```

**`requirements.txt`**

```text
flask==2.1.2
```

**`test_app.py`**

```python
import unittest
from app import app

class TestApp(unittest.TestCase):
    def test_home(self):
        tester = app.test_client()
        response = tester.get("/")

        print(response.data.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.decode("utf-8"),
            "Hello, Jenkins Multi-Stage Pipeline!"
        )

if __name__ == "__main__":
    unittest.main()
```

### Step 2: Create the Jenkinsfile

Create a file named `Jenkinsfile` in the project root. It defines the pipeline stages and the actions Jenkins must execute.

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    . venv/bin/activate
                    python -m unittest discover -s .
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh '''
                    mkdir -p "${WORKSPACE}/python-app-deploy"
                    cp "${WORKSPACE}/app.py" "${WORKSPACE}/python-app-deploy/"
                '''
            }
        }

        stage('Run Application') {
            steps {
                echo 'Running application...'
                sh '''
                    . venv/bin/activate
                    nohup python "${WORKSPACE}/python-app-deploy/app.py" \
                        > "${WORKSPACE}/python-app-deploy/app.log" 2>&1 &
                    echo $! > "${WORKSPACE}/python-app-deploy/app.pid"
                '''
            }
        }

        stage('Test Application') {
            steps {
                echo 'Testing application...'
                sh '''
                    . venv/bin/activate
                    python test_app.py
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for more details.'
        }
    }
}
```

### Step 3: Push the Project to GitHub

Initialize Git, commit the application files, and push them to the repository.

```bash
git init
git add app.py requirements.txt test_app.py Jenkinsfile
git commit -m "Add Python Flask application and Jenkins pipeline"
git branch -M main
git remote add origin https://github.com/<your-GitHub-username>/devops-sample-code.git
git push -u origin main
```

Replace the repository URL with your own GitHub repository URL.

### Step 4: Configure the Jenkins Pipeline

1. Open Jenkins at `http://localhost:8080`.
2. Click **New Item**.
3. Enter `Python-MultiStage-Pipeline` as the job name.
4. Select **Pipeline** and click **OK**.
5. Under the Pipeline section, select **Pipeline script from SCM**.
6. Choose **Git** as the SCM.
7. Enter the GitHub repository URL and configure credentials if required.
8. Set the branch to `*/main`.
9. Set the Script Path to `Jenkinsfile`.
10. Click **Save**.

### Step 5: Configure Python in the Jenkins Container

If Jenkins runs inside Docker and Python is unavailable, open PowerShell and identify the running Jenkins container.

```powershell
docker ps
```

Open a shell as the root user inside the container.

```powershell
docker exec -it -u root jenkins bash
```

Install the required packages inside the container.

```bash
apt-get update
apt-get install -y python3 python3-pip python3-venv
```

Exit the container shell and run the Jenkins pipeline again.

**Note:** Installing packages directly inside a running container is not persistent if the container is removed and recreated. A custom Jenkins image with Python preinstalled is a more durable solution.

### Step 6: Execute the Pipeline

1. Open the `Python-MultiStage-Pipeline` job.
2. Click **Build Now**.
3. Open the latest build from Build History.
4. Select **Console Output** to inspect the execution logs.
5. Verify that all stages complete successfully.

## Expected Outcome

The pipeline should execute all five stages in sequence.

| Stage | Expected Result |
|---|---|
| Build | Creates a virtual environment and installs Flask dependencies. |
| Test | Runs the unit tests successfully. |
| Deploy | Copies `app.py` into `python-app-deploy`. |
| Run Application | Starts the Flask application in the background. |
| Test Application | Executes the test suite and verifies the expected response. |

The console output should include:

```text
Ran 1 test

OK
Hello, Jenkins Multi-Stage Pipeline!
Pipeline completed successfully!
Finished: SUCCESS
```

## Additional Enhancements

### Code Quality Analysis

Integrate a code quality stage using Flake8.

```groovy
stage('Code Quality') {
    steps {
        sh '''
            . venv/bin/activate
            pip install flake8
            flake8 app.py test_app.py
        '''
    }
}
```

### Docker Deployment

Extend the pipeline to build a Docker image and run the Flask application inside a container.

### Notifications

Configure email or Slack notifications to report pipeline success or failure.

## Conclusion

Successfully designed and configured a Jenkins multi-stage pipeline for a Python Flask application. The pipeline automates dependency installation, unit testing, deployment, application execution, and post-deployment testing, demonstrating the core principles of continuous integration and continuous delivery (CI/CD).
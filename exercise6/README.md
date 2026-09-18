# Exercise 6: Real-Time Operations Monitoring and Alerting

## Objective
Develop a real-time monitoring and alerting system for a delivery service using Python, Prometheus, Grafana, Docker, and Jenkins. Simulate delivery metrics, visualize operational performance, configure threshold-based alerts, and automate the deployment workflow using a Jenkins pipeline.

## Scenario
The delivery service requires real-time insights into total deliveries, pending orders, deliveries in transit, and average delivery time. Prometheus collects the metrics, Grafana visualizes them, and Jenkins automates the application deployment and monitoring setup.

## Implementation

### 1. Set Up the Project

Create the project directory and install the required Python package.

```bash
mkdir delivery_monitoring
cd delivery_monitoring
pip install prometheus-client
```

**Purpose:** Creates the project workspace and installs the Prometheus client library for exposing application metrics.

### 2. Develop the Delivery Metrics Application

Create `delivery_metrics.py` to simulate delivery activity and expose metrics on port `8000`.

The application defines the following metrics:
- `total_deliveries` — Total number of deliveries.
- `pending_deliveries` — Number of pending deliveries.
- `on_the_way_deliveries` — Number of deliveries in transit.
- `average_delivery_time` — Observations of delivery time in seconds.

Run the application:

```bash
python delivery_metrics.py
```

Verify the metrics endpoint:

```bash
curl http://localhost:8000/metrics
```

**Purpose:** Simulates changing delivery statistics and exposes them in Prometheus-compatible format for collection.

### 3. Configure Prometheus

Create `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "delivery_service"
    static_configs:
      - targets: ["172.17.0.1:8000"]

rule_files:
  - /etc/prometheus/alert_rules.yml
```

**Purpose:** Configures Prometheus to collect metrics from the delivery application and defines the location of the alert rules.

Start Prometheus with the configuration files mounted:

```bash
docker run -d --name prometheus --network=host \
  -v ./prometheus.yml:/etc/prometheus/prometheus.yml \
  -v ./alert_rules.yml:/etc/prometheus/alert_rules.yml \
  prom/prometheus
```

Access the Prometheus interface at [http://localhost:9090](http://localhost:9090).

**Note:** The example target `172.17.0.1:8000` is specific to certain Linux Docker networking setups. Adjust the target address and networking configuration for your environment.

### 4. Configure Alert Rules

Create `alert_rules.yml`:

```yaml
groups:
  - name: delivery_alerts
    rules:
      - alert: HighPendingDeliveries
        expr: pending_deliveries > 10
        for: 15s
        labels:
          severity: warning
        annotations:
          summary: "High pending deliveries"
          description: "Pending deliveries are above 10 for 15 seconds."

      - alert: HighAverageDeliveryTime
        expr: (average_delivery_time_sum / average_delivery_time_count) > 30
        labels:
          severity: critical
        annotations:
          summary: "High average delivery time"
          description: "Average delivery time exceeds 30 seconds."
```

**Purpose:** Defines warning and critical alerts based on pending delivery counts and average delivery time.

Verify the configured targets and alerts through the Prometheus web interface.

### 5. Set Up Grafana

Start Grafana:

```bash
docker run -d --name grafana -p 3000:3000 grafana/grafana
```

Access Grafana at [http://localhost:3000](http://localhost:3000).

Log in using the default credentials for a new installation:

- Username: `admin`
- Password: `admin`

Add Prometheus as a data source and configure its URL according to the networking setup. Save the configuration and test the connection.

Create a dashboard with the following panels:

1. **Total Deliveries:** `total_deliveries`
2. **Pending Deliveries:** `pending_deliveries`
3. **On-the-Way Deliveries:** `on_the_way_deliveries`
4. **Average Delivery Time:** `average_delivery_time_sum / average_delivery_time_count`

**Purpose:** Visualizes delivery metrics and trends through a centralized monitoring dashboard.

### 6. Configure Jenkins

Start Jenkins in Docker:

```bash
docker run -d -p 8080:8080 -p 50000:50000 \
  --name jenkins \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

Access Jenkins at [http://localhost:8080](http://localhost:8080) and complete the initial setup.

Create a `Jenkinsfile` defining the pipeline stages:

- **Pre-check Docker:** Verify Docker availability and daemon status.
- **Setup Workspace:** Prepare the application and configuration files.
- **Build Docker Image:** Build the delivery metrics application image.
- **Run Application:** Start the metrics application container.
- **Run Prometheus and Grafana:** Start the monitoring services.

Create a Pipeline job in Jenkins and configure it to use the `Jenkinsfile`. Execute the pipeline and inspect the build logs.

**Purpose:** Automates application setup, container image building, and execution of the monitoring stack.

### 7. Simulate and Verify Alerts

Modify the pending delivery generation in `delivery_metrics.py` to increase the number of pending deliveries.

```python
pending = random.randint(50, 100)
```

Restart the metrics application and verify the results in Prometheus and Grafana.

**Purpose:** Generates values above the configured threshold to test whether Prometheus evaluates and activates the expected alerts.

## Expected Result
- The Python application exposes delivery metrics at port `8000`.
- Prometheus collects metrics from the configured target.
- Alert rules detect high pending deliveries and elevated average delivery times.
- Grafana displays delivery metrics through a monitoring dashboard.
- Jenkins executes the configured pipeline and records build logs.
- Increasing pending delivery values allows the warning alert to be tested.

## Key Learnings
- **Metrics Instrumentation:** Expose application metrics using the Prometheus Python client.
- **Monitoring:** Collect and query metrics using Prometheus.
- **Visualization:** Build dashboards with Grafana.
- **Alerting:** Configure threshold-based alert rules.
- **CI/CD Automation:** Use Jenkins pipelines to automate application and monitoring setup.
- **Operational Observability:** Monitor delivery performance and identify potential operational issues.

## Conclusion
Successfully designed a real-time delivery monitoring and alerting workflow using Python, Prometheus, Grafana, Docker, and Jenkins. The exercise demonstrates metrics collection, dashboard visualization, threshold-based alerting, and pipeline automation for operational monitoring.
import pulumi
import pulumi_kubernetes as k8s

# Define Kubernetes resources
nginx_deployment = k8s.apps.v1.Deployment(
    "nginx-deployment",
    metadata={
        "name": "nginx-deployment",
    },
    spec={
        "replicas": 4,
        "selector": {
            "matchLabels": {"app": "nginx"},
        },
        "template": {
            "metadata": {"labels": {"app": "nginx"}},
            "spec": {
                "containers": [
                    {
                        "name": "nginx",
                        "image": "nginx-alpine",  # Use the Docker image you built
                        "ports": [{"containerPort": 80}],
                        "resources": {
                            "requests": {"cpu": "0.1", "memory": "64Mi"},
                            "limits": {"cpu": "0.5", "memory": "256Mi"},
                        },
                        "readinessProbe": {
                            "httpGet": {
                                "path": "/",
                                "port": 80
                            },
                            "initialDelaySeconds": 10,
                            "periodSeconds": 5
                        }
                    }
                ],
            },
        },
    },
)

nginx_service = k8s.core.v1.Service(
    "nginx-service",
    metadata={"name": "nginx-service"},
    spec={
        "selector": {"app": "nginx"},
        "ports": [{"port": 80, "targetPort": 80}],
    },
)

# Export the service IP
pulumi.export("nginx-service-ip", nginx_service.spec["clusterIP"])

# Define a PVC (Persistent Volume Claim) if needed

# Create a Pulumi stack and set config values if needed
pulumi.export("namespace", "default")

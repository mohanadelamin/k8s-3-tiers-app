This is a working example of a Kubernetes 3-tier flask application, with Postgres as the database and the nginx reverse proxy as frontend.

## Setup 
The setup look like the following:
```bash
                      +-------------+
                      |             |
                  +---+    Nginx    +---+
                  |   |             |   |
                  |   +-------------+   |
                  |                     |
+-------------+   |                     |   +-------------+                           +-------------+
|             |   |                     |   |             |                           |             |
|             |   |   +-------------+   |   |             |      +-------------+      |             |      +-------------+
|             |   |   |             |   |   |             |      |             |      |             |      |             |
| Web-Service +-------+    Nginx    +-------+ App-Service +------+  Flask App  +------+ DB-Service  +------+ Postgres DB |
|  NodePort   |   |   |             |   |   |  ClusterIP  |      |             |      |  ClusterIP  |      |             |
|             |   |   +-------------+   |   |             |      +-------------+      |             |      +-------------+
|             |   |                     |   |             |                           |             |
+-------------+   |                     |   +-------------+                           +-------------+
                  |                     |
                  |   +-------------+   |
                  |   |             |   |
                  +---+    Nginx    +---+
                      |             |
                      +-------------+
```

## Usage

1. Clone the repo using:
```bash
git clone https://github.com/mohanadelamin/k8s-3-tiers-app
```

2. Create name-space (All the yaml files has 'namespace: 3-tiers-app'. Modify that if needed)
```bash
$ kubectl create namespace 3-tiers-app
```

3. Create the Postgress DB deployment and service.
```bash
$ kubectl create -f db-deployment.yaml
$ kubectl create -f db-service.yaml
```

4. Create the Flask App Deployment and Service. (Flask app is based on customer image 'melamin/flaskapp:v1.0').
```bash
$ kubectl create -f app-deployment.yaml
$ kubectl create -f app-service.yaml
```

5. Create config map for the NGINX configuration.
```bash
$ kubectl create -f web-configmap.yaml
```

6. Create the NGINX Deployment and Service.
```bash
$ kubectl create -f web-deployment.yaml
$ kubectl create -f web-service.yaml
```

## Example output

![Example output](https://raw.githubusercontent.com/mohanadelamin/k8s-3-tier3-app/master/exmple_output.png)


The Dockerfile for and script for the flaskapp can be found in the flaskapp folder.

# Exercise 1: Kubernetes - Hello Pod

## Aim
Deploy an Nginx web server in a Kubernetes Pod using Minikube and expose it through a NodePort Service.

## Tools Used
- Docker Desktop
- Minikube
- Kubernetes
- kubectl
- Git and GitHub

## Procedure
1. Started Docker Desktop.
2. Started the Minikube cluster using the Docker driver.
3. Verified the Kubernetes node reached Ready status.
4. Created a Pod named hello-k8s using the nginx image.
5. Exposed the Pod through a NodePort Service on port 80.
6. Opened the application using minikube service hello-k8s.

## Commands Executed
- minikube start --driver=docker
- kubectl get nodes
- kubectl run hello-k8s --image=nginx --port=80
- kubectl get pods
- kubectl expose pod hello-k8s --type=NodePort --port=80
- kubectl get services
- minikube service hello-k8s

## Result
Successfully deployed Nginx on Kubernetes. The browser displayed the Nginx welcome page.

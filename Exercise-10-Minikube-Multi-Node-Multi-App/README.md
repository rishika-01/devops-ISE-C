# Exercise 10: Minikube Multi-Node Multi-App Deployment

- Minikube profile: devops-multinode (3 nodes)
- Product Catalog: 2 replicas, GET /products
- Shopping Cart: 3 replicas, GET and POST /cart
- Both apps are Flask applications containerized with Docker.
- Kubernetes Deployments use pod anti-affinity to distribute replicas across nodes.

## Build images
```bash
docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .
```

# AI Recommendation System Platform (K8s + Istio + GitOps)

Платформа для системы рекомендаций, развернутая в кластере Kubernetes с использованием Service Mesh и принципов GitOps.

## Архитектура

- **Infrastructure:** Minikube (K8s), Cilium CNI.
- **GitOps:** ArgoCD (App of Apps pattern).
- **Service Mesh:** Istio (Circuit Breaker, Rate Limiting, mTLS).
- **IaC:** Terraform (Namespaces, RBAC, Secrets).
- **Configuration:** Ansible (Kafka & MongoDB deployment).
- **Observability:** Prometheus, Grafana, Kiali.

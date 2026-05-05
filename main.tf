provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_namespace" "recsys_namespace" {
  metadata {
    name = "recsys-prod"
    labels = {
      name = "recsys-prod"
    }
  }
}

resource "kubernetes_service_account" "rec_service_sa" {
  metadata {
    name      = "recommendation-sa"
    namespace = kubernetes_namespace.recsys_namespace.metadata[0].name
  }
}

resource "kubernetes_secret" "app_secrets" {
  metadata {
    name      = "backend-secrets"
    namespace = kubernetes_namespace.recsys_namespace.metadata[0].name
  }

  data = {
    "REDIS_PASSWORD" = "very-secret-password"
  }

  type = "Opaque"
}
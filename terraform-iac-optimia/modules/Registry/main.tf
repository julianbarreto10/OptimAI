# Crear un Artifact Registry de tipo Docker
resource "google_artifact_registry_repository" "isbn_users_ms" {
  repository_id = "optimia-drivers-ms"                   # ID único del repositorio en Artifact Registry
  format        = "DOCKER"                          # Tipo de repositorio: Docker
  location      = "us-east4"                        # Región donde se crea el repositorio
  mode          = "STANDARD_REPOSITORY"                        # Modo estándar; también se puede usar "VPCSC" para compatibilidad con VPC Service Controls
  description   = "Registro de contenedores Docker para el servicio drivers-ms"  # Descripción del repositorio
}

resource "google_artifact_registry_repository" "isbn_users_ms" {
  repository_id = "optimia-routing-ms"                   # ID único del repositorio en Artifact Registry
  format        = "DOCKER"                          # Tipo de repositorio: Docker
  location      = "us-east4"                        # Región donde se crea el repositorio
  mode          = "STANDARD_REPOSITORY"                        # Modo estándar; también se puede usar "VPCSC" para compatibilidad con VPC Service Controls
  description   = "Registro de contenedores Docker para el servicio de enrutamiento"  # Descripción del repositorio
}

resource "google_artifact_registry_repository" "isbn_users_ms" {
  repository_id = "optimia-bi-ms"                   # ID único del repositorio en Artifact Registry
  format        = "DOCKER"                          # Tipo de repositorio: Docker
  location      = "us-east4"                        # Región donde se crea el repositorio
  mode          = "STANDARD_REPOSITORY"                        # Modo estándar; también se puede usar "VPCSC" para compatibilidad con VPC Service Controls
  description   = "Registro de contenedores Docker para el servicio de modulo bi"  # Descripción del repositorio
}

resource "google_artifact_registry_repository" "isbn_users_ms" {
  repository_id = "optimia-ag"                   # ID único del repositorio en Artifact Registry
  format        = "DOCKER"                          # Tipo de repositorio: Docker
  location      = "us-east4"                        # Región donde se crea el repositorio
  mode          = "STANDARD_REPOSITORY"                        # Modo estándar; también se puede usar "VPCSC" para compatibilidad con VPC Service Controls
  description   = "Registro de contenedores Docker para el servicio API gateway"  # Descripción del repositorio
}

resource "google_artifact_registry_repository" "isbn_users_ms" {
  repository_id = "optimia-wa"                   # ID único del repositorio en Artifact Registry
  format        = "DOCKER"                          # Tipo de repositorio: Docker
  location      = "us-east4"                        # Región donde se crea el repositorio
  mode          = "STANDARD_REPOSITORY"                        # Modo estándar; también se puede usar "VPCSC" para compatibilidad con VPC Service Controls
  description   = "Registro de contenedores Docker para el servicio Front End"  # Descripción del repositorio
}
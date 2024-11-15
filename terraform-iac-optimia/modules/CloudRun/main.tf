# Crear un servicio de Cloud Run
resource "google_cloud_run_service" "optimia-drivers-ms" {
  name     = "optimia-drivers-ms"                         # Nombre del servicio de Cloud Run
  location = "us-east4"                              # Región donde se desplegará el servicio

  template {
    spec {
      containers {
        image = "us-east4-docker.pkg.dev/project-cbse-2024/optimia-drivers-ms/optimia-drivers-ms@sha256:95a89b13a8e039d96048c915e697598edb13cb8542260abead45a739ee179de7"  # URL de la imagen de contenedor en Artifact Registry
        ports {
          container_port = 4000                      # Puerto del contenedor expuesto
        }

        resources {
          limits = {
            cpu    = "1"                             # Límite de CPU (1 vCPU)
            memory = "512Mi"                         # Límite de memoria (512 MiB)
          }
        }

        env {
          name  = "DB_USER"                          # Variable de entorno para el usuario de la base de datos
          value = "optimia"
        }
        env {
          name  = "DB_PASSWORD"                      # Variable de entorno para la contraseña de la base de datos
          value = "123"
        }
        env {
          name  = "DB_HOST"                          # Variable de entorno para la IP pública de la base de datos
          value = "34.48.165.248"                       # Reemplazar "IP_ADDRESS" por la IP pública de Cloud SQL
        }
        env {
          name  = "DB_NAME"                          # Variable de entorno para el nombre de la base de datos
          value = "optimia-drivers-db"
        }
      }
    }
  }

  traffic {
    percent         = 100                            # Enviar el 100% del tráfico a la última revisión
    latest_revision = true                           # Dirige el tráfico a la última revisión desplegada
  }

  autogenerate_revision_name = true                  # Habilitar la generación automática de nombres para cada revisión

  
}

# Configuración de IAM para permitir invocaciones no autenticadas
resource "google_cloud_run_service_iam_member" "allow_unauthenticated" {
  location = google_cloud_run_service.optimia-drivers-ms.location  # Ubicación del servicio Cloud Run
  service  = google_cloud_run_service.optimia-drivers-ms.name      # Nombre del servicio Cloud Run al que aplica el IAM
  role     = "roles/run.invoker"                             # Rol que permite invocar el servicio
  member   = "allUsers"                                      # Permitir acceso no autenticado a todos los usuarios
}

# Crear un servicio de Cloud Run
resource "google_cloud_run_service" "optimia-routing-ms" {
  name     = "optimia-routing-ms"                         # Nombre del servicio de Cloud Run
  location = "us-east4"                              # Región donde se desplegará el servicio

  template {
    spec {
      containers {
        image = "us-east4-docker.pkg.dev/project-cbse-2024/optimia-drivers-ms/optimia-drivers-ms@sha256:95a89b13a8e039d96048c915e697598edb13cb8542260abead45a739ee179de7"  # URL de la imagen de contenedor en Artifact Registry
        ports {
          container_port = 8080                      # Puerto del contenedor expuesto
        }

        resources {
          limits = {
            cpu    = "1"                             # Límite de CPU (1 vCPU)
            memory = "512Mi"                         # Límite de memoria (512 MiB)
          }
        }

        env {
          name  = "URL_DB_INSERT"                          # Variable de entorno para el usuario de la base de datos
          value = "https://routing-ms-367948167762.us-east4.run.app/routing-ms"
        }
      }
    }
  }

  traffic {
    percent         = 100                            # Enviar el 100% del tráfico a la última revisión
    latest_revision = true                           # Dirige el tráfico a la última revisión desplegada
  }

  autogenerate_revision_name = true                  # Habilitar la generación automática de nombres para cada revisión

  
}

# Configuración de IAM para permitir invocaciones no autenticadas
resource "google_cloud_run_service_iam_member" "allow_unauthenticated" {
  location = google_cloud_run_service.optimia-routing-ms.location  # Ubicación del servicio Cloud Run
  service  = google_cloud_run_service.optimia-routing-ms.name      # Nombre del servicio Cloud Run al que aplica el IAM
  role     = "roles/run.invoker"                             # Rol que permite invocar el servicio
  member   = "allUsers"                                      # Permitir acceso no autenticado a todos los usuarios
}

# Crear un servicio de Cloud Run
resource "google_cloud_run_service" "optimia-bi-ms" {
  name     = "optimia-bi-ms"                         # Nombre del servicio de Cloud Run
  location = "us-east4"                              # Región donde se desplegará el servicio

  template {
    spec {
      containers {
        image = "us-east4-docker.pkg.dev/project-cbse-2024/optimia-bi-ms/optimia-bi-ms@sha256:f878790a3cbb5cd52a522e69894c6688ee5f7421968405ac21630cd81f3d0157"  # URL de la imagen de contenedor en Artifact Registry
        ports {
          container_port = 8080                      # Puerto del contenedor expuesto
        }

        resources {
          limits = {
            cpu    = "1"                             # Límite de CPU (1 vCPU)
            memory = "512Mi"                         # Límite de memoria (512 MiB)
          }
        }

        env {
          name  = "URL_DB_GET"                          # Variable de entorno para el usuario de la base de datos
          value = "https://routing-ms-367948167762.us-east4.run.app/routing-ms"
        }
      }
    }
  }

  traffic {
    percent         = 100                            # Enviar el 100% del tráfico a la última revisión
    latest_revision = true                           # Dirige el tráfico a la última revisión desplegada
  }

  autogenerate_revision_name = true                  # Habilitar la generación automática de nombres para cada revisión

  
}

# Configuración de IAM para permitir invocaciones no autenticadas
resource "google_cloud_run_service_iam_member" "allow_unauthenticated" {
  location = google_cloud_run_service.optimia-bi-ms.location  # Ubicación del servicio Cloud Run
  service  = google_cloud_run_service.optimia-bi-ms.name      # Nombre del servicio Cloud Run al que aplica el IAM
  role     = "roles/run.invoker"                             # Rol que permite invocar el servicio
  member   = "allUsers"                                      # Permitir acceso no autenticado a todos los usuarios
}


# Crear un servicio de Cloud Run
resource "google_cloud_run_service" "optimia-ag" {
  name     = "optimia-ag"                         # Nombre del servicio de Cloud Run
  location = "us-east4"                              # Región donde se desplegará el servicio

  template {
    spec {
      containers {
        image = "us-east4-docker.pkg.dev/project-cbse-2024/optimia-ag/optimia-ag@sha256:467be9a0cbf27b651a17911943635da806604510a9a245ef2473329a5b3d80e7"  # URL de la imagen de contenedor en Artifact Registry
        ports {
          container_port = 8080                      # Puerto del contenedor expuesto
        }

        resources {
          limits = {
            cpu    = "1"                             # Límite de CPU (1 vCPU)
            memory = "512Mi"                         # Límite de memoria (512 MiB)
          }
        }

        env {
          name  = "OPTIMIA_DRIVERS_MS_API_URL"                          # Variable de entorno para el usuario de la base de datos
          value = "https://optimia-drivers-ms-367948167762.us-east4.run.app"
        }

        env {
          name  = "OPTIMIA_BI_MS_API_URL"                          # Variable de entorno para el usuario de la base de datos
          value = "https://optimia-bi-ms-367948167762.us-east4.run.app"
        }

        env {
          name  = "OPTIMIA_ROUTING_MS_API_URL"                          # Variable de entorno para el usuario de la base de datos
          value = "http://34.145.246.125:8080"
        }
      }
    }
  }

  traffic {
    percent         = 100                            # Enviar el 100% del tráfico a la última revisión
    latest_revision = true                           # Dirige el tráfico a la última revisión desplegada
  }

  autogenerate_revision_name = true                  # Habilitar la generación automática de nombres para cada revisión

  
}

# Configuración de IAM para permitir invocaciones no autenticadas
resource "google_cloud_run_service_iam_member" "allow_unauthenticated" {
  location = google_cloud_run_service.optimia-ag.location  # Ubicación del servicio Cloud Run
  service  = google_cloud_run_service.optimia-ag.name      # Nombre del servicio Cloud Run al que aplica el IAM
  role     = "roles/run.invoker"                             # Rol que permite invocar el servicio
  member   = "allUsers"                                      # Permitir acceso no autenticado a todos los usuarios
}


# Crear un servicio de Cloud Run
resource "google_cloud_run_service" "optimia-wa" {
  name     = "optimia-wa"                         # Nombre del servicio de Cloud Run
  location = "us-east4"                              # Región donde se desplegará el servicio

  template {
    spec {
      containers {
        image = "us-east4-docker.pkg.dev/project-cbse-2024/optimia-wa/optimia-wa@sha256:1c18be960da9c970defbf688742afc772128d31a698c56a2487d598dcb77e58b"  # URL de la imagen de contenedor en Artifact Registry
        ports {
          container_port = 80                        # Puerto del contenedor expuesto
        }

        resources {
          limits = {
            cpu    = "1"                             # Límite de CPU (1 vCPU)
            memory = "512Mi"                         # Límite de memoria (512 MiB)
          }
        }

        env {
          name  = "ISBN_AG_API_URL"                          # Variable de entorno para el usuario de la base de datos
          value = "https://optimia-ag-367948167762.us-east4.run.app"
        }

      }
    }
  }

  traffic {
    percent         = 100                            # Enviar el 100% del tráfico a la última revisión
    latest_revision = true                           # Dirige el tráfico a la última revisión desplegada
  }

  autogenerate_revision_name = true                  # Habilitar la generación automática de nombres para cada revisión

  
}

# Configuración de IAM para permitir invocaciones no autenticadas
resource "google_cloud_run_service_iam_member" "allow_unauthenticated" {
  location = google_cloud_run_service.optimia-wa.location  # Ubicación del servicio Cloud Run
  service  = google_cloud_run_service.optimia-wa.name      # Nombre del servicio Cloud Run al que aplica el IAM
  role     = "roles/run.invoker"                             # Rol que permite invocar el servicio
  member   = "allUsers"                                      # Permitir acceso no autenticado a todos los usuarios
}
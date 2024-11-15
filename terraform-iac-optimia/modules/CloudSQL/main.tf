# Crear una instancia de Cloud SQL (MySQL 8.0) con edición Enterprise
resource "google_sql_database_instance" "isbn_users_db" {
  name             = "isbn-users-db"              # Nombre de la instancia de base de datos, asignado desde la variable
  database_version = "MYSQL_8_0"                  # Versión de MySQL especificada: 8.0
  region           = var.region                   # Región donde se despliega la instancia, asignada desde la variable

  settings {
    tier = "db-custom-1-3840"                     # Configuración de Sandobox, puedes ajustar el tamaño si es necesario

    backup_configuration {
      enabled = true                              # Habilitar las copias de seguridad automáticas
    }

    ip_configuration {
      ipv4_enabled = true                         # Habilitar IP pública para la instancia
    }

    availability_type = "ZONAL"                # Configuración para disponibilidad en una sola zona    
  }
  deletion_protection = false
}

# Crear una base de datos en la instancia
resource "google_sql_database" "default" {
  name       = var.database_name                    # Nombre de la base de datos dentro de la instancia
  instance   = google_sql_database_instance.isbn_users_db.name  # Referencia a la instancia de Cloud SQL creada
  charset    = "utf8"                             # Conjunto de caracteres para la base de datos
  collation  = "utf8_general_ci"                  # Configuración de collation (predeterminada para UTF-8 en MySQL)
}

# Crear un usuario para la instancia con acceso desde cualquier host
resource "google_sql_user" "isbn_user" {
  name     = "isbn"                               # Nombre del usuario de la base de datos
  instance = google_sql_database_instance.isbn_users_db.name  # Referencia a la instancia de Cloud SQL creada
  password = "123"                                # Contraseña para el usuario (considera almacenarla de forma segura)
  host     = "%"                                  # Permitir acceso desde cualquier host
}
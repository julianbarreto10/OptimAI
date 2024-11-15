# Crear una base de datos Firestore en modo Native
resource "google_firestore_database" "database" {
  name          = "isbn-tasks-db"  # El nombre de la base de datos para Firestore siempre es "(default)"
  location_id   = var.region  # La ubicación de la base de datos en la región us-east4
  type          = "FIRESTORE_NATIVE"     # Configuración para que la base de datos opere en modo Native (orientado a documentos, sin restricciones de particiones)
}
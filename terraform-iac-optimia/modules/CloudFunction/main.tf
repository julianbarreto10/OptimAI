# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "source" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/tmp/function.zip"
}

# Add source code zip to the Cloud Function's bucket (Cloud_function_bucket) 
resource "google_storage_bucket_object" "zip" {
  source       = data.archive_file.source.output_path
  content_type = "application/zip"
  name         = "src-${data.archive_file.source.output_md5}.zip"
  bucket       = google_storage_bucket.Cloud_function_bucket.name
  depends_on = [
    google_storage_bucket.Cloud_function_bucket,
    data.archive_file.source
  ]
}

# Crear una Cloud Function de 2ª generación
resource "google_cloudfunctions2_function" "isbn_tasks_ms" {
  name        = "isbn-tasks-ms"
  location    = var.region

  service_config {
    min_instance_count = 1
    max_instance_count = 5
  }

  labels = {
    env = "development"
  }

  build_config {
    runtime     = "python312"
    entry_point = "tasks_api" # Set the entry point in the code  
    source {
      storage_source {
        bucket = google_storage_bucket.Cloud_function_bucket.name
        object = google_storage_bucket_object.zip.name
      }
    } 
  }
}

# Configuración de acceso para permitir invocaciones no autenticadas
resource "google_cloudfunctions2_function_iam_member" "allow_unauthenticated" {
  cloud_function = google_cloudfunctions2_function.isbn_tasks_ms.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers"  # Permite acceso no autenticado
}


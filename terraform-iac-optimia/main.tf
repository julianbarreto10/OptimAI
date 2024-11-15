provider "google" {
  project =  var.project_id
  region  = "us-east4"
}

module "APIs" {
  source     = "./modules/apis"
  project_id =  var.project_id
}

module "Database" {
    source = "./modules/CloudSQL"
    database_name = var.database_name  
    region = var.region
    depends_on    = [module.APIs]  # Asegura que el módulo de APIs se ejecute primero
}

module "Registry" {
    source = "./modules/Registry" 
    depends_on    = [module.APIs]  # Asegura que el módulo de APIs se ejecute primero 
}

module "docker_commands" {
    source = "./modules/DockerCommands"
    depends_on    = [module.Registry]
}

module "CloudRun" {
  source = "./modules/CloudRun"  
  region = var.region

  # Espera a que la imagen esté disponible antes de crear el servicio
  depends_on = [module.APIs, module.docker_commands]
}

module "Firestore" {
    source = "./modules/Firestore"  
    region = var.region
    depends_on    = [module.APIs]  # Asegura que el módulo de APIs se ejecute primero
}

module "CloudFunction" {
    source = "./modules/CloudFunction"  
    region = var.region
    project_id = var.project_id
    depends_on    = [module.APIs]  # Asegura que el módulo de APIs se ejecute primero
}
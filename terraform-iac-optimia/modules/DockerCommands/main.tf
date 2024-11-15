resource "null_resource" "docker_commands" {
  provisioner "local-exec" {
    command = "docker tag isbn-users-ms us-east4-docker.pkg.dev/isbn-2024ii/isbn-users-ms/isbn-users-ms"
  }

  provisioner "local-exec" {
    command = "docker push us-east4-docker.pkg.dev/isbn-2024ii/isbn-users-ms/isbn-users-ms"
  }
}
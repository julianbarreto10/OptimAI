resource "null_resource" "docker_commands" {
  provisioner "local-exec" {
    command = "docker tag info_drivers_ms us-east4-docker.pkg.dev/project-cbse-2024/optimia-drivers-ms/optimia-drivers-ms"
  }

  provisioner "local-exec" {
    command = "docker push us-east4-docker.pkg.dev/project-cbse-2024/optimia-drivers-ms/optimia-drivers-ms"
  }

  provisioner "local-exec" {
    command = "docker tag routing_ms us-east4-docker.pkg.dev/project-cbse-2024/optimia-routing-ms/optimia-routing-ms"
  }

  provisioner "local-exec" {
    command = "docker push us-east4-docker.pkg.dev/project-cbse-2024/optimia-routing-ms/optimia-routing-ms"
  }

  provisioner "local-exec" {
    command = "docker tag module_bi_ms us-east4-docker.pkg.dev/project-cbse-2024/optimia-bi-ms/optimia-bi-ms"
  }

  provisioner "local-exec" {
    command = "docker push us-east4-docker.pkg.dev/project-cbse-2024/optimia-bi-ms/optimia-bi-ms"
  }

  provisioner "local-exec" {
    command = "docker tag optimia_ag us-east4-docker.pkg.dev/project-cbse-2024/optimia-ag/optimia-ag"
  }

  provisioner "local-exec" {
    command = "docker push us-east4-docker.pkg.dev/project-cbse-2024/optimia-ag/optimia-ag"
  }

  provisioner "local-exec" {
    command = "docker tag optimia_wa us-east4-docker.pkg.dev/project-cbse-2024/optimia-wa/optimia-wa"
  }

  provisioner "local-exec" {
    command = "docker push us-east4-docker.pkg.dev/project-cbse-2024/optimia-wa/optimia-wa"
  }
}
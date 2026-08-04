output "public_ip" {
  value = module.orbit_vm.public_ip
}

output "ssh_connection_string" {
  value = module.orbit_vm.ssh_connection_string
}

output "resource_group_name" {
  value = module.orbit_vm.resource_group_name
}

output "public_ip" {
  description = "Public IP address of the VM."
  value       = azurerm_public_ip.this.ip_address
}

output "vm_name" {
  description = "Name of the virtual machine."
  value       = azurerm_linux_virtual_machine.this.name
}

output "resource_group_name" {
  description = "Name of the resource group holding every resource this module created."
  value       = azurerm_resource_group.this.name
}

output "ssh_connection_string" {
  description = "Ready-to-use SSH command."
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.this.ip_address}"
}

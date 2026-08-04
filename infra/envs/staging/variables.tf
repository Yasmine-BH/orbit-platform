variable "ssh_public_key_path" {
  description = "Path to your SSH public key, e.g. ~/.ssh/orbit_vm_key.pub"
  type        = string
  default     = "~/.ssh/orbit_vm_key.pub"
}

variable "ssh_allowed_cidrs" {
  description = "Your IP address in CIDR form, e.g. [\"203.0.113.45/32\"]. Never use 0.0.0.0/0."
  type        = list(string)
}

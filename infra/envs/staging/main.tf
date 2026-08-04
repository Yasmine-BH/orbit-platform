terraform {
  required_version = ">= 1.7"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }

  # Local state for now, on purpose — see README in this folder for why,
  # and for the remote backend this gets upgraded to later.
}

provider "azurerm" {
  features {}
}

module "orbit_vm" {
  source = "../../modules/vm-instance"

  name        = "orbit-staging"
  environment = "staging"
  location    = "francecentral"

  admin_username    = "azureuser"
  ssh_public_key    = file(var.ssh_public_key_path)
  ssh_allowed_cidrs = var.ssh_allowed_cidrs

  k3s_version = "v1.30.3+k3s1"

  tags = {
    Owner = "yasmine"
  }
}

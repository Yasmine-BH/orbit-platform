# staging environment

Instantiates the `vm-instance` module to create one Azure VM running k3s.

## First-time setup

```bash
cd infra/envs/staging
cp terraform.tfvars.example terraform.tfvars
# edit terraform.tfvars: set your own public IP (curl -s ifconfig.me) and ssh key path

terraform init
terraform fmt -check
terraform validate
terraform plan
terraform apply
```

## State

This starts with **local state** (a `terraform.tfstate` file in this folder, gitignored).
That's deliberate for now — see section 8.4 of the subject for why a remote backend
(Azure Blob Storage) becomes necessary once more than one person might run `apply`.
The backend gets added here once that need is felt, not before.

## Destroying

```bash
terraform destroy
```

Cost note: leaving the VM running costs roughly 45 EUR/month. Destroy it whenever you're
not actively using the cluster — that's the whole point of infrastructure as code.

## Debugging cloud-init

If the VM comes up but k3s isn't ready:

```bash
ssh -i ~/.ssh/orbit_vm_key azureuser@<public_ip>
cloud-init status --wait
cat /var/log/cloud-init-output.log
```

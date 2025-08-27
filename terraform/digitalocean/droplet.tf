resource "digitalocean_droplet" "web" {
  image    = var.droplet_image
  name     = "${var.project_name}-${var.environment}-web"
  region   = var.region
  size     = var.droplet_size
  ssh_keys = [digitalocean_ssh_key.main.fingerprint]
  
  user_data = file("${path.module}/user_data.sh")
  
  tags = [
    digitalocean_tag.environment.id,
    digitalocean_tag.project.id
  ]
}

resource "digitalocean_ssh_key" "main" {
  name       = "${var.project_name}-${var.environment}-key"
  public_key = file(var.ssh_public_key_path)
}

resource "digitalocean_tag" "environment" {
  name = var.environment
}

resource "digitalocean_tag" "project" {
  name = var.project_name
}

resource "digitalocean_firewall" "web" {
  name = "${var.project_name}-${var.environment}-fw"
  
  droplet_ids = [digitalocean_droplet.web.id]
  
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }
  
  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }
  
  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }
  
  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
  
  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

variable "droplet_image" {
  description = "Droplet image"
  type        = string
  default     = "ubuntu-22-04-x64"
}

variable "droplet_size" {
  description = "Droplet size"
  type        = string
  default     = "s-1vcpu-1gb"
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

output "droplet_ip" {
  description = "Public IP address of the droplet"
  value       = digitalocean_droplet.web.ipv4_address
}
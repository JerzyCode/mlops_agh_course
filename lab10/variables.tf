variable "github_token" {
  description = "GitHub Personal Access Token"
  type        = string
  sensitive   = true 
}

variable "repository_name" {
  description = "Name of the GitHub repository to create"
  type        = string
  default     = "terraform-managed-repo"
}

variable "repository_description" {
  description = "Description of the GitHub repository"
  type        = string
  default     = "Repository managed by Terraform"
}

variable "publicly_visible" {
  description = "Controls whether the repository is publicly visible or private"
  type        = bool
  default     = false
}
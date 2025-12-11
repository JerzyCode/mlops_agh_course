# variables.tf
variable "regions" {
  description = "List of AWS regions where S3 buckets will be created"
  type        = list(string)
  default     = ["us-east-1", "us-west-2"]  
}

variable "bucket_name_prefix" {
  description = "Prefix for all S3 bucket names in multiple regions"
  type        = string
  default     = "multi-region-bucket"      
}
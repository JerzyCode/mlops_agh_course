# modules/s3_bucket/variables.tf

variable "bucket_name_prefix" {
  description = "Prefix for the S3 bucket name"
  type        = string
}

variable "region" {
  description = "AWS region where the S3 bucket will be created"
  type        = string
}

variable "random_suffix" {
  description = "Random string to append to the bucket name to make it unique"
  type        = string
}

variable "lifecycle_days" {
  description = "Number of days after which objects in the bucket will transition to another storage class"
  type        = number
  default     = 5
}

variable "lifecycle_storage_class" {
  description = "AWS S3 storage class for lifecycle transition"
  type        = string
  default     = "GLACIER"
}

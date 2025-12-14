# AWS Configuration Variables
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "me-south-1" # Bahrain (closest to Egypt)
}

variable "aws_profile" {
  description = "AWS profile to use (optional)"
  type        = string
  default     = "default"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "world-population-etl"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# S3 Configuration
variable "s3_bucket_name" {
  description = "Name of the S3 bucket for data storage"
  type        = string
  default     = "world-population-etl-bucket"
}

variable "s3_storage_class" {
  description = "Storage class for S3 bucket"
  type        = string
  default     = "STANDARD"
}

# Glue Configuration
variable "glue_database_name" {
  description = "Name of the Glue database"
  type        = string
  default     = "world_population_db"
}

variable "glue_catalog_table_name" {
  description = "Name of the Glue catalog table"
  type        = string
  default     = "population_data"
}

# IAM Configuration
variable "create_iam_roles" {
  description = "Whether to create IAM roles for Glue and other services"
  type        = bool
  default     = true
}
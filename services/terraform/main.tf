# Local values for common configurations
locals {
  base_filename  = "world_population"
  current_date   = formatdate("YYYY-MM-DD", timestamp()) 
  full_filename  = "${local.base_filename}_${local.current_date}.csv"
  file_location  = "/terraform/data/${local.full_filename}"
  
  # Common tags applied to all resources
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Data source to get current AWS account ID
data "aws_caller_identity" "current" {}

# Data source to get current AWS region
data "aws_region" "current" {}

# S3 Bucket for data storage
resource "aws_s3_bucket" "data_bucket" {
  bucket = "${var.s3_bucket_name}-${random_id.bucket_suffix.hex}"
  
  tags = local.common_tags
}

# Random ID for bucket suffix to ensure uniqueness
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# S3 Bucket versioning
resource "aws_s3_bucket_versioning" "data_bucket_versioning" {
  bucket = aws_s3_bucket.data_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 Bucket lifecycle configuration
resource "aws_s3_bucket_lifecycle_configuration" "data_bucket_lifecycle" {
  bucket = aws_s3_bucket.data_bucket.id

  rule {
    id     = "delete_old_versions"
    status = "Enabled"

    expiration {
      days = 30
    }

    noncurrent_version_expiration {
      noncurrent_days = 7
    }
  }
}

# S3 Bucket public access block
resource "aws_s3_bucket_public_access_block" "data_bucket_pab" {
  bucket = aws_s3_bucket.data_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Upload a file to S3 (if file exists locally)
resource "aws_s3_object" "uploaded_file" {
  count = fileexists(local.file_location) ? 1 : 0
  
  bucket = aws_s3_bucket.data_bucket.id
  key    = "raw-data/${local.full_filename}"
  source = local.file_location
  
  tags = local.common_tags
}

# Glue Database
resource "aws_glue_catalog_database" "main_database" {
  name        = var.glue_database_name
  description = "Database for world population data"
  
  tags = local.common_tags
}

# Glue Catalog Table
resource "aws_glue_catalog_table" "population_table" {
  name          = var.glue_catalog_table_name
  database_name = aws_glue_catalog_database.main_database.name

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL                        = "TRUE"
    "parquet.compression"           = "SNAPPY"
    "projection.enabled"            = "true"
    "projection.date.type"          = "date"
    "projection.date.format"        = "yyyy-MM-dd"
    "projection.date.range"         = "2023-01-01,2025-12-31"
    "projection.date.interval"      = "1"
    "projection.date.interval.unit" = "DAYS"
    "storage.location.template"     = "s3://${aws_s3_bucket.data_bucket.bucket}/processed-data/$${date}/"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.data_bucket.bucket}/processed-data/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = "population-data-serde"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }

    columns {
      name = "country"
      type = "string"
    }

    columns {
      name = "population"
      type = "bigint"
    }

    columns {
      name = "year"
      type = "int"
    }

    columns {
      name = "continent"
      type = "string"
    }
  }

  tags = local.common_tags
}

# IAM Role for Glue (if enabled)
resource "aws_iam_role" "glue_role" {
  count = var.create_iam_roles ? 1 : 0
  
  name = "${var.project_name}-glue-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })

  tags = local.common_tags
}

# IAM Policy for Glue to access S3
resource "aws_iam_role_policy" "glue_s3_policy" {
  count = var.create_iam_roles ? 1 : 0
  
  name = "${var.project_name}-glue-s3-policy"
  role = aws_iam_role.glue_role[0].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.data_bucket.arn,
          "${aws_s3_bucket.data_bucket.arn}/*"
        ]
      }
    ]
  })
}

# Attach AWS managed policy for Glue
resource "aws_iam_role_policy_attachment" "glue_service_role" {
  count = var.create_iam_roles ? 1 : 0
  
  role       = aws_iam_role.glue_role[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}
# s3.tf

resource "random_id" "bucket_suffix" {
  count       = length(var.regions)
  byte_length = 4
}


# bucket 1 in us-east-1
resource "aws_s3_bucket" "s3_us_east_1" {
  bucket = "${var.bucket_name_prefix}-${var.regions[0]}-${random_id.bucket_suffix[0].hex}"
  provider = aws.us_east_1
}

resource "aws_s3_bucket_versioning" "s3_us_east_1" {
  bucket = aws_s3_bucket.s3_us_east_1.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "s3_us_east_1" {
  bucket = aws_s3_bucket.s3_us_east_1.id
  rule {
    id     = "transition-to-glacier"
    status = "Enabled"

    filter {}

    transition {
      days          = 2
      storage_class = "GLACIER"
    }
  }
}


# bucket 2 in us-west-2
resource "aws_s3_bucket" "s3_us_west_2" {
  bucket   = "${var.bucket_name_prefix}-${var.regions[1]}-${random_id.bucket_suffix[1].hex}"
  provider = aws.us_west_2
}

resource "aws_s3_bucket_versioning" "s3_us_west_2" {
  bucket = aws_s3_bucket.s3_us_west_2.id
  provider = aws.us_west_2
  
  versioning_configuration {
    status = "Enabled"
  }

  depends_on = [aws_s3_bucket.s3_us_west_2] 
}

resource "aws_s3_bucket_lifecycle_configuration" "s3_us_west_2" {
  bucket = aws_s3_bucket.s3_us_west_2.id
  provider = aws.us_west_2

  rule {  
    id     = "transition-to-glacier"
    status = "Enabled"

    filter {}

    transition {
      days          = 2
      storage_class = "GLACIER"
    }
  }

  depends_on = [aws_s3_bucket.s3_us_west_2]
}
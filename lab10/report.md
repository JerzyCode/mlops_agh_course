## 1. GitHub repository IaC setup


Created repository Command:

```
Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

github_repository.example: Creating...
github_repository.example: Creation complete after 5s [id=terraform-managed-repo]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:

repository_url = "https://github.com/JerzyCode/terraform-managed-repo"  
```

Screen:

![alt text](imgs/created_repo.png)

Cleaned:

```
Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

github_repository.example: Destroying... [id=terraform-managed-repo]
github_repository.example: Destruction complete after 1s

Destroy complete! Resources: 1 destroyed.
```

## Exercise 1

Files:
- outputs.tf
- repository.tf
- variables.tf


## 2. State management and remote backends

- added providers with s3 bucket
- created main.tf with ecr


Created .tfstate

```bash
jerzy-boksa@jerzyb-laptop:~$ aws s3 ls s3://jerzyb-s3-bucket-mlops-lab --recursive
2025-12-11 10:38:09       4022 mlops_app/terraform.tfstate

```

## Exercise 2

Creating buckets for different regions:


terraform plan out:
```
│ Error: creating S3 Bucket (mlops-lab-terraform-us-west-2-add258b0) Versioning: operation error S3: PutBucketVersioning, https response error StatusCode: 307, RequestID: JA2TYT65ACAQYFXE, HostID: EWUxtdYdZ3T4tppbOVK8Eoet7YHPGAQ4YJcCyCYKMkNAcZH2KcuiEOz+WK6VddJh1yeDUnveyMU=, api error TemporaryRedirect: Please re-send this request to the specified temporary endpoint. Continue to use the original request endpoint for future requests.
│ 
│   with aws_s3_bucket_versioning.s3_us_west_2,
│   on s3.tf line 45, in resource "aws_s3_bucket_versioning" "s3_us_west_2":
│   45: resource "aws_s3_bucket_versioning" "s3_us_west_2" {
```

Bucket state:

```bash
jerzy-boksa@jerzyb-laptop:~$ aws s3 ls
2025-12-03 08:56:45 jerzyb-s3-bucket-mlops-lab
2025-12-11 11:17:28 mlops-aliases-bucket-us-east-1
2025-12-11 11:17:28 mlops-aliases-bucket-us-west-2
2025-12-11 11:23:31 mlops-lab-terraform-us-east-1-8ace3ae5
2025-12-11 11:31:12 mlops-lab-terraform-us-west-2-add258b0
```


## Exercise 3

All in exercies3 - directory.

Result on terraform plan:

```bash
Apply complete! Resources: 8 added, 0 changed, 0 destroyed.

Outputs:

bucket_arns = {
  "us-east-1" = "arn:aws:s3:::multi-region-bucket-us-east-1-dfc8377043b5"
  "us-west-2" = "arn:aws:s3:::multi-region-bucket-us-west-2-30150a45a7f9"
}
bucket_regions = {
  "multi-region-bucket-us-east-1-dfc8377043b5" = "us-east-1"
  "multi-region-bucket-us-west-2-30150a45a7f9" = "us-west-2"
}
```


Result on aws s3 ls

```bash
jerzy-boksa@jerzyb-laptop:~$ aws s3 ls
2025-12-03 08:56:45 jerzyb-s3-bucket-mlops-lab
2025-12-11 11:17:28 mlops-aliases-bucket-us-east-1
2025-12-11 11:17:28 mlops-aliases-bucket-us-west-2
2025-12-11 11:23:31 mlops-lab-terraform-us-east-1-8ace3ae5
2025-12-11 11:31:12 mlops-lab-terraform-us-west-2-add258b0
2025-12-11 12:05:51 multi-region-bucket-us-east-1-dfc8377043b5
2025-12-11 12:05:51 multi-region-bucket-us-west-2-30150a45a7f9
```
## 1. Identity and Access Management (IAM)

Skipping because I use AWS Academy account.

### 1.1, 1.2 Skip because AWS Academy


### 1.3 Connect to AWS using the CLI


Running:

```bash
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Veryfi if installed.

```bash
jerzy-boksa@jerzyb-laptop:~/Apps/aws-cli$ aws --version
aws-cli/2.32.8 Python/3.13.9 Linux/6.14.0-36-generic exe/x86_64.ubuntu.24
```

Starting AWS Academy LAB.

Selecting "AWS Details" tab and copy from there aws_access_key etc. andp paste it to file ~/.aws/credentials

![alt text](aws_web_cli.png)


### 1.4 Skip because AWS Academy


## 2. Amazon S3 setup and file management


### 2.1 Create an S3 bucket

![alt text](create_bucket.png)

Bucket created:

![alt text](created_bucket.png)


### 2.2 Uploading file

```bash
jerzy-boksa@jerzyb-laptop:~/Programming/Projects/university/term_3/mlops_agh_course/lab9$ aws s3 cp models/mlops_model/ s3://jerzyb-s3-bucket-mlops-lab/mlops_model/ --recursive
```

Checking if uploaded

```bash
jerzy-boksa@jerzyb-laptop:~/Programming/Projects/university/term_3/mlops_agh_course/lab9$ aws s3 ls s3://jerzyb-s3-bucket-mlops-lab --recursive
2025-12-03 09:05:32     474781 mlops_model/classifier.joblib
2025-12-03 09:05:33        312 mlops_model/sentence_transformer.model/1_Pooling/config.json
2025-12-03 09:05:32      10454 mlops_model/sentence_transformer.model/README.md
2025-12-03 09:05:32        611 mlops_model/sentence_transformer.model/config.json
2025-12-03 09:05:32        283 mlops_model/sentence_transformer.model/config_sentence_transformers.json
2025-12-03 09:05:32   90864192 mlops_model/sentence_transformer.model/model.safetensors
2025-12-03 09:05:32        349 mlops_model/sentence_transformer.model/modules.json
2025-12-03 09:05:33         57 mlops_model/sentence_transformer.model/sentence_bert_config.json
2025-12-03 09:05:33        695 mlops_model/sentence_transformer.model/special_tokens_map.json
2025-12-03 09:05:32     711661 mlops_model/sentence_transformer.model/tokenizer.json
2025-12-03 09:05:32       1464 mlops_model/sentence_transformer.model/tokenizer_config.json
```
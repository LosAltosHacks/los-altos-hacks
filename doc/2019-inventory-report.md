# Services accessed in 2019 development period according to IAM

## Amazon S3

Contains bucket for each website and staging

* main site
* main site staging
* admin
* admin staging
And a bucket for two codepipelines
* arn:aws:s3:::codepipeline-us-east-2-727215867060
* arn:aws:s3:::codepipeline-us-east-2-606377281685

## AWS Health APIs and Notifications

Not related to any specific billable / cfged infra

## AWS Identity and Access Management

Known

## Amazon EC2

One T2.micro instance i-0add44955306c0ca9
functionality includes admin backend hosting
does it run the CI??

## AWS Database Migration Service

Contains a VPC subnet group, two endpoints (1 aurora mysql and one ec2 mysql), and one replication instance
TODO investigate

## Elastic Load Balancing

none

## Amazon CloudWatch

none

## AWS Key Management Service

3 keys - aws/rds, aws/dms, aws/s3 (all of these are default keys)

## AWS Config

none

## Amazon CloudFront

4 distros

* api (http only)
* admin (s3)
* main site, losaltoshacks.com (s3)
* ctf (tempo)

## AWS WAF

none
TODO looks into

## AWS Certificate Manager

none

## AWS Elemental MediaStore

none

## AWS Elemental MediaPackage

none

## AWS Directory Service

none

## Amazon Route 53

records associated w/ cloudfront, gsuite etc
seems to manage losaltoshacks.com
guessing losaltoshacks.com ns is pointed to route53

## Manage - Amazon API Gateway

none

## AWS Certificate Manager Private Certificate Authority

two certs, one ctf, one rest
guessing automatically done by cloudfront

## Amazon SES

contains verified identities and email address, info@losaltoshacks.com

## AWS Application Discovery Service

none

## AWS Billing

none

## AWS CodeBuild

4 pipelines
each perm of {prod, stage},{admin-db, main site}
note no CD of backend
each sources from codepipeline
TODO figure out why not use github source directly
environment is AWS nodejs env, injects S3 bucket and cloudfront distribution
buildspec is in github source

## Amazon Elastic Container Registry

none

## AWS CodeCommit

none

## Amazon CloudWatch Logs

none

## AWS CodePipeline

4 pipelines, as in codebuild, each of which grabs from github and sends to codebuild

## AWS Trusted Advisor

big TODO

## AWS CloudTrail

none

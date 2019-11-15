# Cloudfront Redirects

To ensure resource integrity and privacy on our infra, we don't open production S3 buckets and instead use the Cloudfront REST feature to access them.
This means we don't get AWS S3 URL rewriting, e.g. `/2016/` or `/2016` resolves to `/2016/index.html`.
Instead, we can use [this Lambda function, deployed @Edge](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:621073008195:applications~standard-redirects-for-cloudfront) to do this for us in CF.

It might seem like node.js is a poor choice, but it is the [fastest Lambda runtime](https://medium.com/the-theam-journey/benchmarking-aws-lambda-runtimes-in-2019-part-i-b1ee459a293d).

Also: Lambda@Edge can only trigger functions in us-east-1, so the function is deployed there. It can be attached to new CF behaviors as well.

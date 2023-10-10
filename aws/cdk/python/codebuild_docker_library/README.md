# Using CDK to build CodeBuild and ECR for building docker-library images

This CDK creates an iam role for the codebuild to access ECR.
The following is an example of policy's permissions:

```json
{
    "Effect": "Allow",
    "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:GetRepositoryPolicy",
        "ecr:DescribeRepositories",
        "ecr:ListImages",
        "ecr:DescribeImages",
        "ecr:BatchGetImage",
        "ecr:GetLifecyclePolicy",
        "ecr:GetLifecyclePolicyPreview",
        "ecr:ListTagsForResource",
        "ecr:DescribeImageScanFindings",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecr:PutImage"
    ],
    "Resource": "*"
}
```

The cdk creates a codebuild project with the Buildspec similar to the following:
```yaml
version: 0.2

phases:
  pre_build:
    commands:
       - echo Logging in to Amazon ECR...
       - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
       - git clone $DOCKER_LIBRARY docker-library
       - cd docker-library
  build:
    commands:
      - echo Build started on `date`
      - echo Building the ubuntu base image...
      - docker build dev/ubuntu/ -t pv/ubuntu:latest
      - echo Building the hugo image...
      - ./build.sh -d debian -b pv/ubuntu:latest -i awscli,hugo -t $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/hugo:latest
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the docker images...
      - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/hugo:latest
```

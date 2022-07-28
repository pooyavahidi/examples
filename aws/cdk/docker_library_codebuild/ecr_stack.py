from aws_cdk import core as cdk, aws_ecr


class EcrStack(cdk.Stack):
    def __init__(self, scope, construct_id, props, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.ecr_repos = []

        for repo in props["repositories"]:
            ecr = aws_ecr.Repository(
                scope=self,
                id=repo,
                repository_name=repo,
                removal_policy=cdk.RemovalPolicy.DESTROY,
                image_scan_on_push=True,
            )
            # To only keep the last two images
            ecr.add_lifecycle_rule(max_image_count=2)
            # Add the repos to the list
            self.ecr_repos.append(ecr)

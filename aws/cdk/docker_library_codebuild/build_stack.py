from aws_cdk import (
    core as cdk,
    aws_codebuild,
)


class BuildStack(cdk.Stack):
    def __init__(
        self, scope: cdk.Construct, construct_id: str, props, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        project_name = f"{props['namespace']}-build-project"

        cb_docker_build = aws_codebuild.Project(
            self,
            project_name,
            project_name=project_name,
            build_spec=aws_codebuild.BuildSpec.from_object_to_yaml(
                self.__get_buildspec()
            ),
            environment=aws_codebuild.BuildEnvironment(
                privileged=True,
                build_image=aws_codebuild.LinuxBuildImage.STANDARD_5_0,
                environment_variables={
                    "AWS_ACCOUNT_ID": aws_codebuild.BuildEnvironmentVariable(
                        value=self.account
                    ),
                    "DOCKER_LIBRARY": aws_codebuild.BuildEnvironmentVariable(
                        value=props["docker_library"]
                    ),
                },
            ),
        )

        for ecr_repo in props["ecr_repos"]:
            ecr_repo.grant_pull_push(cb_docker_build)

    def __get_buildspec(self):
        spec = {
            "version": "0.2",
            "phases": {
                "pre_build": {
                    "commands": [
                        "echo Logging in to Amazon ECR...",
                        (
                            "aws ecr get-login-password "
                            "--region $AWS_DEFAULT_REGION | "
                            "docker login --username AWS "
                            "--password-stdin "
                            "$AWS_ACCOUNT_ID.dkr.ecr."
                            "$AWS_DEFAULT_REGION.amazonaws.com"
                        ),
                        "git clone $DOCKER_LIBRARY docker-library",
                        "cd docker-library",
                    ]
                },
                "build": {
                    "commands": [
                        "echo Build started on `date`",
                        "echo Building the ubuntu base image...",
                        "docker build dev/ubuntu/ -t pv/ubuntu:latest",
                        "echo Building the hugo image...",
                        (
                            "./build.sh -d debian -b pv/ubuntu:latest "
                            "-i awscli,hugo "
                            "-t $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION."
                            "amazonaws.com/hugo:latest"
                        ),
                    ]
                },
                "post_build": {
                    "commands": [
                        "echo Build completed on `date`",
                        "echo Pushing the docker images...",
                        (
                            "docker push $AWS_ACCOUNT_ID.dkr.ecr."
                            "$AWS_DEFAULT_REGION.amazonaws.com/hugo:latest"
                        ),
                    ]
                },
            },
        }
        return spec

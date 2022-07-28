#!/usr/bin/env python3

import os
from aws_cdk import core as cdk
from ecr_stack import EcrStack
from build_stack import BuildStack


app = cdk.App()
props = {
    "namespace": app.node.try_get_context("namespace"),
    "repositories": app.node.try_get_context("repositories"),
    "ecr_repos": [],
    "docker_library": app.node.try_get_context("docker_library"),
}
env = cdk.Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION"),
)
ecr = EcrStack(
    scope=app,
    construct_id=f"{props['namespace']}-ecr",
    props=props,
    env=env,
    description="ECR Repositories for docker images",
)

# Read the output of the ecr stack and set it to the props
props["ecr_repos"] = ecr.ecr_repos

build = BuildStack(
    scope=app,
    construct_id=f"{props['namespace']}-build",
    props=props,
    env=env,
    description=(
        "Resources to build Dockerfiles in docker-library and "
        "push them to ECR"
    ),
)

build.add_dependency(ecr)

app.synth()

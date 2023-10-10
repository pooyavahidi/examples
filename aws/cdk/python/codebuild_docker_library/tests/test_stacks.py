import pytest
from aws_cdk import core as cdk
from build_stack import BuildStack
from ecr_stack import EcrStack


@pytest.fixture(scope="session")
def synth():
    app = cdk.App()
    props = {
        "namespace": "docker-library",
        "repositories": ["hugo", "ubuntu"],
        "ecr_repos": [],
        "docker_library": "https://github.com/myuser/myrepo",
    }
    ecr = EcrStack(
        scope=app,
        construct_id=f"{props['namespace']}-ecr",
        props=props,
    )

    props["ecr_repos"] = ecr.ecr_repos

    build = BuildStack(
        scope=app,
        construct_id=f"{props['namespace']}-build",
        props=props,
    )

    build.add_dependency(ecr)

    return app.synth()


def test_stacks_created(synth):
    assert {"docker-library-ecr", "docker-library-build"} == {
        x.display_name for x in synth.stacks
    }

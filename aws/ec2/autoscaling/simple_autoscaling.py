import boto3

asg = boto3.client("autoscaling")


def get_asg(name):
    groups = asg.describe_auto_scaling_groups(
        AutoScalingGroupNames=[
            name,
        ],
    )
    groups = groups["AutoScalingGroups"]
    if not groups:
        raise Exception("asg not found")

    return groups[0]


def set_asg_desired(name, desired):
    response = asg.set_desired_capacity(
        AutoScalingGroupName=name,
        DesiredCapacity=desired,
        HonorCooldown=True,
    )
    return response


if __name__ == "__main__":
    res = get_asg("asg_test")
    print(res)

    # res = set_asg_desired("asg_test", 2)
    # print(res)

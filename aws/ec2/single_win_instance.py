import sys
import argparse
import boto3

AUTO_TERMINATE_IN_MIN = "60"


def get_latest_image_id(ec2, name_prefix):
    images = ec2.describe_images(
        Owners=["amazon"],
        Filters=[{"Name": "name", "Values": [f"{name_prefix}*"]}],
    )

    # Filter images based on creation date and sort them
    images["Images"] = sorted(
        images["Images"], key=lambda x: x["CreationDate"], reverse=True
    )

    # Raise error if images list is empty
    if not images["Images"]:
        raise ValueError(f"No images found with name prefix {name_prefix}")

    image = images["Images"][0]

    print(f"Using AMI: {image['ImageId']}, {image['Name']}")

    return image["ImageId"]


def create_instance(
    ec2, subnet_id, security_group_id, key_pair_name, ami_id, instance_type
):
    if not (
        subnet_id
        and security_group_id
        and key_pair_name
        and ami_id
        and instance_type
    ):
        print(
            "subnet-id, security-group-id, key-pair-name, ami-id, \
and instance-type must be provided."
        )
        sys.exit(1)

    print(f"Creating '{instance_type}' instance...")
    try:
        response = ec2.run_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_type,
            KeyName=key_pair_name,
            SubnetId=subnet_id,
            SecurityGroupIds=[
                security_group_id,
            ],
        )

        instance_id = response["Instances"][0]["InstanceId"]
        print(f"Instance_id: {instance_id} is initializing...")
        waiter = ec2.get_waiter("instance_running")
        waiter.wait(InstanceIds=[instance_id])
        print("Instance is now running...")

        # Create tag
        print(f"Adding 'auto_terminate={AUTO_TERMINATE_IN_MIN}' tag...")
        ec2.create_tags(
            Resources=[instance_id],
            Tags=[
                {"Key": "auto_terminate", "Value": AUTO_TERMINATE_IN_MIN},
            ],
        )

        # Getting the public IP address
        instance_description = ec2.describe_instances(
            InstanceIds=[instance_id]
        )
        public_ip = instance_description["Reservations"][0]["Instances"][0][
            "PublicIpAddress"
        ]
        print(f"Public IP: {public_ip}")

    except Exception as e:
        print(f"Error: Unable to run instance. {str(e)}")
        sys.exit(1)


def check_existing_instances(ec2, subnet_id):
    print("Checking if there are any instances in the subnet...")
    try:
        instances = ec2.describe_instances(
            Filters=[
                {"Name": "subnet-id", "Values": [subnet_id]},
            ],
        )

        return instances["Reservations"]
    except Exception as e:
        print(f"Error: Unable to check existing instances. {str(e)}")
        sys.exit(1)


def cleanup_instances(ec2, subnet_id):
    try:
        instances = check_existing_instances(ec2, subnet_id)
        if len(instances) == 0:
            print("No instances found")
            return

        print("Terminating all instances in subnet...")
        for reservation in instances:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]
                ec2.terminate_instances(InstanceIds=[instance_id])
                print(f"Termination request sent for instance: {instance_id}")
    except Exception as e:
        print(f"Error: Unable to terminate instance. {str(e)}")
        sys.exit(1)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region", required=True, help="AWS Region")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup flag")
    parser.add_argument("--subnet-id", required=True, help="Subnet ID")
    parser.add_argument(
        "--security-group-id",
        required=False,
        help="Security Group ID",
    )
    parser.add_argument(
        "--key-pair-name",
        help="EC2 Key Pair Name",
    )
    parser.add_argument(
        "--ami-name-prefix",
        default="Windows_Server-2022-English-Full-Base",
        help="AMI name prefix, default is 'Windows_Server-2022-English-Full-Base'",
    )

    parser.add_argument(
        "--instance-type",
        default="t2.micro",
        help="Instance type, default is 't2.micro'",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    ec2 = boto3.client("ec2", region_name=args.region)

    if args.cleanup:
        cleanup_instances(ec2, args.subnet_id)
    else:
        instances = check_existing_instances(ec2, args.subnet_id)
        if instances:
            print("Existing instances in subnet:")
            for reservation in instances:
                for instance in reservation["Instances"]:
                    print(instance["InstanceId"])
            print("use --cleanup option to terminate instances first")
        else:
            ami_id = get_latest_image_id(ec2, args.ami_name_prefix)
            create_instance(
                ec2,
                args.subnet_id,
                args.security_group_id,
                args.key_pair_name,
                ami_id,
                args.instance_type,
            )


if __name__ == "__main__":
    main()

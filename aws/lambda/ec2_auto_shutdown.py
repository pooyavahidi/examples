import logging
from datetime import datetime, timedelta
import boto3

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Set the default stop time for instances (in hours)
DEFAULT_STOP_TIME = 12


def lambda_handler(event, context):
    ec2 = boto3.client("ec2")

    # Get list of all regions
    regions = ec2.describe_regions().get("Regions", [])

    # Iterate over each region
    for region in regions:
        region_name = region["RegionName"]
        ec2_region = boto3.client("ec2", region_name=region_name)

        log.info(f"Checking for instances in region {region_name}")

        instances_to_terminate = set(list_instances_to_terminate(ec2_region))
        instances_to_stop = set(list_instances_to_stop(ec2_region))
        instances_to_stop -= instances_to_terminate

        if instances_to_terminate:
            try:
                terminate_instances(ec2_region, list(instances_to_terminate))
            except Exception as e:
                log.error(
                    f"Error terminating instances {instances_to_terminate} in region {region_name}. Error: {str(e)}"
                )

        if instances_to_stop:
            try:
                stop_instances(ec2_region, list(instances_to_stop))
            except Exception as e:
                log.error(
                    f"Error stopping instances {instances_to_stop} in region {region_name}. Error: {str(e)}"
                )

        if not instances_to_terminate and not instances_to_stop:
            log.info("No instances to terminate or stop")


def list_instances_to_terminate(ec2):
    instances = ec2.describe_instances()
    instances_to_terminate = []
    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            # Calculate the difference between current time
            # and instance launch time.
            launch_time = instance["LaunchTime"]
            current_time = datetime.now(launch_time.tzinfo)
            running_time = current_time - launch_time

            termination_time = None

            # Check for auto_terminate tag and if present,
            # use it to determine the termination time.
            for tag in instance.get("Tags", []):
                if tag["Key"] == "auto_terminate":
                    try:
                        termination_time = timedelta(minutes=int(tag["Value"]))
                        break
                    except ValueError:
                        log.error(
                            f"Invalid value for auto_terminate tag in instance {instance['InstanceId']}. Skipping termination."
                        )
                        termination_time = None
                        break

            # Check if the instance has been running for more than
            # the termination time.
            if termination_time and running_time > termination_time:
                instances_to_terminate.append(instance["InstanceId"])

    return instances_to_terminate


def list_instances_to_stop(ec2):
    instances = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )
    instances_to_stop = []
    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            # Calculate the difference between current time and
            # instance launch time.
            launch_time = instance["LaunchTime"]
            current_time = datetime.now(launch_time.tzinfo)
            running_time = current_time - launch_time

            # Check if the instance has been running for more than
            # the default stop time.
            if running_time > timedelta(hours=DEFAULT_STOP_TIME):
                instances_to_stop.append(instance["InstanceId"])

    return instances_to_stop


def terminate_instances(ec2, ids):
    log.info(f"Terminating instances {ids}")
    ec2.terminate_instances(InstanceIds=ids)


def stop_instances(ec2, ids):
    log.info(f"Stopping instances {ids}")
    ec2.stop_instances(InstanceIds=ids)

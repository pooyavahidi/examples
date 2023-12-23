import sys
import math
import logging
import argparse
import inspect
import boto3

# set level to error for sagemaker
logging.getLogger("sagemaker.config").setLevel(logging.ERROR)
import sagemaker

sagemaker_client = boto3.client("sagemaker")
iam = boto3.client("iam")

command_outputs = []


def format_size(size):
    """Convert size from bytes to a human-readable format."""
    if not size:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    power = math.pow(1024, i)
    size = round(size / power, 2)
    return f"{size}{size_name[i]}"


def format_datetime(datetime_str):
    return datetime_str.strftime("%Y-%m-%d %H:%M:%S")


def print_list(rows):
    """
    # Example usage
    rows = ["a", "b", "c"]
    """
    if not rows:
        return

    for row in rows:
        # print index for each row
        print(rows.index(row), end="\t")
        print(row)


def print_table(rows):
    """
    # Example usage
    rows = [
        {"Name": "Alice", "Age": 30, "City": "New York"},
        {"Name": "Bob", "Age": 25, "City": "Los Angeles"},
        {"Name": "Charlie", "Age": 35, "City": "Chicago"}
    ]
    """
    if not rows:
        return

    headers = rows[0].keys()
    col_widths = {header: len(header) for header in headers}

    # Find the maximum width for each column
    for row in rows:
        for header in headers:
            col_widths[header] = max(
                col_widths[header], len(str(row.get(header, "")))
            )

    # Create a format string for each row
    row_format = "\t".join(
        ["{:<" + str(col_widths[header]) + "}" for header in headers]
    )

    # Print headers
    print(row_format.format(*headers))

    # Print rows
    for row in rows:
        print(
            row_format.format(
                *(str(row.get(header, "")) for header in headers)
            )
        )


class SageMaker:
    """SageMaker service class."""

    def cmd_output(self):
        return command_outputs

    def test2(self):
        return "This is test2, an instance method."

    @staticmethod
    def test():
        rows = [
            {
                "Name": "Alice",
                "Age": 30,
                "City": "New York",
                "Extra": {"a": 1},
            },
            {
                "Name": "Bob - or a very longer than expected name",
                "Age": 25,
                "City": "Los Angeles",
            },
            {
                "Name": "Charlie",
                "Age": 35,
                "City": "Chicago",
            },
        ]
        return rows

    @staticmethod
    def role_arn():
        return iam.get_role(RoleName="SageMakerExecutionRole")["Role"]["Arn"]

    @staticmethod
    def bucket():
        return sagemaker.Session().default_bucket()

    @staticmethod
    def bucket_ls(prefix=None):
        bucket = SageMaker.bucket()
        s3_client = boto3.client("s3")
        if prefix:
            objects = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        else:
            objects = s3_client.list_objects_v2(Bucket=bucket)

        if "Contents" not in objects:
            return "No objects found."

        rows = []
        for obj in objects["Contents"]:
            rows.append(
                {
                    "Key": obj["Key"],
                    "LastModified": format_datetime(obj["LastModified"]),
                    "Size": format_size(obj["Size"]),
                }
            )

        return rows

    @staticmethod
    def ep_desc(name):
        desc = sagemaker_client.describe_endpoint(EndpointName=name)
        return [
            {
                "Name": desc["EndpointName"],
                "ConfigName": desc["EndpointConfigName"],
                "Status": desc["EndpointStatus"],
                "CreationTime": format_datetime(desc["CreationTime"]),
                "LastModifiedTime": format_datetime(desc["LastModifiedTime"]),
            }
        ]

    @staticmethod
    def ep_ls():
        endpoints = sagemaker_client.list_endpoints()
        return [
            endpoint["EndpointName"] for endpoint in endpoints["Endpoints"]
        ]

    @staticmethod
    def ep_deploy_from_config(config_name, ep_name):
        if not ep_name:
            ep_name = config_name

        return sagemaker_client.create_endpoint(
            EndpointName=ep_name,
            EndpointConfigName=config_name,
        )

    @staticmethod
    def ep_rm(name):
        return sagemaker_client.delete_endpoint(EndpointName=name)

    @staticmethod
    def ep_config_ls():
        endpoint_configs = sagemaker_client.list_endpoint_configs()
        return [
            endpoint_config["EndpointConfigName"]
            for endpoint_config in endpoint_configs["EndpointConfigs"]
        ]


def handle_action(services, service_alias, action, args):
    # Check if the service is supported
    if service_alias not in services:
        print(f"Service '{service_alias}' is not supported.")
        return

    # Get the service
    service = services[service_alias]["service"]

    # Format action to match the method name in the class
    method_name = action.replace("-", "_")

    # Check if the action is callable and supported
    if not hasattr(service, method_name) or not inspect.isroutine(
        getattr(service, method_name)
    ):
        print(f"Action '{action}' for '{service_alias}' is not supported.")
        return

    # Remove unnecessary arguments before calling the method
    args.pop("service", None)
    args.pop("action", None)

    # Call the method and handle the result
    method = getattr(service, method_name)
    try:
        result = method(**args)
        return handle_result(result)
    except TypeError as ex:
        print(f"Error calling action '{action}': {ex}")


def handle_result(result):
    if result is False:
        sys.exit(1)
    elif result in [0, 1]:
        return result
    elif not result:
        # Handle the case where result is None, [], or {}, "", etc
        return

    command_outputs.clear()
    if isinstance(result, list):
        command_outputs.extend(result)
        if isinstance(result[0], dict):
            print_table(result)
        else:
            print_list(result)
    else:
        command_outputs.append(result)
        print_list([result])


def create_parsers(
    services,
    description,
):
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(dest="service", help="services")

    for service_name, service_info in services.items():
        service = service_info["service"]
        service_description = service_info["description"]

        # Create a subparser for each service
        service_parser = subparsers.add_parser(
            service_name, help=f"{service_description}"
        )
        service_subparsers = service_parser.add_subparsers(
            dest="action", help=f"{service_name} actions"
        )

        # Get all public methods of the service, both static and instance.
        methods = [
            name
            for name, func in inspect.getmembers(
                service, predicate=inspect.isroutine
            )
            if not name.startswith("_")
        ]

        for method in methods:
            method_func = getattr(service, method)
            sig = inspect.signature(method_func)

            # Create a subparser for each method
            formatted_method = method.replace("_", "-")
            method_parser = service_subparsers.add_parser(
                formatted_method, help=f"{method} action"
            )

            # Add arguments for each method
            for param_name, param in sig.parameters.items():
                if param_name == "kwargs":
                    continue

                formatted_param_name = param_name.replace("_", "-")
                is_required = param.default is inspect.Parameter.empty

                method_parser.add_argument(
                    f"--{formatted_param_name}",
                    required=is_required,
                    default=None if is_required else param.default,
                    help=f"Optional (default: {param.default})"
                    if not is_required
                    else "Required",
                )

    return parser


def main():
    services = {
        "sm": {"service": SageMaker(), "description": "SageMaker service"},
    }

    parser = create_parsers(services, description="AWS AI/ML Services CLI")
    args = parser.parse_args()

    # Convert args to dictionary and filter out None values
    args_dict = {k: v for k, v in vars(args).items() if v is not None}

    if args.service and args.action:
        # Pass the dictionary of arguments to handle_action
        handle_action(
            services, args.service, args.action.replace("-", "_"), args_dict
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

import time
import boto3


rds = boto3.client("rds")


def get_rds_instance(db_id):
    try:
        instances = rds.describe_db_instances(
            DBInstanceIdentifier=db_id,
        )
        instance = instances["DBInstances"][0]
    except rds.exceptions.DBInstanceNotFoundFault:
        instance = None

    return instance


def create_read_replica(db_id, source_db_id):
    response = rds.create_db_instance_read_replica(
        DBInstanceIdentifier=db_id,
        SourceDBInstanceIdentifier=source_db_id,
        DBInstanceClass="db.m5.xlarge",
        MultiAZ=False,
        PubliclyAccessible=False,
    )
    return response


def wait_until_instance_is_available(db_id):
    while True:
        db = get_rds_instance(db_id)
        db_status = db["DBInstanceStatus"]
        print(f"{db_id} is {db_status}")

        if db_status == "available":
            break

        time.sleep(5)


def delete_db_instance(db_id):
    response = rds.delete_db_instance(
        DBInstanceIdentifier=db_id,
        SkipFinalSnapshot=True,
        DeleteAutomatedBackups=True,
    )
    return response


if __name__ == "__main__":
    res = get_rds_instance(db_id="mydb")
    print(res)

    # res = create_read_replica(db_id="read-replica", source_db_id="mydb")
    # print(res)

    # wait_until_instance_is_available("read-replica")

    # res = delete_db_instance("read-replica")
    # print(res)

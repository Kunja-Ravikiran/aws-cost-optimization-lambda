import boto3
from datetime import datetime, timezone

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    print("Starting snapshot cleanup process...")

    # Get all snapshots
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

    # Get all volumes
    volumes = ec2.describe_volumes()['Volumes']
    volume_ids = {vol['VolumeId'] for vol in volumes}

    # Get running instances
    instances = ec2.describe_instances()
    active_instance_ids = set()

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])

    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        try:
            # Optional: retention policy (30 days)
            age_days = (datetime.now(timezone.utc) - snapshot['StartTime']).days

            if age_days < 30:
                continue

            # If volume doesn't exist
            if volume_id not in volume_ids:
                print(f"Deleting snapshot {snapshot_id} (volume not found)")
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                continue

            # Check if volume attached to any instance
            volume = next((v for v in volumes if v['VolumeId'] == volume_id), None)

            if volume and not volume['Attachments']:
                print(f"Deleting snapshot {snapshot_id} (volume not attached)")
                ec2.delete_snapshot(SnapshotId=snapshot_id)

        except Exception as e:
            print(f"Error processing snapshot {snapshot_id}: {str(e)}")

    print("Cleanup completed.")

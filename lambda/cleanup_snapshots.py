import boto3
from datetime import datetime, timezone

# 🔧 Configurable retention period
RETENTION_DAYS = 0  # Set to 30 for production

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    print("🚀 Starting EBS Snapshot Cleanup Process...")

    # Get all snapshots
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    print(f"📸 Total snapshots found: {len(snapshots)}")

    # Get all volumes
    volumes = ec2.describe_volumes()['Volumes']
    volume_ids = {vol['VolumeId'] for vol in volumes}

    print(f"💾 Total volumes found: {len(volume_ids)}")

    # Process each snapshot
    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        print(f"🔍 Checking snapshot: {snapshot_id}")

        try:
            # 🧠 Retention Logic
            age_days = (datetime.now(timezone.utc) - snapshot['StartTime']).days

            if age_days < RETENTION_DAYS:
                print(f"⏩ Skipping {snapshot_id} (age {age_days} days < {RETENTION_DAYS})")
                continue

            # ❌ Case 1: No volume attached
            if not volume_id:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"🗑️ Deleted {snapshot_id} (no volume attached)")
                continue

            # ❌ Case 2: Volume does not exist
            if volume_id not in volume_ids:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"🗑️ Deleted {snapshot_id} (volume not found)")
                continue

            # ❌ Case 3: Volume exists but not attached
            volume = next((v for v in volumes if v['VolumeId'] == volume_id), None)

            if volume and not volume['Attachments']:
                ec2.delete_snapshot(SnapshotId=snapshot_id)
                print(f"🗑️ Deleted {snapshot_id} (volume not attached)")

        except Exception as e:
            print(f"❌ Error processing {snapshot_id}: {str(e)}")

    print("✅ Snapshot cleanup completed.")

    return {
        "statusCode": 200,
        "body": "Snapshot cleanup completed successfully"
    }

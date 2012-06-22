#!/bin/bash

## This script is an attempt to automate http://blog.ibd.com/scalable-deployment/copy-an-ebs-ami-image-to-another-amazon-ec2-region/
## (there is another blog as well about it http://alestic.com/2010/10/ec2-ami-copy)

## It is not complete since i got stuck while finding the right kernel id to associate with the AMI in the target region
## so i endup just recreating the image from scratch!

src_keypair=tiziano
src_fullpath_keypair=/home/acca/.ssh/tiziano-aws-us-east-1.pem
src_availability_zone=us-east-1a
src_instance_type=m1.medium
src_region=us-east-1
src_origin_ami=ami-9ad979f3
src_device=/dev/sdh
src_dir=/src
src_user=tiziano

# src_instance_id=i-2c800255

read -p "Do you have already a source instance? [leave it blank or give us the id] "
src_instance_id=$REPLY
if [ ! -z $src_instance_id ]; then
	echo "Source instance id to use: $src_instance_id"
else
	echo "Starting up a source instance and capture his instance id ..."

	# Start up the source instance and capture the instanceid
	src_instance_id=$(ec2-run-instances \
	  --key $src_keypair \
	  --availability-zone $src_availability_zone \
	  --instance-type $src_instance_type \
	  $src_origin_ami \
	  --region $src_region  | \
	  egrep ^INSTANCE | cut -f2)

	echo "Source instance id: $src_instance_id"

	# Wait for the instance to move to the “running” state
	while src_public_fqdn=$(ec2-describe-instances --region $src_region "$src_instance_id" | \
	  egrep ^INSTANCE | cut -f4) && test -z $src_public_fqdn; do echo -n .; sleep 1; done

	echo ""
	echo "Source instance is running with fqdn: $src_public_fqdn"
fi

# new_volume_id=vol-2933ab47

read -p "Does the instance have already the source volume attached? [leave it blank or give us the id] "
new_volume_id=$REPLY
if [ ! -z $new_volume_id ]; then
	echo "New source volume id to use: $new_volume_id"
else
	## Create a new volume from the EBS AMI snapshot

	# Get the volume id
	ec2-describe-instances --region $src_region $src_instance_id > /tmp/src_instance_info
	src_volume_id=$(egrep ^BLOCKDEVICE /tmp/src_instance_info | cut -f3); 
	echo "The current volume id associated with the instance: $src_volume_id"

	# Now get the snapshot id from the volume id
	ec2-describe-volumes --region $src_region $src_volume_id | egrep ^VOLUME > /tmp/volume_info
	src_snapshot_id=$(cat /tmp/volume_info | cut -f4)
	echo "The original snapshot id associated with the current volume: $src_snapshot_id"

	src_size=$(cat /tmp/volume_info | cut -f3)
	echo "Size of the current volume: $src_size Gb"

	## TODO you can get the snapshot_id from the image itself without describing instance and volume
	## i.e. ec2-describe-images $src_origin_ami

	# Create a new volume from the source snapshot
	echo "Creating a new source volume from the original snapshot ..."
	new_volume_id=$(ec2-create-volume --region $src_region --snapshot $src_snapshot_id -z $src_availability_zone | egrep ^VOLUME | cut -f2)
	echo "New source volume created from snapshot $src_snapshot_id with id: $new_volume_id"

	# Attach the new volume to the source instance
	ec2-attach-volume --region $src_region $new_volume_id -i $src_instance_id -d $src_device

	# Wait for the volume to be ok
	while volume_status=$(ec2-describe-volume-status --region $src_region $new_volume_id | \
	  egrep ^VOLUME | cut -f4) && [ "$volume_status" != "ok" ]; do echo -n .; sleep 1; done

	echo "New volume $new_volume_id attached to instance $src_instance_id: $volume_status"
fi

# Prepare the Destination Instance and Volume
dst_keypair=tiziano
dst_fullpath_keypair=/home/acca/.ssh/tiziano-aws-eu-west-1.pem
dst_availability_zone=eu-west-1b
dst_instance_type=m1.large
dst_region=eu-west-1
# ubuntu-precise-12.04-amd64-server-20120424  ==  plain Ubuntu 12.04 AMI EBS-backed
dst_origin_ami=ami-e1e8d395
#aki-62695816
dst_size=$src_size
dst_device=/dev/sdh
dst_dir=/dst
dst_user=tiziano

# dst_instance_id=

read -p "Do you have already a destination instance? [leave it blank or give us the id] "
dst_instance_id=$REPLY
if [ ! -z $dst_instance_id ]; then
	echo "Destination instance id to use: $dst_instance_id"
else
	echo "Starting up a destination instance and capture his instance id ..."

	# Start up the source instance and capture the instanceid
	dst_instance_id=$(ec2-run-instances \
	  --key $dst_keypair \
	  --availability-zone $dst_availability_zone \
	  --instance-type $dst_instance_type \
	  $dst_origin_ami \
	  --region $dst_region  | \
	  egrep ^INSTANCE | cut -f2)

	echo "Destination instance id: $dst_instance_id"

	# Wait for the instance to move to the “running” state
	while dst_public_fqdn=$(ec2-describe-instances --region $dst_region "$dst_instance_id" | \
	  egrep ^INSTANCE | cut -f4) && test -z $dst_public_fqdn; do echo -n .; sleep 1; done

	echo ""
	echo "Destination instance is running with fqdn: $dst_public_fqdn"
fi


read -p "Does the instance have already an empty destination attached? [leave it blank or give us the id] "
dst_volume_id=$REPLY
if [ ! -z $dst_volume_id ]; then
	echo "Empty destination volume id to use: $new_volume_id"
else
	# Create an empty destination volume
	dst_volume_id=$(ec2-create-volume --region $dst_region --size $dst_size -z $dst_availability_zone | egrep ^VOLUME | cut -f2)
	echo "New volume id: $dst_volume_id"

	# Attach the new volume to the destination instance 
	ec2-attach-volume --region $dst_region $dst_volume_id -i $dst_instance_id -d $dst_device

	# Wait for the new volume to be ok
	while volume_status=$(ec2-describe-volume-status --region $dst_region $dst_volume_id | \
	  egrep ^VOLUME | cut -f4) && [ "$volume_status" != "ok" ]; do echo -n .; sleep 1; done

	echo "New volume $dst_volume_id attached to instance $dst_instance_id: $volume_status"
fi

## Copy the data from the source volume to the destination volume

echo "Copying your target region keypair to your source instance ..."
scp -i $src_fullpath_keypair $dst_fullpath_keypair ${src_user}@${src_public_fqdn}:.ssh

echo "Mounting source and destination volumes on their instances ..."
ssh -i $src_fullpath_keypair ${src_user}@${src_public_fqdn} sudo mkdir -p $src_dir
ssh -i $src_fullpath_keypair ${src_user}@${src_public_fqdn} sudo mount $src_device $src_dir
ssh -i $dst_fullpath_keypair ${dst_user}@${dst_public_fqdn} sudo mkfs.ext3 -F $dst_device
ssh -i $dst_fullpath_keypair ${dst_user}@${dst_public_fqdn} sudo mkdir -p $dst_dir
ssh -i $dst_fullpath_keypair ${dst_user}@${dst_public_fqdn} sudo mount $dst_device $dst_dir

ec2-describe-instances --region $dst_region "$dst_instance_id" > /tmp/dst_instance_info
dst_internal_fqdn=$(egrep ^INSTANCE /tmp/dst_instance_info | cut -f5); 
echo "Destination instance is running with internal fqdn: $dst_internal_fqdn"
dst_kernel=$(egrep ^INSTANCE /tmp/dst_instance_info | cut -f13); 
echo "Kernel id of target ami: $dst_kernel"
dst_ramdisk=$(egrep ^INSTANCE /tmp/dst_instance_info | cut -f14);
echo "Ramdisk id of target ami: $dst_ramdisk"





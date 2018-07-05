#!/usr/bin/env sh
# Compute the mean image from the cifar100 training lmdb


EXAMPLE=/media/path/to/datasets/ # Location of cifar100_train_lmdb
DATA=/media/path/to/datasets/ # Where to store the mean.binaryproto
TOOLS=build/tools # Location of compute_image_mean (Inside CAFFE_HOME)

$TOOLS/compute_image_mean $EXAMPLE/cifar100_train_lmdb \
  $DATA/cifar100_mean.binaryproto

echo "cifar100_mean.binaryproto file generation is done."

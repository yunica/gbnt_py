#!/usr/bin/env bash

outDir=data

mkdir -p $outDir

python3 src/run.py \
  --folder_path=$outDir
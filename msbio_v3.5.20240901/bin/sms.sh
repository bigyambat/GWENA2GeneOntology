#!/usr/bin/env sh
singularity run --writable-tmpfs --bind $PWD/data:/data --bind $PWD/license:/license msbio2.sif /msbio/mylib/ms/smsbio2.sh $@

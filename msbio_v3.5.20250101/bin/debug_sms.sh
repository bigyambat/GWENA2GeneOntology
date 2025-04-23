#!/usr/bin/env sh
singularity shell --writable-tmpfs --bind $PWD/data:/data --bind $PWD/license:/license msbio2.sif

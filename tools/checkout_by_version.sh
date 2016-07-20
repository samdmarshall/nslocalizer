#!/bin/bash
commit_hash="$1"
actual_commit=`git rev-list --all --parents | grep ". $commit_hash" | awk '{print $1}'`
git checkout $actual_commit
#!/bin/bash
for f in ../../../log/*.log
do
  echo '' > $f
done
ls -la
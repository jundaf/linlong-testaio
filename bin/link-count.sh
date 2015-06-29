#!/bin/bash

echo -n ":5555  "
netstat -na | awk '$4 ~ /5555$/ && $NF ~ /ESTABLISHED/' | wc -l

echo -n ":5556  "
netstat -na | awk '$4 ~ /5556$/ && $NF ~ /ESTABLISHED/' | wc -l

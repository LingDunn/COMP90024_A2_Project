#!/bin/bash

. ./grp-52-openrc.sh; ansible-playbook -vv mrc.yaml | tee output.txt
#!/bin/bash

for i in `cat pip_lists.txt`; do ./flask/bin/pip install $i; done;

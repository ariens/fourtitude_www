#!/bin/bash 

./flask/bin/pip list | perl -pne 's/\s\(.*//'

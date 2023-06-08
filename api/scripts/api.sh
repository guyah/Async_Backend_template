#!/bin/bash
hypercorn --reload -w 1 --bind 0.0.0.0:80 --log-level=debug --access-logfile - --error-log - srcs.main:app
#!/bin/bash
celery -A srcs.tasks.celery worker -c 1 --loglevel=info
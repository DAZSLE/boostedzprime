#!/bin/bash
default_port=8889
port="${1:-$default_port}"
jupyter notebook --port $port

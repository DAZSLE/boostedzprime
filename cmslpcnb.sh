#!/bin/bash
if [ -z "$1" ]; then
	PORT=8889;
else
	PORT="$1";
fi
myname=$USER
ssh -N -L localhost:${PORT}:localhost:${PORT} $myname@cmslpc-sl7.fnal.gov

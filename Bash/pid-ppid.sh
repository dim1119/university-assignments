#!/bin/bash


#ps aux | awk  '{if( $11 == "/init" ) print $1,$3}'


PARENT=$(pidof init)
ps -eo pid,ppid --ppid $PARENT 
ps -e --ppid $PARENT| wc -l
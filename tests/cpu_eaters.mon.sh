#!/bin/bash

PATH="/sbin:/usr/sbin:${PATH}"
rcommand=${0##*/}
rpath=${0%/*}
#*/ (this is needed to fix vi syntax highlighting)
source ${rpath}/../conf/mon.conf

echo ""
echo "CPU eaters:"
echo "-----------"

ps aux | awk '{print $3" "$11" "$12" "$13" "$14" "$15}' | grep -v ^0.0 | grep -v COMMAND | while read LINE; do a=${LINE%% *}; a=${a#*.}; if [[ $a -gt $CPU_EATERS_MIN ]]; then echo $LINE; fi | while read LINE; do echo "<**> $LINE"; done; done

#!/usr/bin/env bash
# Copyright (C) 2008-2011 Igor Simonov (me@igorsimonov.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


rcommand=${0##*/}
rpath=${0%/*}
#*/ (this is needed to fix vi syntax highlighting)
DIFF=`which diff 2>/dev/null`
[ -z "$DIFF" ] && echo "Diff utility not found, exiting" && exit 1
SED=`which sed 2>/dev/null`
[ -z "$SED" ] && echo "Sed utility not found, exiting" && exit 1
SSH=`which ssh 2>/dev/null`
[ -z "$SSH" ] && echo "Ssh utility not found, exiting" && exit 1
possible_options="cluster help"
necessary_options=""
#[ "X$*" == "X" ] && echo "Can't run without options. Possible options are: ${possible_options}" && exit 1
for s_option in "${@}"
do
  found=0
  case ${s_option} in
  --*=*)
    s_optname=`expr "X$s_option" : 'X[^-]*-*\([^=]*\)'`  
    s_optarg=`expr "X$s_option" : 'X[^=]*=\(.*\)'` 
    ;;
  --*)
    s_optname=`expr "X$s_option" : 'X[^-]*-*\([^=]*\)'`    
    s_optarg='yes' 
    ;;
  *=*)
    echo "Wrong syntax: options must start with a double dash"
    exit 1
    ;;
  *)
    s_param=${s_option}
    s_optname=''
    s_optarg=''
    ;;
  esac
  for option in `echo $possible_options | sed 's/,//g'`; do 
    [ "X$s_optname" == "X$option" ] && eval "$option=${s_optarg}" && found=1
  done
  [ "X$s_option" == "X$s_param" ] && found=1
  if [[ found -ne 1 ]]; then 
    echo "Unknown option: $s_optname"
    exit 1
  fi
done
if [ "X$help" == "Xyes" ] ; then
  echo "Usage: ${0##*/} <options>"
  echo 
  echo "Without options all found clusters will be synced"
  echo
  echo "Options:"
  echo
  echo "  --cluster=clustername    - syncs only this single cluster."
  exit 0
fi
found=0

for option in `echo $necessary_options | sed 's/,//g'`; do
  [ "X$(eval echo \$$option)" == "X" ] && missing_options="${missing_options}, --${option}" && found=1
done
if [[ found -eq 1 ]]; then
  missing_options=${missing_options#*,}
  echo "Necessary options: ${missing_options} not found"
  exit 1
fi

source ${rpath}/../conf/cloud.conf

for var in JAVA_HOME EC2_HOME EC2_PRIVATE_KEY EC2_CERT EC2_REGION EC2_TOOLS_BIN_PATH ; do
  [ -z "`eval echo \\$\$var`" ] && echo "$var is not defined! Define it in conf/cloud.conf please." && exit 1
done
PATH="${EC2_TOOLS_BIN_PATH}:${PATH}"
export JAVA_HOME EC2_HOME EC2_PRIVATE_KEY EC2_CERT EC2_REGION PATH
TMPDIR=/tmp/m_script/cloud
install -d $TMPDIR
`which date` >> ${rpath}/../cloud.log
echo "------------------" >> ${rpath}/../cloud.log

changed=0
[ -f $TMPDIR/ec2.servers.ips ] && mv $TMPDIR/ec2.servers.ips $TMPDIR/ec2.servers.ips.prev
[ -x ${EC2_TOOLS_BIN_PATH}/ec2-describe-instances ] || (echo "ec2-describe-instances binary not found! Exiting.." >> ${rpath}/../cloud.log && exit 1)
  
${EC2_TOOLS_BIN_PATH}/ec2-describe-instances -K "$EC2_PRIVATE_KEY" -C "$EC2_CERT" --region $EC2_REGION | sed 's/\t/|/g' > $TMPDIR/ec2.servers.tmp
firstline=1
while read SERVER
do
  if [[ $SERVER =~ ^RESERVATION ]] ; then 
    if [[ $firstline -eq 0 ]] ; then
      sname=`$SSH -o StrictHostKeyChecking=no $inIP hostname 2>/dev/null`
      [ "X$sname" == "X" ] && echo "Unable to retrieve hostname of the server with IP $inIP|$extIP" >> ${rpath}/../cloud.log
      [ "X$state" == "Xrunning" ] && echo "$inIP|$extIP|$iID|$ami|$state|$keypair|$isize|$secgroup|$started|$zone|$aki|$ari|$sname|$cluster" >> $TMPDIR/ec2.servers.ips
      unset inIP extIP iID ami state keypair isize secgroup started zone aki ari cluster sname
    else
      firstline=0
    fi
    secgroup=`echo $SERVER | awk -F'|' '{print $4}'`
  fi
  if [[ $SERVER =~ ^INSTANCE ]] ; then
    inIP=`echo $SERVER | awk -F'|' '{print $18}'`
    extIP=`echo $SERVER | awk -F'|' '{print $17}'`
    iID=`echo $SERVER | awk -F'|' '{print $2}'`
    ami=`echo $SERVER | awk -F'|' '{print $3}'`
    state=`echo $SERVER | awk -F'|' '{print $6}'`
    keypair=`echo $SERVER | awk -F'|' '{print $7}'`
    isize=`echo $SERVER | awk -F'|' '{print $10}'`
    started=`echo $SERVER | awk -F'|' '{print $11}'`
    zone=`echo $SERVER | awk -F'|' '{print $12}'`
    aki=`echo $SERVER | awk -F'|' '{print $13}'`
    ari=`echo $SERVER | awk -F'|' '{print $14}'`
  fi
  if [[ $SERVER =~ ^TAG ]] ; then
    tag=`echo $SERVER | awk -F'|' '{print $4}'`
    [ "X$tag" == "Xcluster" ] && cluster=`echo $SERVER | awk -F'|' '{print $5}'`
  fi
done<$TMPDIR/ec2.servers.tmp
[ -z "$inIP" ] && echo "ERROR: empty IP!" >> ${rpath}/../cloud.log && exit 1
sname=`$SSH -o StrictHostKeyChecking=no $inIP hostname 2>/dev/null`
[ "X$sname" == "X" ] && echo "Unable to retrieve hostname of the server with IP $inIP|$extIP" >> ${rpath}/../cloud.log
[ "X$state" == "Xrunning" ] && echo "$inIP|$extIP|$iID|$ami|$state|$keypair|$isize|$secgroup|$started|$zone|$aki|$ari|$sname|$cluster" >> $TMPDIR/ec2.servers.ips
unset inIP extIP iID ami state keypair isize secgroup started zone aki ari cluster sname

[ -f $TMPDIR/ec2.servers.ips.prev ] && [ -f $TMPDIR/ec2.servers.ips ] && [ -z "`$DIFF -q $TMPDIR/ec2.servers.ips.prev $TMPDIR/ec2.servers.ips`" ] && exit 0

$SED -i -e '/^#/!d' ${rpath}/../servers.list
echo >> ${rpath}/../servers.list
while read SERVER
do
  inIP=`echo $SERVER | awk -F'|' '{print $1}'`
  sname=`echo $SERVER | awk -F'|' '{print $13}'`
  srole=`echo $SERVER | awk -F'|' '{print $14}'`
  echo "$inIP $sname $srole" >> ${rpath}/../servers.list
done<$TMPDIR/ec2.servers.ips

if [ -n "$NGINX_PROXY_CLUSTER_CONF_DIR" ] ; then
  ${rpath}/update_nginx_proxy.sh
fi
${rpath}/update_hosts_file.sh
${rpath}/update_mynetworks.sh
#${rpath}/update_firewalls.sh


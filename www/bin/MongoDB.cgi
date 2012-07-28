#!/bin/bash

scriptname=${0%.cgi}
scriptname=${scriptname##*/}
source "${PWD}/../../lib/dash_functions.sh"
print_cgi_headers
print_nav_bar "MongoDB|Servers" "sharding|Sharding" "collections|Collections"
print_page_title "host:port" "Status" "Memory Res/Virt" "Conn" "Curr/Avail" "Bandwidth In/Out" "Requests / sec"

IFS1=$IFS
IFS='
'
if [ `cat "${PWD}/../../standalone/${scriptname}/mongo_config_servers.list" | wc -l` -gt 0 ] ; then

  print_cluster_header "configservers|Configuration Servers"
  
    for s in `cat "${PWD}/../../standalone/${scriptname}/mongo_config_servers.list"` ; do
      port=${s##*:}
      name=${s%:*}
      id="${name}_${port}"
      [ -n "$port" ] && wport=`expr $port + 1000`
      echo "<div class=\"server\" id=\"${name}:${port}\">"
        echo "<div class=\"servername\" id=\"${id}_name\" onClick=\"showData('${id}_name','/${scriptname}')\">${name}:${port}<div id=\"data_${id}_name\" class=\"dhtmlmenu\" style=\"display: none\"></div></div>"
        echo "<div class=\"status\" id=\"${id}_http\" onclick=\"showURL('${id}_http','http://${name}:${wport}','${scriptname}')\">HTTP<div id=\"data_${id}_http\" class=\"dhtmlmenu\" style=\"display: none\"></div></div>"
        if [ "X`grep ^status\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`" == "X1" ] ; then
          echo "<div class=\"status statusok\" id=\"${id}_status\" onclick=\"showDetails('${id}_status','mongostatus')\">OK</div>"
        else
          echo "<div class=\"status statuserr\" id=\"${id}_status\" onclick=\"showDetails('${id}_status','mongostatus')\">Error</div>"
        fi
        echo "<div class=\"status\" id=\"${id}_mem\">`grep ^memRes\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^memVir\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
        echo "<div class=\"status\" id=\"${id}_conn\">`grep ^connCurrent\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^connAvailable\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
        
        echo "<div class=\"status\" id=\"${id}_bw\">`grep '^Bandwidth in ' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'` / `grep '^Bandwidth out ' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'`</div>"
        echo "<div class=\"status\" id=\"${id}_qps\" onclick=\"showDetails('${id}_qps','mongoqps')\">`grep '^Network requests per second' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'`</div>"
      echo "</div>"
      echo "<div class=\"details\" id=\"${name}:${port}_details\"></div>"
    done
    
  print_cluster_bottom
  
# Standalone servers
elif [ `cat "${PWD}/../../standalone/${scriptname}/mongo_servers.list" | wc -l` -gt 0 ] ; then
  
  print_cluster_header "mongoservers|MongoDB Servers"
  
    for rs in `cat "${PWD}/../../standalone/${scriptname}/mongo_servers.list" | cut -d'|' -f2 | sort | uniq` ; do
      echo "<div class=\"server\" id=\"${rs}\">"
      echo "<div class=\"servername\" id=\"${rs}_name\">Replica Set: ${rs}</div>"
      echo "</div>"
      for s in `cat "${PWD}/../../standalone/${scriptname}/mongo_servers.list" | grep "|${rs}|" | cut -d'|' -f1,3` ; do
        host=${s%|*}
        role=${s##*|}
        port=${host##*:}
        name=${host%:*}
        id="${name}_${port}"
        [ -n "$port" ] && wport=`expr $port + 1000`
        echo "<div class=\"server\" id=\"${name}:${port}\">"
          echo "<div class=\"servername\" id=\"${id}_name\" onClick=\"showData('${id}_name','/${scriptname}')\">${name}:${port}<span class=\"${role}\" title=\"${role}\">`echo $role | cut -b 1 | sed 's|.|\U&|'`</span><div id=\"data_${id}_name\" class=\"dhtmlmenu\" style=\"display: none\"></div></div>"
          echo "<div class=\"status\" id=\"${id}_http\" onclick=\"showURL('${id}_http','http://${name}:${wport}','${scriptname}')\">HTTP<div id=\"data_${id}_http\" class=\"dhtmlmenu\" style=\"display: none\"></div></div>"
          if [ "X`grep ^status\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`" == "X1" ] ; then
            echo "<div class=\"status statusok\" id=\"${id}_status\" onclick=\"showDetails('${id}_status','mongostatus')\">OK</div>"
          else
            echo "<div class=\"status statuserr\" id=\"${id}_status\" onclick=\"showDetails('${id}_status','mongostatus')\">Error</div>"
          fi
          echo "<div class=\"status\" id=\"${id}_mem\">`grep ^memRes\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^memVir\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
          echo "<div class=\"status\" id=\"${id}_conn\">`grep ^connCurrent\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^connAvailable\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
          
          echo "<div class=\"status\" id=\"${id}_bw\">`grep '^Bandwidth in ' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'` / `grep '^Bandwidth out ' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'`</div>"
          qps=`grep '^Network requests per second' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'`
          [ -n "$qps" ] || qps=`grep '^Total' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | awk '{print $2}'`
          echo "<div class=\"status\" id=\"${id}_qps\" onclick=\"showDetails('${id}_qps','mongoqps')\">$qps</div>"
        echo "</div>"
        echo "<div class=\"details\" id=\"${name}:${port}_details\"></div>"
      done
    done
### Not members of any RS
    for s in `cat "${PWD}/../../standalone/${scriptname}/mongo_servers.list" | grep ^.*\|$` ; do
      host=${s%|*}
      role=${s##*|}
      port=${host##*:}
      name=${host%:*}
      id="${name}_${port}"
      [ -n "$port" ] && wport=`expr $port + 1000`
      echo "<div class=\"server\" id=\"${name}:${port}\">"
        echo "<div class=\"servername\" id=\"${id}_name\" onClick=\"showData('${id}_name','/${scriptname}')\">${name}:${port}<span class=\"${role}\" title=\"${role}\">`echo $role | cut -b 1 | sed 's|.|\U&|'`</span><div id=\"data_${id}_name\" class=\"dhtmlmenu\" style=\"display: none\"></div></div>"
        echo "<div class=\"status\" id=\"${id}_http\" onclick=\"showURL('${id}_http','http://${name}:${wport}','${scriptname}')\">HTTP<div id=\"data_${id}_http\" class=\"dhtmlmenu\" style=\"display: none\"></div></div>"
        if [ "X`grep ^status\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`" == "X1" ] ; then
          echo "<div class=\"status statusok\" id=\"${id}_status\" onclick=\"showDetails('${id}_status','mongostatus')\">OK</div>"
        else
          echo "<div class=\"status statuserr\" id=\"${id}_status\" onclick=\"showDetails('${id}_status','mongostatus')\">Error</div>"
        fi
        echo "<div class=\"status\" id=\"${id}_mem\">`grep ^memRes\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^memVir\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
        echo "<div class=\"status\" id=\"${id}_conn\">`grep ^connCurrent\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^connAvailable\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
        
        echo "<div class=\"status\" id=\"${id}_bw\">`grep '^Bandwidth in ' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'` / `grep '^Bandwidth out ' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'`</div>"
        qps=`grep '^Network requests per second' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'`
        [ -n "$qps" ] || qps=`grep '^Total' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | awk '{print $2}'`
        echo "<div class=\"status\" id=\"${id}_qps\" onclick=\"showDetails('${id}_qps','mongoqps')\">$qps</div>"
      echo "</div>"
      echo "<div class=\"details\" id=\"${name}:${port}_details\"></div>"
    done
    
  print_cluster_bottom
  
fi

if [ `cat "${PWD}/../../standalone/${scriptname}/mongo_shards.list" | wc -l` -gt 0 ] ; then

  print_cluster_header "shardservers|Shard Servers"
  
    for s in `cat "${PWD}/../../standalone/${scriptname}/mongo_shards.list"|cut -d'|' -f1` ; do
      port=`echo $s | awk '{print $1}' | cut -d':' -f2`
      name=`echo $s | awk '{print $1}' | cut -d':' -f1`
      id="${name}_${port}"
      [ -n "$port" ] && wport=`expr $port + 1000`
      echo "<div class=\"server\" id=\"${name}:${port}\">"
        echo "<div class=\"servername\" id=\"${id}_name\" onClick=\"showData('${id}_name','/${scriptname}')\">${name}:${port}<div id=\"data_${id}_name\" class=\"dhtmlmenu\" style=\"display: none\"></div></div>"
        echo "<div class=\"status\" id=\"${id}_http\" onclick=\"showURL('${id}_http','http://${name}:${wport}','${scriptname}')\">HTTP<div id=\"data_${id}_http\" class=\"dhtmlmenu\" style=\"display: none\"></div></div>"
        if [ "X`grep ^status\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`" == "X1" ] ; then
          echo "<div class=\"status statusok\" id=\"${id}_status\" onclick=\"showDetails('${id}_status','mongostatus')\">OK</div>"
        else
          echo "<div class=\"status statuserr\" id=\"${id}_status\" onclick=\"showDetails('${id}_status','mongostatus')\">Error</div>"
        fi
        echo "<div class=\"status\" id=\"${id}_mem\">`grep ^memRes\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^memVir\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
        echo "<div class=\"status\" id=\"${id}_conn\">`grep ^connCurrent\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^connAvailable\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
        echo "<div class=\"status\" id=\"${id}_bw\">`grep '^Bandwidth in ' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'` / `grep '^Bandwidth out ' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'`</div>"
        qps=`grep '^Network requests per second' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'`
        [ -n "$qps" ] || rps=`grep '^Total' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | awk '{print $2}'`
        echo "<div class=\"status\" id=\"${id}_qps\" onclick=\"showDetails('${id}_qps','mongoqps')\">$qps</div>"
      echo "</div>"
      echo "<div class=\"details\" id=\"${name}:${port}_details\"></div>"
    done
    
  print_cluster_bottom
  
fi

if [ `cat "${PWD}/../../standalone/${scriptname}/mongo_mongos_servers.list" | wc -l` -gt 0 ] ; then

  print_cluster_header "balancers|Balancers"
  
    for s in `cat "${PWD}/../../standalone/${scriptname}/mongo_mongos_servers.list"` ; do
      port=${s##*:}
      name=${s%:*}
      id="${name}_${port}"
      install -d "${PWD}/../${scriptname}/balancers/${id}"
      [ -n "$port" ] && wport=`expr $port + 1000`
      echo "<div class=\"server\" id=\"${name}:${port}\">"
        echo "<div class=\"servername\" id=\"${id}_name\" onClick=\"showData('${id}_name','/${scriptname}')\">${name}:${port}<div id=\"data_${id}_name\" class=\"dhtmlmenu\" style=\"display: none\"></div></div>"
        echo "<div class=\"status\" id=\"${id}_http\" onclick=\"showURL('${id}_http','http://${name}:${wport}','${scriptname}')\">HTTP<div id=\"data_${id}_http\" class=\"dhtmlmenu\" style=\"display: none\"></div></div>"
        if [ "X`grep ^status\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`" == "X1" ] ; then
          echo "<div class=\"status statusok\" id=\"${id}_status\" onclick=\"showDetails('${id}_status','mongostatus')\">OK</div>"
        else
          echo "<div class=\"status statuserr\" id=\"${id}_status\" onclick=\"showDetails('${id}_status','mongostatus')\">Error</div>"
        fi
        echo "<div class=\"status\" id=\"${id}_mem\">`grep ^memRes\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^memVir\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
        echo "<div class=\"status\" id=\"${id}_conn\">`grep ^connCurrent\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^connAvailable\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
        echo "<div class=\"status\" id=\"${id}_bw\">`grep '^Bandwidth in ' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'` / `grep '^Bandwidth out ' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'`</div>"
        qps=`grep '^Network requests per second' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | cut -d':' -f2 | sed 's| *||g'`
        [ -n "$qps" ] || rps=`grep '^Total' "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.report" | awk '{print $2}'`
        echo "<div class=\"status\" id=\"${id}_qps\" onclick=\"showDetails('${id}_qps','mongoqps')\">$qps</div>"
      echo "</div>"
      echo "<div class=\"details\" id=\"${name}:${port}_details\"></div>"
    done
    
  print_cluster_bottom
  
fi
IFS=$IFS1


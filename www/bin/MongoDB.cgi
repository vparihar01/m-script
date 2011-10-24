#!/bin/bash
echo "Pragma: no-cache"
echo "Expires: 0"
echo "Content-Cache: no-cache"
echo "Content-type: text/html"
echo ""

scriptname=${0%.cgi}
scriptname=${scriptname##*/}

for script in ${PWD}/../../standalone/${scriptname}/rc/*.mon ; do
  [ -x "$script" ] && $script
done

IFS1=$IFS
IFS='
'
if [ -f "${PWD}/../../standalone/${scriptname}/mongo_config_servers.list" ] ; then
  echo "<div class=\"clustername\">Configuration servers</div>"
  echo "<div class=\"cluster\" id=\"configservers\">"
    for s in `cat "${PWD}/../../standalone/${scriptname}/mongo_config_servers.list"` ; do
      port=${s##*:}
      name=${s%:*}
      id=${name}_${port}
      [ -n "$port" ] && wport=`expr $port + 1000`
      echo "<div class=\"servername\" id=\"${id}\">${name}:${port}"
      echo "</div>"
      echo "<div class=\"status\" id=\"${id}_http\" onclick=\"showURL('${id}_http','http://${name}:${wport}','${scriptname}')\">HTTP<div id=\"data_${id}_http\" class=\"dhtmlmenu\" style=\"display: none\"></div></div>"
      if [ "X`grep ^status\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`" == "X1" ] ; then
        echo "<div class=\"status statusok\" id=\"${id}_status\">OK</div>"
      else
        echo "<div class=\"status statuserr\" id=\"${id}_status\">Error</div>"
      fi
      echo "<div class=\"status\" id=\"${id}_mem\">`grep ^memRes\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^memVir\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
      echo "<div class=\"status\" id=\"${id}_conn\">`grep ^connCurrent\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^connAvailable\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
    done
  echo "</div>"
fi

if [ -f "${PWD}/../../standalone/${scriptname}/mongo_shards.list" ] ; then
  echo "<div class=\"clustername\">Shard servers</div>"
  echo "<div class=\"cluster\" id=\"shardservers\">"
    for s in `cat "${PWD}/../../standalone/${scriptname}/mongo_shards.list"` ; do
      port=`echo $s | awk '{print $1}' | cut -d':' -f2`
      name=`echo $s | awk '{print $1}' | cut -d':' -f1`
      id=${name}_${port}
      install -d "${PWD}/../${scriptname}/shardservers/${id}"
      [ -n "$port" ] && wport=`expr $port + 1000`
      echo "<div class=\"servername\" id=\"${id}\">${name}:${port}"
      echo "</div>"
      echo "<div class=\"status\" id=\"${id}_http\" onclick=\"showURL('${id}_http','http://${name}:${wport}','${scriptname}')\"><a href='#'>HTTP</a><div id=\"data_${id}_http\" class=\"dhtmlmenu\" style=\"display: none\"></div></div>"
      if [ "X`grep ^status\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`" == "X1" ] ; then
        echo "<div class=\"status statusok\" id=\"${id}_status\">OK</div>"
      else
        echo "<div class=\"status statuserr\" id=\"${id}_status\">Error</div>"
      fi
      echo "<div class=\"status\" id=\"${id}_mem\">`grep ^memRes\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^memVir\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
      echo "<div class=\"status\" id=\"${id}_conn\">`grep ^connCurrent\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^connAvailable\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
    done
  echo "</div>"
fi

if [ -f "${PWD}/../../standalone/${scriptname}/mongo_mongos_servers.list" ] ; then
  echo "<div class=\"clustername\">Balancers</div>"
  echo "<div class=\"cluster\" id=\"balancers\">"
    for s in `cat "${PWD}/../../standalone/${scriptname}/mongo_mongos_servers.list"` ; do
      port=${s##*:}
      name=${s%:*}
      id=${name}_${port}
      install -d "${PWD}/../${scriptname}/balancers/${id}"
      [ -n "$port" ] && wport=`expr $port + 1000`
      echo "<div class=\"servername\" id=\"${id}\">${name}:${port}"
      echo "</div>"
      echo "<div class=\"status\" id=\"${id}_http\" onclick=\"showURL('${id}_http','http://${name}:${wport}','${scriptname}')\"><a href='#'>HTTP</a><div id=\"data_${id}_http\" class=\"dhtmlmenu\" style=\"display: none\"></div></div>"
      if [ "X`grep ^status\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`" == "X1" ] ; then
        echo "<div class=\"status statusok\" id=\"${id}_status\">OK</div>"
      else
        echo "<div class=\"status statuserr\" id=\"${id}_status\">Error</div>"
      fi
      echo "<div class=\"status\" id=\"${id}_mem\">`grep ^memRes\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^memVir\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
      echo "<div class=\"status\" id=\"${id}_conn\">`grep ^connCurrent\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2` / `grep ^connAvailable\| "${PWD}/../../standalone/${scriptname}/data/${name}:${port}.dat" | cut -d'|' -f2`</div>"
    done
  echo "</div>"
fi
IFS=$IFS1


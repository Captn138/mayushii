#!/bin/bash
RECIPIENT="mickael.almeida1308@gmail.com"
ST=$(speedtest -p no)
echo "$ST"
printf "Subject:SPEEDTEST\n\n$ST" | msmtp --debug --from=default -t ${RECIPIENT} > /dev/null

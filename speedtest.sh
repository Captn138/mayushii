#!/bin/bash
RECIPIENT="mickael.almeida1308@gmail.com"
ST=$(speedtest -p no)
echo "$ST"
content="Subject:SPEEDTEST

$ST"
echo "$content" | msmtp --debug --from=default -t ${RECIPIENT} > /dev/null

#!/usr/bin/env bash

cd /home/sean/website-subdomains/elite/maps
/home/sean/website-subdomains/elite/scripts/galmap-build/bin/galmap -c /home/sean/website-subdomains/elite/scripts/scrape_config.yaml -r /home/sean/website-subdomains/elite/scripts/galmap/resources $*

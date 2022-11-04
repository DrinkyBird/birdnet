#!/usr/bin/env bash

sudo cp /home/sean/website-subdomains/elite/scripts/munin/munin_elitedangerous_eddn_messages.py /usr/share/munin/plugins/elitedangerous_eddn_messages
sudo cp /home/sean/website-subdomains/elite/scripts/munin/munin_elitedangerous_eddn_journal.py /usr/share/munin/plugins/elitedangerous_eddn_journal
sudo cp /home/sean/website-subdomains/elite/scripts/munin/munin_elitedangerous_eddn_software.py /usr/share/munin/plugins/elitedangerous_eddn_software
sudo cp /home/sean/website-subdomains/elite/scripts/munin/munin_elitedangerous_systems_total.py /usr/share/munin/plugins/elitedangerous_starsystems_total
sudo cp /home/sean/website-subdomains/elite/scripts/munin/munin_elitedangerous_markets_total.py /usr/share/munin/plugins/elitedangerous_markets_total
sudo cp /home/sean/website-subdomains/elite/scripts/munin/munin_elitedangerous_eddn_client_types.py /usr/share/munin/plugins/elitedangerous_eddn_game_types
sudo cp /home/sean/website-subdomains/elite/scripts/munin/munin_elitedangerous_eddn_users.py /usr/share/munin/plugins/elitedangerous_eddn_users

sudo chmod +x /usr/share/munin/plugins/elitedangerous_*
sudo ln -s /usr/share/munin/plugins/elitedangerous_* /etc/munin/plugins/

sudo systemctl restart munin-node

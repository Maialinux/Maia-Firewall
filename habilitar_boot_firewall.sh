#!/usr/bin/env bash

sudo cp maiawall.service /etc/systemd/system/maiawall.service
sudo chmod 644 /etc/systemd/system/maiawall.service
sudo chmod +x /etc/init.d/maiawall
sudo systemctl daemon-reload
sudo systemctl enable maiawall.service
sudo systemctl start maiawall.service
sudo systemctl status maiawall.service
cp drone.service /etc/systemd/system/drone.service
sudo chmod 644 /etc/systemd/system/drone.service
systemctl enable drone.service
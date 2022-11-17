#! /bin/bash
docker kill mysql sber
docker rm mysql sber
docker image rm  fake_sber:dev
rm /etc/ssl/certs/rootCA.pem
rm /usr/local/share/ca-certificates/rootCA.crt
dirs=($(ls /home))
for dir in "${dirs[@]}"; do
  certutil -d sql:/home/$dir/.pki/nssdb -D -n custom-sber
done

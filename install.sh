#! /usr/bin/bash
echo "127.0.0.1 sber.ru" >> /etc/hosts
apt install -y libnss3-tools ca-certificates chromium
cp certs/rootCA.crt /usr/local/share/ca-certificates
update-ca-certificates

dirs=($(ls /home))
for dir in "${dirs[@]}"; do
  certutil -d sql:/home/$dir/.pki/nssdb -A -t "C,," -n "custom-sber"  -i ./certs/rootCA.crt 
done

docker run --name mysql -d \
    -p 3306:3306 \
    -e MYSQL_ROOT_PASSWORD=sql_password \
    --restart unless-stopped \
    mysql:8

docker build -t fake_sber:dev .
until [ "`docker inspect -f {{.State.Running}} mysql`"=="true" ]; do
    sleep 0.1;
done;
docker run --name sber -d \
    --net host \
    --restart unless-stopped \
    fake_sber:dev
docker start sber

sleep 10
sudo runuser -u $SUDO_USER -- chromium https://sber.ru:5000
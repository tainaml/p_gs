#!/bin/bash

echo "[INSTALL APP]"

# CRIANDO LOG
if [[ ! -d /var/log/rede_gsti ]]; then
    mkdir /var/log/rede_gsti/
    touch /var/log/rede_gsti/error.log
    chmod -R 777 /var/log/rede_gsti
fi


cd /var/www

ssh-add ~/.ssh/host_key/id_rsa
ssh-keyscan -H git.dominiodeteste.net >> ~/.ssh/known_hosts
ssh -T git@git.dominiodeteste.net

sudo ssh-add ~/.ssh/host_key/id_rsa
sudo ssh-keyscan -H git.dominiodeteste.net >> ~/.ssh/known_hosts
sudo ssh -T git@git.dominiodeteste.net

git submodule update --init --remote -f --rebase --merge --recursive
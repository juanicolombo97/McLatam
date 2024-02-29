#!/bin/bash
echo 'Iniciamos screen'

# Creamos una subshell para poder correr con el usuario de ubuntu
sudo -u ubuntu bash -c 'screen -dmS "programa" bash run_main.sh'

echo 'Terminamos screen'
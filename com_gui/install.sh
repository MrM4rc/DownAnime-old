#!/bin/bash

pacote=$(dpkg -l | grep "python3-pip")
tamanho=${#pacote}

diretorio_instalacao="/bin/downanime"

if [ -f "$diretorio_instalacao" ]
then
echo "tudo instalado"
else

    if [ $tamanho -gt 0 ]
    then
    pip3 install pyside2 robobrowser requests

    else
    sudo apt install python3-pip
    pip3 install pyside2 requests robobrowser
    fi
    
     mkdir ~/.local/share/DownAnime
    cp ./main.py ./downanime.py ./inter_downanime.py ./downanime.ico ~/.local/share/DownAnime/
    chmod +x ./downanime
    cp ./downanime /bin/
fi


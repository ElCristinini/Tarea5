#!/bin/bash
# Inicia roscore en segundo plano
roscore &
sleep 2

# Ejecuta el nodo talker
python3 talker.py

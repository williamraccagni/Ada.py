#!/bin/bash

for T_index in 200 400 600 800 1000
do
  python3 Adaboost.py $T_index > ~/Scrivania/Progetto\ Statistici/risultati/test_${T_index}.txt
done

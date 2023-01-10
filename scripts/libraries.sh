#!/bin/bash

libraries=(
    'pygame==2.1.2'
    'pandas==1.1.5'
    'numpy==1.21.6'
    'xlrd==1.2.0'
    'openpyxl==3.0.10'
    'PyPDF2==3.0.1'
    'reportlab==3.6.12'
    'matplotlib==3.5.3'
)

for library in "${libraries[@]}"
do
    pip install $library
done

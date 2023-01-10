#!/bin/bash

# array of extension IDs
extensions=(
    "GrapeCity.gc-excelviewer"
    "tomoki1207.pdf"
    "hnw.vscode-auto-open-markdown-preview"

)

for extension in "${extensions[@]}"
do
    code --install-extension $extension
done

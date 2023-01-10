#!/bin/bash
cd scripts/
files=(
    'extensions.sh'
    'libraries.sh'
)

for file in "${files[@]}"; do
    chmod +x ${file}
    ./${file}
done

cd ..
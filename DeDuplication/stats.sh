#!/bin/bash

# Base directory
base_dir=".././TeluguData"

# Directories to check
directories=("TeluguPost" "Tupaki" "TeluguStop")

# Loop through each directory
for dir in "${directories[@]}"; do
    dir_path="$base_dir/$dir"

    if [ -d "$dir_path" ]; then
        # Count number of files
        file_count=$(find "$dir_path" -type f | wc -l)

        # Calculate total size in MB and GB
        total_size_mb=$(du -sm "$dir_path" | cut -f1)
        total_size_gb=$(echo "scale=2; $total_size_mb / 1024" | bc)

        # Output results
        echo "Directory: $dir"
        echo "Number of files: $file_count"
        echo "Total size: $total_size_mb MB ($total_size_gb GB)"
        echo "----------------------------------------"
    else
        echo "Directory: $dir does not exist."
        echo "----------------------------------------"
    fi
done

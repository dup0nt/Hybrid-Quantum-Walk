#!/bin/bash
# The script will run in the current directory
CURRENT_DIR=$(pwd)

# Check if mprof is installed
if ! command -v mprof &> /dev/null
then
    echo "mprof could not be found, please install mprof."
    exit
fi

# Specify the filenames to plot
declare -a files_to_plot=("434990" "434991" "434992" "434993")

# Loop over specified mprof run files
for base_name in "${files_to_plot[@]}"; do
    # Form the run file name
    run_file="$CURRENT_DIR/$base_name.prof"
    
    # Check if the file exists
    if [ ! -f "$run_file" ]; then
        echo "File not found: $run_file"
        continue
    fi
    
    # Set the plot file name
    plot_file="$CURRENT_DIR/$base_name.png"
    
    # Generate the plot
    mprof plot -o "$plot_file" "$run_file"
    
    echo "Plot saved to $plot_file"
done

echo "All specified plots have been attempted. Check any 'File not found' errors if plots are missing."
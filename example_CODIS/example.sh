# Ryan M Harrison
# ryan.m.harrison@gmail.com
# Generate reference sequences for all sequence specification 
# configuration files.

abs_exec_path=$(dirname $(readlink -f $0))
for config in `ls $abs_exec_path/../config/*.cfg`; 
do 
    # Not worth my time to re-invent the wheel
    # http://stackoverflow.com/questions/965053/extract-filename-and-extension-in-bash
    filename=$(basename "$config")
    extension="${filename##*.}"
    basefilename="${filename%.*}"

    echo "#Writing fasta files for $basefilename"
    echo "#Using $config"
    python "$abs_exec_path"/../expand_sequence_cfg.py $config --output_dir $abs_exec_path/$basefilename
done

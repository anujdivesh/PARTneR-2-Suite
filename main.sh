#!/bin/bash

XML_FILE="/mnt/DATA/production/flag.xml"

get_flag_value() {
    grep -oP '(?<=<isRunning>).*?(?=</isRunning>)' "$XML_FILE"
}

set_flag_value() {
    sed -i "s|<isRunning>.*</isRunning>|<isRunning>$1</isRunning>|" "$XML_FILE"
}

is_running=$(get_flag_value)

if [ "$is_running" == "true" ]; then
    echo "Job is already running. Exiting..."
    exit 1
fi

set_flag_value "true"

echo "Running cron job..."
###############################MAIN#######################################
#!/bin/bash

#REMOVE input file
#rm /mnt/DATA/production/out.log

#CHECK JSON AND CSV
json_count=$(find /mnt/DATA/production -maxdepth 1 -type f -name "*.json" | wc -l)
csv_count=$(find /mnt/DATA/production -maxdepth 1 -type f -name "*.csv" | wc -l)
#echo $json_count
if [[ $json_count -ne 1 || $csv_count -ne 1 ]]; then
  echo "Too many/NO files supplied. Exiting."
  exit 1
fi

#COPY config.json and track.csv to appropriate locations
#COPY TO TCHA
cp /mnt/DATA/production/*.json /mnt/DATA/production/TCHA
cp /mnt/DATA/production/*.csv /mnt/DATA/production/TCHA

#COPY TO QUICKSURGE
cp /mnt/DATA/production/*.json /mnt/DATA/production/QuickSurge
cp /mnt/DATA/production/*.csv /mnt/DATA/production/QuickSurge

#RUN TCHA
echo "Running TCHA model"
##FOR DEV ONLY
#docker run -v /mnt/DATA/production/TCHA:/TCHA -ti --rm --cpuset-cpus="16-17" tcha-prod /bin/bash -c ". /opt/miniconda/bin/activate; cd /TCHA/tcrm; python main.py"
##FOR PROD
docker run -v /mnt/DATA/production/TCHA:/TCHA --rm --cpuset-cpus="22-22" tcha-prod /bin/bash -c ". /opt/miniconda/bin/activate; cd /TCHA/tcrm; python main.py"

#RUN QuickSurge
echo "Running QuickSurge Model"
##FOR DEV ONLY
#docker run -v /mnt/DATA/production/QuickSurge:/QuickSurge -ti --rm --cpuset-cpus="0-21" quickly /bin/bash -c ". /opt/conda/bin/activate; cd /QuickSurge/Python_Codes; python main_IDA_PDNA_StormSurge.py"
#FOR PROD
docker run -v /mnt/DATA/production/QuickSurge:/QuickSurge --rm --cpuset-cpus="0-21" quickly /bin/bash -c ". /opt/conda/bin/activate; cd /QuickSurge/Python_Codes; python main_IDA_PDNA_StormSurge.py"

#GET LATEST FILE FROM TCHA
latest_dir_tcha=$(realpath "$(ls -td /mnt/DATA/production/TCHA/output/*/ | head -n 1)")
echo $latest_dir_tcha
cp -r "$latest_dir_tcha"/* "/mnt/DATA/production/outputs"
echo "Copied TCHA."

#GET LATEST FILES FROM TCHA
latest_dir_quicksurge=$(realpath "$(ls -td /mnt/DATA/production/QuickSurge/Runs/*/ | head -n 1)")
echo $latest_dir_quicksurge
cp -r "$latest_dir_quicksurge"/* "/mnt/DATA/production/outputs"
echo "Copied QuickSurge."

#REMOVE CONFIG FILES FROM MAIN
rm /mnt/DATA/production/*.json
rm /mnt/DATA/production/*.csv

truncate -s 100M /mnt/DATA/production/out.log

XML_FILE="/mnt/DATA/production/flag.xml"

get_flag_value() {
    grep -oP '(?<=<isRunning>).*?(?=</isRunning>)' "$XML_FILE"
}

set_flag_value() {
    sed -i "s|<isRunning>.*</isRunning>|<isRunning>$1</isRunning>|" "$XML_FILE"
}


set_flag_value "false"

echo "HAZARD model run completed...."

#RUN RiskScape
find /mnt/DATA/production/outputs -name "local_wind_merged.tif" -exec cp {} /mnt/DATA/production/outputs \;
find /mnt/DATA/production/outputs -name "_merged.tif" -exec cp {} /mnt/DATA/production/outputs \;

search_directory="/mnt/DATA/production/outputs"

# Find the first JSON file in the specified directory
json_file=$(find "$search_directory" -maxdepth 1 -name "*.json" -print -quit)

# Check if a JSON file was found
if [ -z "$json_file" ]; then
  echo "No JSON file found in $search_directory"
  exit 1
fi

# Extract the domainCode from the JSON file
domain_code=$(grep -oP '"domainCode"\s*:\s*"\K[^"]+' "$json_file")
cd /mnt/DATA/production/rs-projects/pdie_ini/"$domain_code" || { echo "Directory $domain_code not found."; exit 1; }
echo "we are in the country directory $domain_code"

python3 /mnt/DATA/production/rs-projects/pdie_ini/edit_RMSC_track_riskscape.py 

#riskscape model run Cyclone-PDIE

risk_output="/mnt/DATA/production/rs-projects/pdie_ini/$domain_code/output/Cyclone-PDIE/"

#GET LATEST FILES FROM TCHA
latest_dir_quicksurge=$(realpath "$(ls -td /mnt/DATA/production/rs-projects/pdie_ini/$domain_code/output/Cyclone-PDIE/*/ | head -n 1)")
echo $latest_dir_quicksurge
cp -r "$latest_dir_quicksurge"/* "/mnt/DATA/production/impact_output"
echo "Copied RiskScape."


###############################MAIN#######################################

set_flag_value "false"

echo "Cron job completed."







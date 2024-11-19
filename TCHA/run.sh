#!/bin/bash

#docker run -v /mnt/DATA/QuickSurge-docker/QuickSurge:/QuickSurge --rm --cpuset-cpus="0-19" quick-surge /bin/bash -c ". /opt/miniconda/bin/activate; cd /QuickSurge/Python_Codes; python main_IDA_PDNA_StormSurge.py"


#docker run -v /mnt/DATA/TCHA:/TCHA --rm --cpuset-cpus="16-16" tcha /bin/bash -c ". /opt/miniconda/bin/activate; cd /TCHA/tcrm; python main.py"

docker run -v /mnt/DATA/production/TCHA:/TCHA -ti --rm --cpuset-cpus="16-20" tcha-prod /bin/bash -c ". /opt/miniconda/bin/activate; cd /TCHA/tcrm; python main.py"
echo "Model run Successful!"

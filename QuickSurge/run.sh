#!/bin/bash

docker run -v /mnt/DATA/production/QuickSurge:/QuickSurge -ti --rm --cpuset-cpus="0-36" quickly /bin/bash -c ". /opt/conda/bin/activate; cd /QuickSurge/Python_Codes; python main_IDA_PDNA_StormSurge.py"


echo "Model run Successful!"

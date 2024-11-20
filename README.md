# PARTneR2 - Rapid Tropical Cyclone Impact Assessment Tool
This repository contains suite of models that was developed under PARTneR-2 Project. Below is a guide on safely launching the model.

### 1. Prerequisite
- Access to machine [ssh/sftp]
  - contact noureddinet@spc.int or vincentk@spc.int or divesha@spc.int
- Cyclone track file from RSMC Nadi `csv format`. Sample file: [Link](https://github.com/anujdivesh/PARTneR-2-Suite/blob/main/20231023T030000Z_Official_Forecast_Track_2324_01F_Lola.csv)
  - it is important to breifly check the latest file you get with the sample above, esp datetime format.
- Configuration file `.json`. Sample file [Link](https://github.com/anujdivesh/PARTneR-2-Suite/blob/main/01_test_config.json)
  - `stormName` and `stormYear` information could be got from the track file.
  - `domainCode` to be from this list `["CK","VU","SA","TO"]` | CK = Cook Islands, VU = Vanuatu, SA = Samoa, TO = Tonga.
  - `trackFile` to be the same name as the file you are going to put on the server
  - `trackSource` remains as `RSMC`

### 2. Preliminary checks
- Ensure you have Two files, 1 x `.json` 1 x `.csv`
- In the working directory `/mnt/DATA/production`, we can see a `flag.xml`. If `isRunning` flag is set to `true`, means someone has already launched or is running the model, you may want to email and check the group. If the `isRunning` flag is set to `false`, then we are allowed to launch the model. These locks are set so there are no overlapping instances of model running.
- There can be a `Bug`, where the execution came to a halt, so we need to change `isRunning` flag to `false` in the `flag.xml`, before we can run the model.

### 3. Launching the model
- SCP/SFTP 1 x json config file and 1 x csv track file on `/mnt/DATA/production`
- The `crontab` is set to run on every 5th minute.
- You can monitor on the `/mnt/DATA/production/out.log` file.
  - Some common problems could occur
    - `Too many/NO files supplied. Exiting.` message, meaning there was no files `.csv` `.json` provided or there was many files provided. Ensure 1 of each is provided.
    - `Job is already running. Exiting...` message, meaning there could be an instance of the model being run.

### 4. HAZARD latest datasets
- A directory `/mnt/DATA/production/outputs` has been created to house latest results of the current run.

### 5. Judith, Sam, Sachin to continue......

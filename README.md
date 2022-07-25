# GCAM for CDR Policy Deployment Documentation
## Setup Instructions
Instance Requirements:
 - `r5a.4xlarge` (for full capabilities) with `45GB` of disk space
 - `m5a.2xlarge` (for build capabilities only)

1. Turn on instance and `ssh` into instance.

2. ```git clone https://github.com/ecwood/GCAM-CDR-modeling.git```

3. ```cd GCAM-CDR-modeling```

4. ```screen -S setup_gcam```

5. ```./setup_gcam.sh > ~/setup_gcam.log 2>&1```

6. Ctrl-A, Ctrl-D

## GCAM Basics
Important GCAM Repositories:
 - [gcam-core](https://github.com/JGCRI/gcam-core)
   - Full repository for GCAM
 - [gcam-doc](https://github.com/JGCRI/gcam-doc/)
   - GitHub backend for [official documentation](jgcri.github.io/gcam-doc/)
   - Acts as a searchable options for documentation
 - [gcamdata](https://github.com/JGCRI/gcamdata)
   - Contains the data system for GCAM
   - This includes all of the CSV files and R scripts to compile the GCAM XML files


## Process GCAM Output
Runtimes:
 - From scratch: ~17 minutes
 - From pickle file: ~2 minutes
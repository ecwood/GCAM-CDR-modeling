# Setup Instructions
Instance Requirements:
 - `r5a.4xlarge` (for full capabilities) with `45GB` of disk space
 - `m5a.2xlarge` (for build capabilities only)

1. Turn on instance and `ssh` into instance.

2. ```git clone https://github.com/ecwood/GCAM-CDR-modeling.git```

3. ```cd GCAM-CDR-modeling```

4. ```screen -S setup_gcam```

5. ```./setup_gcam.sh > ~/setup_gcam.log 2>&1```

6. Ctrl-A, Ctrl-D


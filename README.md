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

## Running GCAM Scenarios
- 
## Process GCAM Output
Runtimes:
 - From scratch: ~17 minutes
 - From pickle file: ~2 minutes

## Assorted Notes
 - Can change time frame of scenario in `modeltime.xml`, theoretically, but I haven't gotten it to work, giving errors like this:
```
ERROR:Invalid year: 2060 passed to Modeltime::getyr_to_per. 
ERROR:Invalid year: 2065 passed to Modeltime::getyr_to_per. 
ERROR:Invalid year: 2070 passed to Modeltime::getyr_to_per. 
ERROR:Invalid year: 2075 passed to Modeltime::getyr_to_per. 
ERROR:Invalid year: 2080 passed to Modeltime::getyr_to_per. 
ERROR:Invalid year: 2085 passed to Modeltime::getyr_to_per. 
ERROR:Invalid year: 2090 passed to Modeltime::getyr_to_per. 
ERROR:Invalid year: 2095 passed to Modeltime::getyr_to_per. 
ERROR:Invalid year: 2100 passed to Modeltime::getyr_to_per. 
```

## Implementing H.R. 7434
Things I've tried:
1. 6969631 (fixed the DAC output value to exactly H.R. 7434 levels; worked, but not robust enough for what I need)
2. daf4ace  (didn't do anything)
3. 57ad277 (didn't do anything)
4. Put in `carbon_tax_20_5.xml` in the `policy` spot (didn't do anything)
5. Adding these lines to the configuration file and reverting
```diff
-                 <Value name="policy-target-file">../input/policy/carbon_tax_20_5.xml</Value>
+                <Value name="policy-target-file">../input/policy/forcing_target_4p5.xml</Value>
...
                <Value name = "indenergy_emiss_USA">../input/gcamdata/xml/indenergy_emissions_USA.xml</Value>
                <Value name = "elc_emiss_USA">../input/gcamdata/xml/elc_emissions_USA.xml</Value>
                <Value name = "transport_emiss_USA">../input/gcamdata/xml/transport_emissions_USA.xml</Value>
                <Value name = "prc_usa">../input/gcamdata/xml/ind_urb_processing_sectors_USA.xml</Value>
                <Value name = "process_emiss_USA">../input/gcamdata/xml/ind_urb_proc_emissions_USA.xml</Value>
                <Value name = "refining_emiss_USA">../input/gcamdata/xml/refinery_emissions_USA.xml</Value>

                <Value name = "solver">../input/solution/cal_broyden_config.xml</Value>

                <Value name = "dac">../input/gcamdata/xml/dac_ssp2.xml</Value>
                <Value name = "dac_usa">../input/gcamdata/xml/dac_USA_ssp2.xml</Value>

+                <Value name = "policy_target">../input/policy/policy_target_4p5_spa1.xml</Value>
+                <Value name = "tax">../input/policy/carbon_tax_15_5.xml</Value>
```
(Didn't do anything) 
 - What is a dispatch?
```
Period 19: 2090
Model solved normally. Iterations period 19: 176. Total iterations: 15148

Period 20: 2095
Model solved normally. Iterations period 20: 283. Total iterations: 15431

Period 21: 2100
Model solved normally. Iterations period 21: 158. Total iterations: 15589

All model periods solved correctly.
Model run completed.
Policy Target Runner:  scenario dispatch #3

Starting a model run. Running period 21
Model run beginning.
Period 6: 2025
Model solved normally. Iterations period 6: 558. Total iterations: 16146
```
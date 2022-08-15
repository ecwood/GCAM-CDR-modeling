# How to Use GCAM to Implement DAC Deployment

## Setup
Instance Requirements:
 - `r5a.4xlarge` (for full capabilities) with `45GB` of disk space
 - `m5a.2xlarge` (for build capabilities only)

1. Turn on instance and `ssh` into instance.

2. ```git clone https://github.com/ecwood/GCAM-CDR-modeling.git```

3. ```cd GCAM-CDR-modeling```

4. ```screen -S setup_gcam```

5. ```./setup_gcam.sh > ~/setup_gcam.log 2>&1```

6. Ctrl-A, Ctrl-D

## Introduction to GCAM

### File Structure

```bash
.
├── CONTRIBUTING.md
├── cvs
│    └── objects
│        ├── build
│        ├── ccarbon_model
│        ├── climate
│        ├── configuration_files
│        ├── consumers
│        ├── containers
│        ├── demographics
│        ├── doxygen
│        ├── emissions
│        ├── functions
│        ├── java
│        ├── land_allocator
│        ├── main
│        ├── marketplace
│        ├── parallel
│        ├── policy
│        ├── reporting
│        ├── resources
│        ├── sectors
│        ├── solution
│        ├── target_finder
│        ├── technologies
│        └── util
├── exe
│    ├── gcam.exe
│    ├── logs
│    └── restart
├── input
│    ├── climate
│    ├── extra
│    ├── gcamdata
│    │   ├── chunk-generator
│    │   ├── data
│    │   ├── data-raw
│    │   ├── DESCRIPTION
│    │   ├── exec
│    │   ├── figures
│    │   ├── gcamdata.Rproj
│    │   ├── inst
│    │   │   ├── CITATION
│    │   │   └── extdata
│    │   │       ├── aglu
│    │   │       ├── common
│    │   │       ├── emissions
│    │   │       ├── energy
│    │   │       │   ├── GIS
│    │   │       │   └── mappings
│    │   │       ├── gcam-usa
│    │   │       │   ├── emissions
│    │   │       │   └── GIS
│    │   │       │       └── README.md
│    │   │       ├── mi_headers
│    │   │       ├── ModelInterface
│    │   │       ├── socioeconomics
│    │   │       ├── tests
│    │   │       └── water
│    │   ├── LICENSE
│    │   ├── man
│    │   ├── NAMESPACE
│    │   ├── R
│    │   ├── README.md
│    │   ├── renv
│    │   ├── renv.lock
│    │   ├── solution
│    │   ├── tests
│    │   ├── vignettes
│    │   │   ├── driverdrake_vignette.Rmd
│    │   │   └── usermod_vignette.Rmd
│    │   └── xml
│    ├── magicc
│    ├── policy
│    │   └── input-module
│    └── solution
├── LICENSE.md
├── Makefile
├── output
│    ├── database_basexdb
│    ├── gcam_diagnostics
│    │   ├── batch_queries
│    │   ├── gcam_data
│    │   ├── logs
│    │   ├── mappings
│    │   ├── post_process
│    │   ├── readme.md
│    │   └── scripts
│    ├── modelinterface
│    └── queries
├── README.md
└── util
    └── testing-framework
```

`${GCAM_HOME}/gcam-core/input/gcamdata`

## What is a GCAM Scenario?

### Components
 - [Configuration file](#configuration-files)
 - [Policy files](#policy-files)
 - [DAC files](#dac-files)

### Configuration Files
`policy-target-file`: This tag in the configuration file specifies what the main policy for the scenario will be. 

### Policy Files

### DAC Files

## Debugging Tips
 - You will likely need to reference the [documentation](http://jgcri.github.io/gcam-doc/) frequently. Utilize the search function on [gcam-doc](https://github.com/JGCRI/gcam-doc/) if you are trying to find something.
 - Be careful editing the `CSV` files. Things can get out of hand quickly due to the cross references between them.
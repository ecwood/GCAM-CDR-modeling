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
Annotation Key:
 - 🟧: Base directory explanation
 - 🟩: File explanation
 - 🟦: Core directory explanation
 - 🟪: Niche directory explanation

<pre><code>
.
├── CONTRIBUTING.md
├── cvs
│    └── objects 🟧 This is the folder that contains all of the C++ source code that makes up the model. (This is the code that the model solves with.) 🟧
│        ├── build
│        ├── ccarbon_model
│        ├── climate 🟪 This is where the Hector related files are located. Hector is a separate PNNL package that makes up the climate backbone of GCAM. 🟪
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
├── exe 🟧 This folder contains the files that a user uses to directly run the model at runtime. (i.e. in the run command) 🟧
│    ├── configuration_policy.xml 🟩 This is an example scenario that shows how to create a configuration file that includes a policy. <a href="https://github.com/ecwood/GCAM-CDR-modeling/blob/main/GCAM-DAC-Guide.md#configuration-files">Configuration File</a> 🟩
│    ├── configuration_ref.xml 🟩  🟩
│    ├── configuration_ssp.xml 🟩 🟩
│    ├── configuration_usa.xml 🟩 🟩
│    ├── debug_db.xml 🟩 🟩
│    ├── gcam.exe 🟩 🟩
│    ├── logs
│    └── restart
├── input 🟧 🟧
│    ├── climate
│    ├── extra
│    ├── gcamdata 🟦 🟦
│    │   ├── chunk-generator
│    │   ├── data
│    │   ├── data-raw
│    │   ├── DESCRIPTION
│    │   ├── exec
│    │   ├── figures
│    │   ├── gcamdata.Rproj
│    │   ├── inst
│    │   │   ├── CITATION
│    │   │   └── extdata 🟦 This folder is the root of all CSV files. 🟦
│    │   │       ├── aglu
│    │   │       ├── common
│    │   │       ├── emissions
│    │   │       ├── energy 🟪 This folder contains all of the global DAC related data. The following files are DAC related files in this folder. 🟪
│    │   │       │   ├── A62.calibration.csv 🟩 🟩
│    │   │       │   ├── A62.demand.csv 🟩 🟩
│    │   │       │   ├── A62.globaltech_co2capture.csv 🟩 🟩
│    │   │       │   ├── A62.globaltech_coef_ssp1.csv 🟩 🟩
│    │   │       │   ├── A62.globaltech_coef_ssp2.csv
│    │   │       │   ├── A62.globaltech_coef_ssp3.csv
│    │   │       │   ├── A62.globaltech_coef_ssp4.csv
│    │   │       │   ├── A62.globaltech_coef_ssp5.csv
│    │   │       │   ├── A62.globaltech_cost_ssp1.csv 🟩 🟩
│    │   │       │   ├── A62.globaltech_cost_ssp2.csv
│    │   │       │   ├── A62.globaltech_cost_ssp3.csv
│    │   │       │   ├── A62.globaltech_cost_ssp4.csv
│    │   │       │   ├── A62.globaltech_cost_ssp5.csv
│    │   │       │   ├── A62.globaltech_retirement.csv 🟩 🟩
│    │   │       │   ├── A62.globaltech_shrwt_ssp1.csv 🟩 🟩
│    │   │       │   ├── A62.globaltech_shrwt_ssp2.csv
│    │   │       │   ├── A62.globaltech_shrwt_ssp3.csv
│    │   │       │   ├── A62.globaltech_shrwt_ssp4.csv
│    │   │       │   ├── A62.globaltech_shrwt_ssp5.csv
│    │   │       │   ├── A62.PrimaryFuelCCoef.csv 🟩 🟩
│    │   │       │   ├── A62.sector.csv 🟩 🟩
│    │   │       │   ├── A62.subsector_interp.csv 🟩 🟩
│    │   │       │   ├── A62.subsector_logit.csv 🟩 🟩
│    │   │       │   ├── A62.subsector_shrwt.csv 🟩 🟩
│    │   │       │   ├── GIS
│    │   │       │   └── mappings
│    │   │       ├── gcam-usa 🟪 🟪
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
│    │   ├── R 🟦 🟦
│    │   │   ├── zchunk_batch_dac_USA_xml.R 🟩 🟩
│    │   │   ├── zchunk_batch_dac_xml.R 🟩 🟩
│    │   │   ├── zchunk_L262.dac.R 🟩 🟩
│    │   │   ├── zchunk_L262.dac_USA.R 🟩 🟩
│    │   │   └── zchunk_LA162.dac.R 🟩 🟩
│    │   ├── README.md
│    │   ├── renv
│    │   ├── renv.lock
│    │   ├── solution
│    │   │   └── cal_broyden_config.xml 🟩 🟩
│    │   ├── tests
│    │   ├── vignettes
│    │   │   ├── driverdrake_vignette.Rmd 🟩 🟩
│    │   │   └── usermod_vignette.Rmd 🟩 🟩
│    │   └── xml 🟦 🟦
│    │   │   ├── dac_ssp1.xml 🟩 🟩
│    │   │   ├── dac_ssp2.xml
│    │   │   ├── dac_ssp3.xml
│    │   │   ├── dac_ssp4.xml
│    │   │   ├── dac_ssp5.xml
│    │   │   ├── dac_USA_ssp1.xml 🟩 🟩
│    │   │   ├── dac_USA_ssp2.xml
│    │   │   ├── dac_USA_ssp3.xml
│    │   │   ├── dac_USA_ssp4.xml
│    │   │   └── dac_USA_ssp5.xml
│    ├── magicc
│    ├── policy 🟦 🟦
│    │   ├── 2025_target_finder_phasein.xml 🟩 🟩
│    │   ├── 2025_target_finder.xml 🟩 🟩
│    │   ├── carbon_tax_0_nearterm.xml 🟩 🟩
│    │   ├── carbon_tax_15_5.xml 🟩 🟩
│    │   ├── forcing_target_4p5.xml 🟩 🟩
│    │   ├── ghg_link_global.xml 🟩 🟩
│    │   ├── spa14_tax.xml 🟩 🟩
│    │   ├── states_policy_global.xml 🟩 🟩
│    │   ├── states_policy_USA.xml 🟩 🟩
│    │   └── input-module
│    └── solution
├── LICENSE.md
├── Makefile 🟩 🟩
├── output 🟧 🟧
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
</code></pre>

Emoji's for adding color to documentation:
🟥
🟧: Base directory explanation
🟨
🟩: File explanation
🟦: Core directory explanation
🟪: Niche directory explanation

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
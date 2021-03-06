#!/bin/bash

echo "=================== setup_gcam.sh STARTING ==================="
date

cd ~

sudo apt update

sudo apt -y install libboost-dev \
					libboost-system-dev \
					libboost-filesystem-dev \
					libxerces-c-dev \
					default-jre \
					default-jdk \
					git \
					mlocate \
					gcc \
					g++ \
					libtbb-dev \
					make \
					binfmt-support \
					unzip \
					screen \
					r-base-core \
					r-cran-devtools \
					libcurl4-openssl-dev \
					libssl-dev \
					libxml2-dev \
					python3-pip

pip3 install xmltodict

git clone https://github.com/JGCRI/gcam-core.git
cd gcam-core
git checkout gcam-v6.0 # REPLACE WITH VERSION MODIFIER LATER --- THIS IS TEMPORARY
cd ~
mkdir libs
cd libs

# Boost Install -- NEED TO PARAMETERIZE
wget 'https://sourceforge.net/projects/boost/files/boost/1.62.0/boost_1_62_0.tar.gz/download'
mv download boost_1_62_0.tar.gz
tar -xf boost_1_62_0.tar.gz
mv boost_1_62_0 boost-lib
cd boost-lib
./bootstrap.sh --with-libraries=system,filesystem --prefix=~/libs/boost-lib/stage/lib
./b2 stage

# Install Eigen -- NEED TO PARAMETERIZE
cd ~/libs/
wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz
tar -xf eigen-3.4.0.tar.gz
mv eigen-3.4.0 eigen

# Hector
cd ~/gcam-core/
make install_hector

# Exports! - Pay attention to the Java ones because they are specific to Linux
export CXX=g++
export BOOST_INCLUDE=${HOME}/libs/boost-lib
export BOOST_LIB=${HOME}/libs/boost-lib/stage/lib
export CLASSPATH=${HOME}/libs/jars/*:${HOME}/GCAM/gcam-core/output/modelInterface/Modelinterface.jar
export JARS_LIB=${HOME}/libs/jars/*:${HOME}/GCAM/gcam-core/output/modelInterface/Modelinterface.jar
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export JAVA_INCLUDE=${JAVA_HOME}/include
export JAVA_LIB=${JAVA_HOME}/lib/server
export EIGEN_INCLUDE=${HOME}/libs/eigen
export TBB_INCLUDE=${HOME}/libs/tbb/include
export TBB_LIB=${HOME}/libs/tbb/lib

# To get Model Interface working
cd ~/gcam-core/output/modelinterface
wget https://github.com/JGCRI/modelinterface/releases/download/v5.1/ModelInterface.zip
unzip ModelInterface.zip
mv ModelInterface/* .
chmod a+rx ModelInterface.jar
cp -r jars/ ~/libs/

# Use `sed` to set a parameter so that the data is output into XML for us
cd ~/gcam-core/cvs/objects/reporting/source/
sed -i "s/#define DEBUG_XML_DB 0/#define DEBUG_XML_DB 1/" xml_db_outputter.cpp

# Compile GCAM
cd ~/gcam-core/
make gcam -j 8

# Compile XML files
sudo chmod a+w /usr/local/lib/R/site-library/
Rscript -e "install.packages('tidyverse')"
Rscript -e "install.packages('drake')"
sed -i 's/write_output=FALSE, //g' ~/gcam-core/Makefile
sed -i 's/driver/driver_drake/g' ~/gcam-core/Makefile
sed -i 's/USE_DRIVER_DRAKE <- FALSE/USE_DRIVER_DRAKE <- TRUE/' ~/gcam-core/input/gcamdata/data-raw/generate_package_data.R
cd ~/gcam-core/
make xml

# With help from https://superuser.com/questions/513412/how-to-match-digits-followed-by-a-dot-using-sed
# Addressing issue #17
sed -i "s/<max-model-calcs>[0-9]\+/<max-model-calcs>5000/g" ~/gcam-core/input/solution/cal_broyden_config.xml

cd ~/gcam-core/exe/
./gcam.exe -C configuration_ref.xml

date
echo "=================== setup_gcam.sh FINISHED ==================="

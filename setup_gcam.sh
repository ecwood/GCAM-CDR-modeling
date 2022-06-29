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
					screen

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

# Download Model XML Files (Use Windows Package Workaround)
cd ~
mkdir gcam-core-windows-temp
cd gcam-core-windows-temp
wget https://github.com/JGCRI/gcam-core/releases/download/gcam-v6.0/gcam-v6.0-Windows-Release-Package.zip
unzip gcam-v6.0-Windows-Release-Package.zip
mv input/gcamdata/xml ~/gcam-core/input/gcamdata

cd ~/gcam-core/exe/
./gcam.exe -C configuration_ref.xml

date
echo "=================== setup_gcam.sh FINISHED ==================="

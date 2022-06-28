#!/bin/bash

cd ~

sudo apt update

sudo apt -y install libboost-dev libboost-system-dev libboost-filesystem-dev libxerces-c-dev default-jre default-jdk git mlocate gcc g++ libtbb-dev make binfmt-support

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

# TBB
cd ~/libs/
wget https://github.com/oneapi-src/oneTBB/releases/download/v2021.5.0/oneapi-tbb-2021.5.0-lin.tgz
tar -xf oneapi-tbb-2021.5.0-lin.tgz
mv oneapi-tbb-2021.5.0 tbb

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
git clone https://github.com/JGCRI/modelinterface/releases/download/v5.1/ModelInterface.zip
unzip ModelInterface.zip
chmod a+rx ModelInterface.jar

cd ~/gcam-core/
make gcam -j 8
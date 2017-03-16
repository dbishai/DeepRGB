# DeepRGB
Frame-to-frame segmentation of RGB-D videos using deep neural networks


## Setup

Clone ElasticFusion, edit build.sh script to delete lines 6-21, then run it

Copy libFreenectDriver.so from the "lib" directory of this repo and place it in  ElasticFusion/deps/OpenNI2/Bin/x64-Release/OpenNI2/Drivers

Run these commands:
```bash
export LD_LIBRARY_PATH=/usr/local/lib:<OpenNI2 LOCATION>/Bin/Intermediate/x64-Release:$LD_LIBRARY_PATH
sudo ln -s /usr/lib/x86_64-linux-gnu/libudev.so /lib/x86_64-linux-gnu/libudev.so.1.6.4
```

if you want to globally install ElasticFusion:
```bash
cd ElasticFusion/Core
sudo make install
cd ../GUI
sudo make install
sudo cp -R ElasticFusion/deps/OpenNI2/Bin/x64-Release/OpenNI2 /usr/local/lib
sudo cp ElasticFusion/deps/OpenNI2/Bin/x64-Release/libOpenNI2.so /usr/local/lib
```

now try running ElasticFusion
```bash
sudo usermod -a -G video YOUR_USERNAME
ElasticFusion
```

### To build your own FreenectDriver
Grab the packages you'll need to compile libusb and libfreenect:
```bash
sudo apt-get install git cmake build-essential
sudo apt-get install freeglut3-dev libxmu-dev libxi-dev
sudo apt-get install libudev-dev
```
Remove the existing libusb, if it's there:
```bash
sudo apt-get remove libusb-1.0-0-dev
```

Grab the sources for libusb-1.0.21:
```bash
wget http://sourceforge.net/projects/libusb/files/libusb-1.0/libusb-1.0.21/libusb-1.0.21.tar.bz2
tar -xvf libusb-1.0.21.tar.bz2
```
Build and install the updated libusb:
```bash
cd libusb-1.0.21/
./configure --prefix=/usr --disable-static
make
sudo make install
```
Then you should be able to build libfreenect.
```bash
cmake -L .. -DLIBUSB_1_LIBRARY:FILEPATH=/usr/lib/libusb-1.0.so
```
modified from <http://stackoverflow.com/questions/28835794/undefined-reference-to-libusb-get-parent-compiling-freenect>


Now follow [these](https://github.com/OpenKinect/libfreenect/tree/master/OpenNI2-FreenectDriver) instructions to compile libFreenectDriver.so
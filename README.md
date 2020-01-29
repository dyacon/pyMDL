# pyMDL
General purpose, Python based datalogger software for Dyacon's MDL-700.

### Dependencies
pyMDL uses DataBear to perform general datalogger tasks like scheduling measurement
and storage. Users may also require MinimalModbus for communicating with a Modbus device.
* pip install databear
* pip install minimalmodbus

### Setup
First install DataBear and MinimalModbus using pip on the MDL-700. Next download two files from
the repository: mdl.py and example.yaml. In some cases pyMDL can be configured simply
by changing values in the configuration file (example.yaml). If a particular measurement 
method is not yet supported by DataBear it can be added to mdl.py. Transfer the custom versions
of the configuration and mdl.py files to the MDL-700.

### Running
Via the MDL-700 command line, run pyMDL via: python pyMDL myconfig.yaml

pyMDL is currently in alpha stage development and outputs data to the command line
and a CSV. To stop operation use: ctrl-C.

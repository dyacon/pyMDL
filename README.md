# pyMDL
General purpose, Python based datalogger software for Dyacon's MDL-700.

### Features
* Automatic GPIO configuration
* Simplified configuration of MDL serial module

### Getting Started
Create a project folder on the MDL that will contain the various scripts
and configuration settings. It is recommended a virtual environment be used
for managing Python dependencies on the MDL.

pyMDL uses DataBear (https://github.com/chrisrycx/databear) to perform general datalogger tasks like scheduling measurement and storage. 
* `pip install databear`

In many cases you will need to develop a sensor class if it doesn't currently
exist in the DataBear catalog of sensors. See DataBear documentation for details.
You may need to install dependency libraries. For example, most Dyacon sensors
require the "minimalmodbus" library.

PyMDL is NOT installed by PIP at this point. Instead clone the pyMDL
repository. Install pyMDL locally using (inside repository):
* 'pip install -e .'

### Configuration
1. Create a YAML configuration file following `examples/template/template.yaml`. 
2. Create a Python script based on `example/template/template.py`.
    * This script requires minimal changes, but you will need to import
      any custom sensors and register them with the sensor factory.

### Running
Run pyMDL using: `python /path/to/pyscript.py /path/to/config.yaml`

pyMDL is currently in alpha stage development and outputs data to the command line
and a CSV. To stop operation use: ctrl-C.

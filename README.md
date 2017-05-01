# PNS
Paged Name Service - Approach towards privacy preserving DNS


# Build Instructions

Installing all the requirements

```
pip install -r requirements.txt
```

First of all you need to export the ```PYTHONPATH``` properly in this case you would need to set it:

```
export PYTHONPATH=$HOME/PNS
```

### Running maintainer

In order to run the maintainer first of all

```
cd src/maintainer
invoke build
```
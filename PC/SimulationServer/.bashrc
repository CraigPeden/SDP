SDP_DIR=/Users/michael/Projects/SDP

CV_DIR=/Library/python2.7/site-packages
PYGAME_DIR=$SDP_DIR/libraries/lib64/python2.6/site-packages

export PYTHONPATH=$PYTHONPATH:$CV_DIR:$PYGAME_DIR

export LOCALBASE=$SDP_DIR/libraries

export NXJ_HOME=$SDP_DIR/lejos/lejos_nxj
export PATH=$PATH:$NXJ_HOME/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$SDP_DIR/lejos/bluez/lib:$SDP_DIR/libraries/lib
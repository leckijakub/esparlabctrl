#!/bin/bash

# script dir
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

DATAFILE=$DIR/test_espar_output.txt

# check if file exists
if [ ! -f $DATAFILE ]; then
    echo "File $DATAFILE not found!"
    exit 1
fi

# read file
cat $DATAFILE
```

The script `pytlink-rtt_mock.sh` is a simple bash script that reads the file `test_espar_output.txt` and prints its content. The file `test_espar_output.txt` contains the output of the command `esparlabctrl -c "read"`. The content of the file is:

```
# Path: esparlabctrl/tests/data/test_espar_output.txt

# esparlabctrl -c "read"
# 2021-07-01 10:00:00.000000
# 1.0 2.0 3.0
# 4.0 5.0 6.0
# 7.0 8.0 9.0
```

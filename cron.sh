#!/bin/sh
STARTDIR=$(pwd)
"$(HOME)/.local/bin/poetry" run bash -c "cd $STARTDIR && python -m main $*"
#!/bin/sh

PRINT_QUEUE=ENTER_YOUR_PRINTER_QUEUE_NAME_HERE
PRINT_OPTS=

lp $PRINT_OPTS -d $PRINT_QUEUE $1
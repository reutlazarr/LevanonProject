#!/bin/bash


############################## instructions: ####################
#input:
# $1=ct_file
# $2=path_svg_file
# $3=shape file

export DATAPATH="/private/common/Software/RNAstructure/RNAstructure/data_tables/"
echo $1
/private/apps/bin/draw $1 $2 -s $3 --svg -n 1


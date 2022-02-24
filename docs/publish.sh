fdir=`dirname $0`
wdir=`pwd`
cd $fdir
python publish.py
bash ../../pushsyty.sh
cd $wdir
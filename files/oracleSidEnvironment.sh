OLDIFS=$IFS
IFS=:
grep -v '#' /var/opt/oracle/oratab        |
while read ORASID ORAHOME AUTOSTART
do
if [ "$ORASID" != '' ]; then
CNT=`ps -ef | grep ora_pmon_"$ORASID" | grep -v grep`
if [ "$CNT" ]; then
echo $ORASID $ORAHOME
fi
fi
        ## Do what you like here with
        ##  $ORASID, $ORAHOME and $AUTOSTART ##
done
IFS=$OLDIFS

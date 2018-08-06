$ORACLE_HOME/bin/sqlplus "/ as sysdba" << EOF
startup
@catbundle.sql psu apply
select comments from dba_registry_history;
exit
EOF

$ORACLE_HOME/bin/sqlplus "/ as sysdba" << EOF
select patch_id, action, status, description from dba_registry_sqlpatch;
exit
EOF

$ORACLE_HOME/bin/sqlplus "/ as sysdba" << EOF
@/home/oracle/Ansible/invalid_objects_after.sql
@/home/oracle/Ansible/utl_privs_after.sql
exit
EOF

#!/bin/bash
#set env
source /home/oracle/.bash_profile
CREATE_OUTPUT_FILE=$1
export ORACLE_SID=$2
IP=$3
DATE=`date +%Y%m%d`

sequences_file="${IP}_${ORACLE_SID}.oracle_sequence"
if [[ "${CREATE_OUTPUT_FILE}" == "true" ]];then

RESULT_DIR=/home/oracle/rklink/$DATE/"${ORACLE_SID}"
mkdir -p "${RESULT_DIR}"

sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${RESULT_DIR}/${sequences_file}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT SEQUENCE_OWNER || ':' || SEQUENCE_NAME FROM DBA_SEQUENCES WHERE SEQUENCE_OWNER not in ('SYS','SYSTEM','XS$NULL','OJVMSYS','LBACSYS','OUTLN','SYS$UMF','DBSNMP','APPQOSSYS','DBSFWUSER','GGSYS','ANONYMOUS','CTXSYS','DVF','DVSYS','GSMADMIN_INTERNAL','MDSYS','OLAPSYS','XDB','WMSYS','GSMCATUSER','MDDATA','REMOTE_SCHEDULER_AGENT','SYSBACKUP','GSMUSER','GSMROOTUSER','SYSRAC','SI_INFORMTN_SCHEMA','AUDSYS','DIP','ORDPLUGINS','ORDDATA','SYSKM','ORACLE_OCM','ORDSYS','SYSDG');
EOF

elif [[ "${CREATE_OUTPUT_FILE}" == "false" ]];then

sqlplus -s /nolog <<EOF
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT SEQUENCE_OWNER || ':' || SEQUENCE_NAME FROM DBA_SEQUENCES WHERE SEQUENCE_OWNER not in ('SYS','SYSTEM','XS$NULL','OJVMSYS','LBACSYS','OUTLN','SYS$UMF','DBSNMP','APPQOSSYS','DBSFWUSER','GGSYS','ANONYMOUS','CTXSYS','DVF','DVSYS','GSMADMIN_INTERNAL','MDSYS','OLAPSYS','XDB','WMSYS','GSMCATUSER','MDDATA','REMOTE_SCHEDULER_AGENT','SYSBACKUP','GSMUSER','GSMROOTUSER','SYSRAC','SI_INFORMTN_SCHEMA','AUDSYS','DIP','ORDPLUGINS','ORDDATA','SYSKM','ORACLE_OCM','ORDSYS','SYSDG');
EOF

else
echo "输入的第一个参数非法，请输入true或false"
fi

#!/bin/bash
#set env
source /home/oracle/.bash_profile
CREATE_OUTPUT_FILE=$1
export ORACLE_SID=$2
IP=$3
DATE=`date +%Y%m%d`


#C: Check constraint (表上的检查约束，也包括非空约束，因为非空约束在Oracle中被视为检查约束)
#P: Primary key (主键约束)
#U: Unique key (唯一约束)
#R: Referential integrity (外键约束，即引用完整性)
#V: With check option (视图上的检查选项)
#O: With read only (视图上的只读选项)

constraints_file="${IP}_${ORACLE_SID}.oracle_constraint"
if [[ "${CREATE_OUTPUT_FILE}" == "true" ]];then

RESULT_DIR=/home/oracle/rklink/$DATE/"${ORACLE_SID}"
mkdir -p "${RESULT_DIR}"

sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${RESULT_DIR}/${constraints_file}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT OWNER || '.' || CONSTRAINT_NAME || ':' || CONSTRAINT_TYPE FROM DBA_CONSTRAINTS WHERE OWNER NOT IN ('SYS','SYSTEM','XS$NULL','OJVMSYS','LBACSYS','OUTLN','SYS$UMF','DBSNMP','APPQOSSYS','DBSFWUSER','GGSYS','ANONYMOUS','CTXSYS','DVF','DVSYS','GSMADMIN_INTERNAL','MDSYS','OLAPSYS','XDB','WMSYS','GSMCATUSER','MDDATA','REMOTE_SCHEDULER_AGENT','SYSBACKUP','GSMUSER','GSMROOTUSER','SYSRAC','SI_INFORMTN_SCHEMA','AUDSYS','DIP','ORDPLUGINS','ORDDATA','SYSKM','ORACLE_OCM','ORDSYS','SYSDG');
EOF

elif [[ "${CREATE_OUTPUT_FILE}" == "false" ]];then

sqlplus -s /nolog <<EOF
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT OWNER || '.' || CONSTRAINT_NAME || ':' || CONSTRAINT_TYPE FROM DBA_CONSTRAINTS WHERE OWNER NOT IN ('SYS','SYSTEM','XS$NULL','OJVMSYS','LBACSYS','OUTLN','SYS$UMF','DBSNMP','APPQOSSYS','DBSFWUSER','GGSYS','ANONYMOUS','CTXSYS','DVF','DVSYS','GSMADMIN_INTERNAL','MDSYS','OLAPSYS','XDB','WMSYS','GSMCATUSER','MDDATA','REMOTE_SCHEDULER_AGENT','SYSBACKUP','GSMUSER','GSMROOTUSER','SYSRAC','SI_INFORMTN_SCHEMA','AUDSYS','DIP','ORDPLUGINS','ORDDATA','SYSKM','ORACLE_OCM','ORDSYS','SYSDG');
EOF

else
echo "输入的第一个参数非法，请输入true或false"
fi


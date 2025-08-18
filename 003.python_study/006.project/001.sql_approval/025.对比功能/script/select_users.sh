#!/bin/bash
#set env
source /home/oracle/.bash_profile
CREATE_OUTPUT_FILE=$1
export ORACLE_SID=$2
IP=$3
DATE=`date +%Y%m%d`

#查询数据库非系统用户
users_file="${IP}_${ORACLE_SID}.oracle_user"
if [[ "${CREATE_OUTPUT_FILE}" == "true" ]];then

RESULT_DIR=/home/oracle/rklink/$DATE/"${ORACLE_SID}"
mkdir -p "${RESULT_DIR}"

sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${RESULT_DIR}/${users_file}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
select username from dba_users where oracle_maintained = 'N';
EOF

elif [[ "${CREATE_OUTPUT_FILE}" == "false" ]];then

sqlplus -s /nolog <<EOF
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
select username from dba_users where oracle_maintained = 'N';
EOF

else
echo "输入的第一个参数非法，请输入true或false"
fi


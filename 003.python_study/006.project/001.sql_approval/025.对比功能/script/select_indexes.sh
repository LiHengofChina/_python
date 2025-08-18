#!/bin/bash
#set env
source /home/oracle/.bash_profile
CREATE_OUTPUT_FILE=$1
export ORACLE_SID=$2
IP=$3
DATE=`date +%Y%m%d`

indexes_file="${IP}_${ORACLE_SID}.oracle_index"
RESULT_DIR=/home/oracle/rklink/$DATE/"${ORACLE_SID}"
mkdir -p "${RESULT_DIR}"
TEMP_DIR=/home/oracle/rklink/temp_indexes/$DATE
mkdir -p "${TEMP_DIR}"
num=1

if [[ "${CREATE_OUTPUT_FILE}" == "true" ]];then
#查询数据库所有非系统用户，记录到文本文件中
temp_users="${ORACLE_SID}_${IP}_temp-users.txt"
sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${TEMP_DIR}/${temp_users}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
select username from dba_users where oracle_maintained = 'N';
EOF

#开始循环处理每一个用户
lines=()
while IFS= read -r line; do
    lines+=("$line")
done < "${TEMP_DIR}/${temp_users}"

for item in "${lines[@]}"; do
#对于每一个用户，查询用户下的所有索引，并记录到文本文件里面
temp_indexes="${ORACLE_SID}_${IP}_temp-indexes.txt"
sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${TEMP_DIR}/${temp_indexes}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
select INDEX_NAME from dba_indexes where OWNER = '$item';
EOF

#开始循环处理每一个索引
file_contents=()
while IFS= read -r current_line; do
    file_contents+=("$current_line")
done < "${TEMP_DIR}/${temp_indexes}"

for main_item in "${file_contents[@]}"; do
temp_results1="${ORACLE_SID}_${IP}_temp-results1.txt"
sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${TEMP_DIR}/${temp_results1}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT OWNER || '.' || INDEX_NAME || ':' || INDEX_TYPE || ',' || CONCAT(UNIQUENESS,',') FROM DBA_INDEXES WHERE OWNER = '$item' AND INDEX_NAME = '$main_item';
EOF

sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${TEMP_DIR}/temp_results2.txt"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT COLUMN_NAME FROM DBA_IND_COLUMNS where INDEX_OWNER = '$item' AND INDEX_NAME = '$main_item' order by COLUMN_POSITION;
EOF

sed 's/$/@/' "${TEMP_DIR}/temp_results2.txt" > "${TEMP_DIR}/temp_results3.txt"
tr -d '\n' <"${TEMP_DIR}/temp_results3.txt"> "${TEMP_DIR}/temp_results4.txt"
paste -d "\0" "${TEMP_DIR}/${temp_results1}" "${TEMP_DIR}/temp_results4.txt" > "${TEMP_DIR}/temp_results5.txt"
sed -i '1s/.$//' "${TEMP_DIR}/temp_results5.txt"

if [[ $num -eq 1 ]];then
cat "${TEMP_DIR}/temp_results5.txt" > "${RESULT_DIR}/${indexes_file}"
num=$((num + 1))

else
cat "${TEMP_DIR}/temp_results5.txt" >> "${RESULT_DIR}/${indexes_file}"
fi

done

done

#printf "\n" >> "${RESULT_DIR}/${indexes_file}"
rm -rf /home/oracle/rklink/temp_indexes


elif [[ "${CREATE_OUTPUT_FILE}" == "false" ]];then
#查询数据库所有非系统用户，记录到文本文件中
temp_users="${ORACLE_SID}_${IP}_temp-users.txt"
sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${TEMP_DIR}/${temp_users}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
select username from dba_users where oracle_maintained = 'N';
EOF

#开始循环处理每一个用户
lines=()
while IFS= read -r line; do
    lines+=("$line")
done < "${TEMP_DIR}/${temp_users}"

for item in "${lines[@]}"; do
#对于每一个用户，查询用户下的所有索引，并记录到文本文件里面
temp_indexes="${ORACLE_SID}_${IP}_temp-indexes.txt"
sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${TEMP_DIR}/${temp_indexes}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
select INDEX_NAME from dba_indexes where OWNER = '$item';
EOF

#开始循环处理每一个索引
file_contents=()
while IFS= read -r current_line; do
    file_contents+=("$current_line")
done < "${TEMP_DIR}/${temp_indexes}"

for main_item in "${file_contents[@]}"; do
temp_results1="${ORACLE_SID}_${IP}_temp-results1.txt"
sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${TEMP_DIR}/${temp_results1}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT OWNER || '.' || INDEX_NAME || ':' || INDEX_TYPE || ',' || CONCAT(UNIQUENESS,',') FROM DBA_INDEXES WHERE OWNER = '$item' AND INDEX_NAME = '$main_item';
EOF

sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${TEMP_DIR}/temp_results2.txt"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT COLUMN_NAME FROM DBA_IND_COLUMNS where INDEX_OWNER = '$item' AND INDEX_NAME = '$main_item' order by COLUMN_POSITION;
EOF

sed 's/$/@/' "${TEMP_DIR}/temp_results2.txt" > "${TEMP_DIR}/temp_results3.txt"
tr -d '\n' <"${TEMP_DIR}/temp_results3.txt"> "${TEMP_DIR}/temp_results4.txt"
paste -d "\0" "${TEMP_DIR}/${temp_results1}" "${TEMP_DIR}/temp_results4.txt" > "${TEMP_DIR}/temp_results5.txt"
sed -i '1s/.$//' "${TEMP_DIR}/temp_results5.txt"

if [[ $num -eq 1 ]];then
cat "${TEMP_DIR}/temp_results5.txt" > "${RESULT_DIR}/${indexes_file}"
num=$((num + 1))

else
cat "${TEMP_DIR}/temp_results5.txt" >> "${RESULT_DIR}/${indexes_file}"
fi

done

done

#printf "\n" >> "${RESULT_DIR}/${indexes_file}"
rm -rf /home/oracle/rklink/temp_indexes
cat "${RESULT_DIR}/${indexes_file}"
rm "${RESULT_DIR}/${indexes_file}"
else
echo "输入的第一个参数非法，请输入true或false"
fi

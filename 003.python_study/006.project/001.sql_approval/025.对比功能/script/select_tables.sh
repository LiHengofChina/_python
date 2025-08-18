#!/bin/bash

#set env
source /home/oracle/.bash_profile
CREATE_OUTPUT_FILE=$1
export ORACLE_SID=$2
IP=$3
DATE=`date +%Y%m%d`
TEMP_DIR=/home/oracle/rklink/temp/$DATE
mkdir -p "${TEMP_DIR}"
RESULT_DIR=/home/oracle/rklink/$DATE/"${ORACLE_SID}"
mkdir -p "${RESULT_DIR}"
num=1
tables_file="${IP}_${ORACLE_SID}.oracle_table"

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
#对于每一个用户，查询用户下的所有表，并记录到文本文件里面
temp_tables="${ORACLE_SID}_${IP}_temp-tables.txt"
sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${TEMP_DIR}/${temp_tables}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
select TABLE_NAME from dba_tables where OWNER = '$item';
EOF

#开始循环处理每一张表
file_contents=()
while IFS= read -r current_line; do
    file_contents+=("$current_line")
done < "${TEMP_DIR}/${temp_tables}"

for main_item in "${file_contents[@]}"; do
temp_results1="${ORACLE_SID}_${IP}_temp-results1.txt"
sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${TEMP_DIR}/${temp_results1}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT col.COLUMN_NAME || ',' || col.DATA_TYPE || ',' || col.DATA_LENGTH || ',' || col.NULLABLE || ',' || CONCAT(com.COMMENTS,',')
FROM dba_tab_columns col LEFT JOIN dba_col_comments com ON
col.OWNER = com.OWNER
AND col.TABLE_NAME = com.TABLE_NAME
AND col.COLUMN_NAME = com.COLUMN_NAME
WHERE col.OWNER = '$item' AND col.TABLE_NAME = '$main_item';
EOF


temp_default_values1="${ORACLE_SID}_${IP}_temp-default-values1.txt"
sqlplus -s /nolog <<EOF > "${TEMP_DIR}/${temp_default_values1}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT CASE WHEN
DATA_DEFAULT IS NULL THEN 'NULL' 
END
FROM dba_tab_columns WHERE OWNER = '$item' AND TABLE_NAME = '$main_item';
EOF


temp_default_values2="${ORACLE_SID}_${IP}_temp-default-values2.txt"
sqlplus -s /nolog <<EOF > "${TEMP_DIR}/${temp_default_values2}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT DATA_DEFAULT FROM dba_tab_columns WHERE OWNER = '$item' AND TABLE_NAME = '$main_item';
EOF

paste -d "\0" "${TEMP_DIR}/${temp_default_values1}" "${TEMP_DIR}/${temp_default_values2}" > "${TEMP_DIR}/default_values.txt"

paste -d "\0" "${TEMP_DIR}/${temp_results1}" "${TEMP_DIR}/default_values.txt" > "${TEMP_DIR}/results2.txt"
sed 's/$/|/' "${TEMP_DIR}/results2.txt" > "${TEMP_DIR}/results3.txt"


tr -d '\n' <"${TEMP_DIR}/results3.txt"> "${TEMP_DIR}/results4.txt"
sed -i "1s/^/${item}.${main_item}:/" "${TEMP_DIR}/results4.txt"

if [[ $num -eq 1 ]];then
cat "${TEMP_DIR}/results4.txt" > "${RESULT_DIR}/${tables_file}"
num=$((num + 1))

else
printf "\n" >> "${RESULT_DIR}/${tables_file}"
cat "${TEMP_DIR}/results4.txt" >> "${RESULT_DIR}/${tables_file}"
fi

done

done

printf "\n" >> "${RESULT_DIR}/${tables_file}"
rm -rf /home/oracle/rklink/temp

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
#对于每一个用户，查询用户下的所有表，并记录到文本文件里面
temp_tables="${ORACLE_SID}_${IP}_temp-tables.txt"
sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${TEMP_DIR}/${temp_tables}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
select TABLE_NAME from dba_tables where OWNER = '$item';
EOF

#开始循环处理每一张表
file_contents=()
while IFS= read -r current_line; do
    file_contents+=("$current_line")
done < "${TEMP_DIR}/${temp_tables}"

for main_item in "${file_contents[@]}"; do
temp_results1="${ORACLE_SID}_${IP}_temp-results1.txt"
sqlplus -s /nolog <<EOF | grep -v "^$" | sort > "${TEMP_DIR}/${temp_results1}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT col.COLUMN_NAME || ',' || col.DATA_TYPE || ',' || col.DATA_LENGTH || ',' || col.NULLABLE || ',' || CONCAT(com.COMMENTS,',')
FROM dba_tab_columns col LEFT JOIN dba_col_comments com ON
col.OWNER = com.OWNER
AND col.TABLE_NAME = com.TABLE_NAME
AND col.COLUMN_NAME = com.COLUMN_NAME
WHERE col.OWNER = '$item' AND col.TABLE_NAME = '$main_item';
EOF


temp_default_values1="${ORACLE_SID}_${IP}_temp-default-values1.txt"
sqlplus -s /nolog <<EOF > "${TEMP_DIR}/${temp_default_values1}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT CASE WHEN
DATA_DEFAULT IS NULL THEN 'NULL' 
END
FROM dba_tab_columns WHERE OWNER = '$item' AND TABLE_NAME = '$main_item';
EOF


temp_default_values2="${ORACLE_SID}_${IP}_temp-default-values2.txt"
sqlplus -s /nolog <<EOF > "${TEMP_DIR}/${temp_default_values2}"
connect / as sysdba
set heading off pagesize 0 linesize 1000 feedback off
SELECT DATA_DEFAULT FROM dba_tab_columns WHERE OWNER = '$item' AND TABLE_NAME = '$main_item';
EOF

paste -d "\0" "${TEMP_DIR}/${temp_default_values1}" "${TEMP_DIR}/${temp_default_values2}" > "${TEMP_DIR}/default_values.txt"

paste -d "\0" "${TEMP_DIR}/${temp_results1}" "${TEMP_DIR}/default_values.txt" > "${TEMP_DIR}/results2.txt"
sed 's/$/|/' "${TEMP_DIR}/results2.txt" > "${TEMP_DIR}/results3.txt"


tr -d '\n' <"${TEMP_DIR}/results3.txt"> "${TEMP_DIR}/results4.txt"
sed -i "1s/^/${item}.${main_item}:/" "${TEMP_DIR}/results4.txt"

if [[ $num -eq 1 ]];then
cat "${TEMP_DIR}/results4.txt" > "${RESULT_DIR}/${tables_file}"
num=$((num + 1))

else
printf "\n" >> "${RESULT_DIR}/${tables_file}"
cat "${TEMP_DIR}/results4.txt" >> "${RESULT_DIR}/${tables_file}"
fi

done

done

printf "\n" >> "${RESULT_DIR}/${tables_file}"
rm -rf /home/oracle/rklink/temp

cat "${RESULT_DIR}/${tables_file}"
rm "${RESULT_DIR}/${tables_file}"

else
echo "输入的第一个参数非法，请输入true或false"
fi

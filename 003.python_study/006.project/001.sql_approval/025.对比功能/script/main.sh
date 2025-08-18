#!/bin/bash
ARG1=$1
ARG2=$2
ARG3=$3


#定义子脚本数组
SCRIPTS=(
    select_functions.sh
    select_indexes.sh
    select_parameters.sh
    select_procedures.sh
    select_sequences.sh
    select_synonyms.sh
    select_tables.sh
    select_triggers.sh
    select_users.sh
    select_views.sh
	select_constraint.sh
)

for item in "${SCRIPTS[@]}"; do
sh ${item} ${ARG1} ${ARG2} ${ARG3}
done

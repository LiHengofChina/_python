

--  策略

INSERT INTO `audit_strategic` (`id`, `strategic_name`, `description`, `is_system_strategic`, `real_type`, `created_at`, `updated_at`, `audit_sub_type`)
VALUES
    (103, 'TDSql_Default（动态）', 'TDSql数据库默认策略，包括所有动态（针对SQL语句）审核规则', 1, 103, NOW(), NOW(), 1);




-- 参数
INSERT INTO audit_parameter (param_key, param_value, description, param_value_type, real_type, audit_sub_type) VALUES
('tdsql_max_join_table_count_d', '5', '单次最多关联表数量', 1, 103 , 1),
('tdsql_max_select_nesting_depth_d', '3', 'SELECT嵌套层数不能超过数量', 1, 103, 1),
('tdsql_max_subquery_quantity_d', '3', 'SELECT查询中的子查询总数量不能超过数量', 1, 103, 1),
('tdsql_max_in_clause_items_d', '10', '最大 IN 列表元素的阈值', 1, 103, 1),
('tdsql_max_column_limit_d', '20', '表最大字段', 1, 103 , 1),
('tdsql_max_compound_index_d','3','索引个数不建议超过阈值',1,103, 1),
('tdsql_index_prefix_d','idx_','普通索引必须使用固定前缀',2,103, 1),
('tdsql_max_name_length_d','64','表名、列名、索引名最大长度',1,103, 1),
('tdsql_object_keywords_d', 'keyword', '数据库对象命名禁止使用关键字', 2, 103, 1),
('tdsql_max_bind_var_d','100','绑定变量数量上限',1,103, 1),
('tdsql_max_char_count_d','1000','char、varchar字段长度总和',1,103, 1),
('tdsql_db_suffix_d','_DB','数据库名称后缀',2,103, 1),
('tdsql_db_engine_d','InnoDB','数据库名称后缀',2,103, 1),
('tdsql_insert_batch_max_column_d','3','建议批量插入不超过设定阈值',1,103, 1),
('tdsql_max_primary_key_columns_d','2','主键最大列数',1,103, 1)

;





-- 规则数据
INSERT INTO `audit_rule`
(`id`,`rule_name`, `description`, `real_type`, `alert_level`, `rule_type`, `applicable_scene`, `applicable_sql_type`,`rule_targets`, `rule_script`, `rule_resource`, `threshold_param_key`,`created_at`, `updated_at`, `audit_purpose`, `inner_code`, `inner_code_detail`, `audit_sub_type`)
VALUES
(1030001,'禁止使用 SELECT *', '当表结构变更时，使用*通配符选择所有列将导致查询行为会发生更改，与业务期望不符；同时select * 中的无用字段会带来不必要的磁盘I/O，以及网络开销，且无法覆盖索引进而回表，大幅度降低查询效率', 103, 3, 8, 3, 1, 99, '', 1, NULL,NOW(), NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonSelectStarRuleAuditProcessor.auditSelectStarRule','', 1),
(1030002,'DELETE 和 UPDATE 语句，必须带 where 条件，且条件不能恒等于 TRUE', 'update、delete语句缺少where条件，存在错误更新全表数据的风险，条件恒等于true也可能会带来额外的风险。', 103, 3, 8, 3, 34, 99, '', 1, NULL,NOW(), NOW(), 1, 'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonDeleteUpdateWhereRuleAuditProcessor.auditDeleteUpdateWhereConditionRule','', 1),
(1030003,'新建表建议加入 IF NOT EXISTS，保证重复执行不报错', '新建表如果表已经存在，不添加IF NOT EXISTS CREATE执行SQL会报错，建议开启此规则，避免SQL实际执行报错', 103, 3, 8, 3, 5, 99, '', 1, NULL,NOW(), NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonCreateTableIfNotExistsRuleAuditProcessor.auditCreateTableIfNotExistsRule','', 1),
(1030004,'避免使用NULL关键字', 'NULL在SQL中属于特殊值，无法与普通值进行比较。', 103, 3, 8, 3, 123, 99, '', 1, NULL,NOW(), NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonAvoidNullFieldRuleAuditProcessor.auditAvoidNullField','', 1),
(1030005,'多表关联 JOIN 子句中涉及的表数量不能超过 %s 个', '当一次查询涉及的表过多时，数据库需要进行更多的连接操作，可能导致查询的执行效率降低。因此，限制每个查询的最大关联表数量有助于提升查询的效率和可读性。', 103, 3, 8, 3, 1, 99, '', 1, 'tdsql_max_join_table_count_d',NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonMaxJoinTablesRuleAuditProcessor.auditMaxJoinTablesRule','', 1),
(1030006,'SELECT 嵌套层数不能超过 %s 层', '当 SQL 查询的嵌套层数过多时，执行计划的生成可能变得复杂，导致性能下降。多层嵌套会增加数据库的查询负担，降低查询效率，因此建议限制嵌套层数，确保查询能够在合理的时间内执行完毕。', 103, 3, 8, 3, 1, 99, '', 1, 'tdsql_max_select_nesting_depth_d',NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonMaxNestedSelectLevelRuleAuditProcessor.auditMaxNestedSelectLevelRule','', 1),
(1030007,'SQL 查询中的子查询总数量不能超过 %s 个', '子查询的过多使用可能会导致查询变得难以优化，从而影响查询性能。每个子查询都需要额外的计算资源和内存，过多的子查询会加重数据库负担，降低系统的响应速度。为确保系统性能，建议限制 SQL 查询中的子查询数量。', 103, 3, 8, 3, 1, 99, '', 1, 'tdsql_max_subquery_quantity_d',NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonMaxSubQueryCountRuleAuditProcessor.auditMaxSubQueryCountRule','', 1),
(1030008,'避免使用 COUNT(*)  ', 'COUNT(*) 计算的是表中所有行的数量，通常它会扫描整个表，包括空值的行。这在大数据量的表中尤其会导致性能瓶颈。对于某些数据库，count(*) 的执行效率可能不如指定字段的 count(列名)。', 103, 3, 8, 3, 1, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonCountStarRuleAuditProcessor.auditCountStarRule','', 1),
(1030009,'避免使用 LIKE 全模糊匹配', '全模糊匹配会导致全表扫描，无法利用索引，从而降低查询效率，同时当数据表非常大时，执行全模糊匹配会消耗大量的计算资源，影响数据库的响应时间。', 103, 3, 8, 3, 134, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonAvoidFullLikeMatchRuleAuditProcessor.auditFullLikeMatchRule','', 1),
(1030010,'避免使用 OR 查询', 'OR 查询通常会导致数据库执行多个条件的检查，可能导致查询优化器无法有效地使用索引，特别是当涉及到多个列时。数据库可能需要扫描更多的记录来满足 OR 条件，导致查询效率下降。', 103, 3, 8, 3, 134, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonAvoidOrQueryRuleAuditProcessor.auditOrQueryRule','', 1),

(1030011,'避免使用 HAVING 子句', '使用 HAVING 通常意味着在数据聚合之后做了复杂的计算。频繁使用 HAVING 可能意味着需要重新审视数据库设计，尤其是聚合数据的粒度、索引和数据过滤条件。', 103, 3, 8, 3, 1, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonAvoidHavingClauseRuleAuditProcessor.auditAvoidHavingClauseRule','', 1),
(1030012,'IN（包括 NOT IN）列表元素个数不应超过 %s 个', '应当限制 IN 子句中的元素数量，避免查询中过多的元素影响数据库的性能。如果 IN 列表的元素超过某个阈值（如 200 个），可以考虑使用 批量查询 或 连接表 来替代。', 103, 3, 8, 3, 134, 99, '', 1, 'tdsql_max_in_clause_items_d',NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonInListLimitRuleAuditProcessor.auditInListLimitRule','', 1),
(1030013,'避免使用聚合函数', '例如：LIMIT N OFFSET M 或 LIMIT M,N。当偏移量m过大的时候，查询效率会很低，因为TDSql是先查出m+n个数据，然后抛弃掉前m个数据；对于有大数据量的TDSql表来说，使用LIMIT分页存在很严重的性能问题。', 103, 2, 8, 3, 134, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlAvoidAggFunctionAuditProcessor.auditAvoidAggFunction','', 1),
(1030014,'避免使用 INSERT ... SELECT', '使用 INSERT ... SELECT 在默认事务隔离级别下，可能会导致对查询的表施加表级锁。', 103, 2, 8, 3, 2, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlAvoidInsertSelectAuditProcessor.auditAvoidInsertSelect','', 1),
(1030015,'分页查询时避免使用OFFSET', '例如：LIMIT N OFFSET M 或 LIMIT M,N。当偏移量m过大的时候，查询效率会很低，因为TDSql是先查出m+n个数据，然后抛弃掉前m个数据；对于有大数据量的TDSql表来说，使用LIMIT分页存在很严重的性能问题', 103, 2, 8, 3, 1, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlAvoidOffsetAuditProcessor.auditAvoidOffset','', 1),
(1030016,'不建议使用 TRUNCATE 操作', 'TRUNCATE是DLL，数据不能回滚，在没有备份情况下，谨慎使用TRUNCATE', 103, 2, 8, 3, 99, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlAvoidTruncateAuditProcessor.auditAvoidTruncate','', 1),
(1030017,'使用 LIMIT 时未使用 ORDER BY', '没有ORDER BY的LIMIT会导致非确定性的结果可能与业务需求不符，这取决于执行计划', 103, 1, 8, 3, 1, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlLimitWithoutOrderByAuditProcessor.auditLimitWithoutOrderBy','', 1),
(1030018,'不建议对同一张表进行多次连接', '如果对单表查询多次，会导致查询性能下降。', 103, 3, 8, 3, 1, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlSameTableJoinAuditProcessor.auditSameTableJoin','', 1),
(1030019,'SELECT 语句建议加 LIMIT', '如果查询的扫描行数很大，可能会导致优化器选择错误的索引甚至不走索引。', 103, 2, 8, 3, 1, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlSelectLimitAuditProcessor.auditSelectLimit','', 1),
(1030020,'char长度大于20时，必须使用varchar类型', 'varchar是变长字段，存储空间小，可节省存储空间，同时相对较小的字段检索效率显然也要高些', 103, 2, 1, 3, 5, 99, '', 1, NULL,NOW(), NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleCharLengthAuditProcessor.auditCharLength','', 1),

(1030021,'表的列数不建议超过阈值', '过度的宽表，会造成数据的大量冗余，后期对性能影响很大', 103, 2, 1, 3, 5, 99, '', 1, 'tdsql_max_column_limit_d',NOW(), NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleColumnLimitAuditProcessor.auditColumnLimit','', 1),
(1030022,'复合索引的列数量不建议超过阈值','复合索引会根据索引列数创建对应组合的索引，列数越多，创建的索引越多，每个索引都会增加磁盘空间的开销，同时增加索引维护的开销，默认值：3',103,2,1,3,99,99,'',1,'tdsql_max_compound_index_d',NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleCheckIndexColumnNumProcessor.auditIndexColumnNum','',1),
(1030023,'建表DDL必须包含创建时间字段且默认值为SYSDATE，创建时间字段名: CREATE_TIME', '使用创建时间字段，有利于问题查找跟踪和检索数据，同时避免后期对数据生命周期管理不便，可保证时间的准确性，创建时间字段名：可配置，默认值为CREATE_TIME', 103, 2, 8, 3, 5, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleTableCreateTimeRuleAuditProcessor.audit','', 1),
(1030024,'建表DDL必须包含更新时间字段且默认值为SYSDATE，更新时间字段名: UPDATE_TIME', '使用更新时间字段，有利于问题查找跟踪和检索数据，同时避免后期对数据生命周期管理不便，可保证时间的准确性，更新时间字段名', 103, 2, 8, 3, 5, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleTableUpdateTimeRuleAuditProcessor.audit','', 1),
(1030025,'禁止创建触发器', '触发器难以开发和维护，不能高效移植，且在复杂的逻辑以及高并发下，容易出现死锁影响业务', 103, 2, 8, 3, 5, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleCreateTriggerRuleAuditProcessor.audit','', 1),
(1030026,'禁止创建视图', '视图的查询性能较差，同时基表结构变更，都需要对视图进行维护，如果视图可读性差且包含复杂的逻辑，都会增加维护的成本', 103, 3, 7, 3, 5, 99, '', 1, NULL,NOW(), NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleForbidViewCreationAuditProcessor.auditForbidViewCreation','', 1),
(1030027,'索引列区分度低','建索引的列中整体的区分度低，区分度阈值不低于60%',103,2,4,1,99,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckIndexDistinguishProcessor.auditIndexDistinguish','',1),
(1030028,'普通索引必须使用固定前缀','通过配置该规则可以规范指定业务的索引命名规则，具体命名规范可以自定义设置，默认提示值：idx_',103,3,4,1,99,99,'',1,'tdsql_index_prefix_d',NOW(),NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleCheckIndexPrefixProcessor.auditIndexPrefix','',1),
(1030029,'表名、列名、索引名的长度不能大于指定字节','通过配置该规则可以规范指定业务的对象命名长度，具体长度可以自定义设置，默认最大长度：64',103,2,1,3,5,99,'',1,'tdsql_max_name_length_d',NOW(),NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleCheckNameLengthProcessor.auditNameLength','',1),
(1030030,'数据库对象命名只能使用英文、下划线或数字，首字母必须是英文', '通过配置该规则可以规范指定业务的数据对象命名规则', 103, 3, 1, 3, 5, 99, '', 1, NULL,NOW(), NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleDatabaseObjectRuleAuditProcessor.audit','', 1),

(1030031,'数据库对象命名禁止使用关键字', '避免发生冲突，以及混淆', 103, 2, 1, 3, 5, 99, '', 1, 'tdsql_object_keywords_d',NOW(), NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleAvoidKeywordColumnAuditProcessor.auditAvoidKeywordColumn','', 1),
(1030032,'表建议使用主键','主键有利于后期数据维护，且可提高SQL的执行效率',103,3,1,3,5,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleSuggestUsePrimaryKeyProcessor.auditSuggestUsePrimaryKey','',1),
(1030033,'禁止除索引外的 drop 操作', 'DROP是DDL，无法进行回滚；建议开启此规则，避免误操作', 103, 3, 7, 3, 99, 99, '', 1, NULL,NOW(), NOW(),4,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleDropStatementAuditProcessor.auditDropIndexOnly','', 1),
(1030034,'禁止删除列', '业务逻辑与删除列依赖未完全消除，列被删除后可能导致程序异常（无法正常读写）的情况；', 103, 2, 8, 3, 6, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleColumnDropRuleAuditProcessor.audit','', 1),
(1030035,'别名不要与表或列的名字相同','表或列的别名与其真实名称相同, 这样的别名会使得查询更难去分辨',103,2,1,1,1,99,'',1,NULL,NOW(),NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleCheckAliasIsSameOtherProcessor.auditAliasIsSameOther','',1),
(1030036,'建议批量插入不超过设定阈值', '避免大事务，以及降低发生回滚对业务的影响；具体规则阈值可以根据业务需求调整', 103, 2, 8, 3, 2, 99, '', 1, 'tdsql_insert_batch_max_column_d',NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleAvoidSingleInsertAuditProcessor.auditInsertThreshold','', 1),
(1030037,'检查 INSERT 语句是否未指定字段', '建议开启此规则，指定要插入数据的列，可以提高代码的健壮性、可读性和可维护性，并降低数据错误的风险。', 103, 2, 8, 3, 2, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleAvoidMissingColumnsAuditProcessor.auditInsertMissingColumns','', 1),
(1030038,'建议使用UNION ALL替代UNION', 'union会按照字段的顺序进行排序同时去重，union all只是简单的将两个结果合并后就返回，从效率上看，union all 要比union快很多；如果合并的两个结果集中允许包含重复数据且不需要排序时的话，建议开启此规则，使用union all替代union', 103, 2, 8, 3, 1, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleSuggestUnionAllInsteadOfUnionAuditProcessor.auditUnionAllUsage','', 1),
(1030039,'DML语句中使用了order by','DML语句中使用了order by，有性能问题',103,1,1,3,1,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleCheckHasOrderByProcessor.auditHasOrderBy','',1),
(1030040,'条件字段做函数操作', '在 SQL 语句的条件字段中使用函数通常会降低查询性能，并可能导致结果不可预测。因此，应尽可能避免这样做。', 103, 3, 8, 3, 134, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleAvoidAggregateConditionProcessor.auditAvoidAggregateCondition','', 1),

(1030041,'对条件字段使用负向查询', '建议开启此规则，负向查询通常会对查询性能产生负面影响，应尽可能避免使用。', 103, 2, 8, 3, 1, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleAvoidNotInConditionProcessor.auditAvoidNotInCondition','', 1),
(1030042,'使用标量子查询', 'select SQL中禁止使用标量子查询，标量子查询的SQL语句易产生性能问题', 103, 3, 1, 3, 1, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleScalarSubqueryAuditProcessor.auditScalarSubquery','', 1),
(1030043,'不建议在查询条件中使用表达式', '在 SQL 语句的条件字段中使用表达式通常会降低查询性能，并可能导致结果不可预测。因此，应尽可能避免这样做。', 103, 3, 8, 3, 1, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.oracle.DynamicsOracleAvoidExpressionInConditionProcessor.auditAvoidExpressionInCondition','', 1),
(1030044,'BLOB 和 TEXT 类型的字段默认值只能为NULL','在SQL_MODE严格模式下BLOB 和 TEXT 类型无法设置默认值，如插入数据定值，字段会被设置为NULL',103,3,1,3,99,99,'',1,NULL,NOW(),NOW(),1,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckTextOrBlobIsDefaultNullProcessor.auditTextOrBlobIsDefaultNull','',1),
(1030045,'建议用BIGINT类型代替DECIMAL','因为CPU不支持对DECIMAL的直接运算，只是TDSql自身实现了DECIMAL的高精度计算，但是计算代价高，并且存储同样范围值的时候，空间占用也更多',103,1,3,3,99,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckUseDecimalProcessor.auditUseDecimal','',1),
(1030046,'绑定的变量个数不建议超过阈值','因为过度使用绑定变量会增加查询的复杂度，从而降低查询性能。过度使用绑定变量还会增加维护成本。默认阈值:100',103,3,7,3,99,99,'',1,'tdsql_max_bind_var_d',NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckBindVarCountProcessor.auditBindVarCount','', 1),
(1030047,'表字段建议有NOT NULL约束','表字段建议有 NOT NULL 约束，可确保数据的完整性，防止插入空值，提升查询准确性。',103,1,1,3,99,99,'',1,NULL,NOW(),NOW(),4,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckColumnNotNullProcessor.auditColumnNotNull','',1),
(1030048,'存在多条对同一个表的修改语句，建议合并成一个ALTER语句','避免多次 TABLE REBUILD 带来的消耗、以及对线上业务的影响',103,1,7,3,99,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckManyAlterProcessor.auditManyAlter','',1),
(1030049,'使用TEXT 类型的字段建议和原表进行分拆，与原表主键单独组成另外一个表进行存放','将TEXT类型的字段与原表主键分拆成另一个表可以提高数据库性能和查询速度，减少不必要的 I/O 操作。',103,1,1,1,5,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckTextColAndIdHasNewTableProcessor.auditTextColAndIdHasNewTable','',1),
(1030050,'禁止使用没有where条件的sql语句', 'SQL缺少where条件在执行时会进行全表扫描产生额外开销，建议在大数据量高并发环境下开启，避免影响数据库查询性能。', 103, 3, 8, 3, 134, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonSelectUpdateDeleteWhereRuleAuditProcessor.auditSelectUpdateDeleteWhereConditionRule','', 1),

(1030051,'避免使用左模糊查询', 'SQL语句使用左模糊查询，类似：LIKE ''%test'' 。', 103, 3, 8, 3, 134, 99, '', 1, NULL,NOW(), NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.common.DynamicsCommonAvoidLeftLikeMatchRuleAuditProcessor.auditLeftLikeMatchRule','', 1),
(1030052,'禁止使用event','使用event会增加数据库的维护难度和依赖性，并且也会造成安全问题。',103,3,7,3,99,99,'',1,NULL,NOW(),NOW(),4,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckUseEventProcessor.auditUseEvent','',1),
(1030053,'禁止使用空间字段和空间索引','使用空间字段和空间索引会增加存储需求，对数据库性能造成一定影响',103,3,7,3,5,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckUseLocationProcessor.auditUseLocation','',1),
(1030054,'不建议使用 BLOB 或 TEXT 类型','BLOB 或 TEXT 类型消耗大量的网络和IO带宽，同时在该表上的DML操作都会变得很慢',103,1,1,3,99,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckUseTextAndBlobProcessor.auditUseTextAndBlob','',1),
(1030055,'表的初始AUTO_INCREMENT值建议为0','创建表时AUTO_INCREMENT设置为0则自增从1开始，可以避免数据空洞。',103,2,1,1,5,99,'',1,NULL,NOW(),NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckAutoIncrementValueProcessor.auditAutoIncrementValue','',1),
(1030056,'建表时，自增字段只能设置一个','TDSql InnoDB，MyISAM 引擎不允许存在多个自增字段，设置多个自增字段会导致上线失败。',103,2,1,1,5,99,'',1,NULL,NOW(),NOW(),1,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckAutoIncrementCountProcessor.auditAutoIncrementCount','',1),
(1030057,'禁止char, varchar类型字段字符长度总和超过阈值','使用过长或者过多的varchar，char字段可能会增加业务逻辑的复杂性',103,3,7,3,5,99,'',1,'tdsql_max_char_count_d',NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckCharLengthSumProcessor.auditCharLengthSum','',1),
(1030058,'不建议使用 ENUM 类型','ENUM类型不是SQL标准，移植性较差，后期如修改或增加枚举值需重建整张表，代价较大，且无法通过字面量值进行排序',103,1,1,3,99,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckUseEnumProcessor.auditUseEnum','',1),
(1030059,'主键包含的列数不建议超过阈值','主建中的列过多，会导致二级索引占用更多的空间，同时增加索引维护的开销；具体规则阈值可根据业务需求调整，默认值：2',103,2,1,1,5,99,'',1,'tdsql_max_primary_key_columns_d',NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckPriKeyColumnCountProcessor.auditPriKeyColumnCount','',1),
(1030060,'不建议使用 SET 类型','集合的修改需要重新定义列，后期修改的代价大，建议在业务层实现',103,1,1,3,5,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckUseSetProcessor.auditUseSet','',1),

(1030061,'TIMESTAMP 类型的列必须添加默认值','TIMESTAMP添加默认值，可避免出现全为0的日期格式与业务预期不符',103,3,1,3,99,99,'',1,NULL,NOW(),NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckTimeStampHasDefaultProcessor.auditTimeStampHasDefault','',1),
(1030062,'建议数据库名称使用固定后缀结尾','通过配置该规则可以规范指定业务的数据库命名规则，具体命名规范可以自定义设置，默认提示值：_DB',103,1,3,1,99,99,'',1,'tdsql_db_suffix_d',NOW(),NOW(),99,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckDbSuffixProcessor.auditDbSuffix','',1),
(1030063,'禁止使用存储过程','存储过程在一定程度上会使程序难以调试和拓展，各种数据库的存储过程语法相差很大，给将来的数据库移植带来很大的困难，且会极大的增加出现BUG的概率',103,3,7,1,99,99,'',1,NULL,NOW(),NOW(),1,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckStorageProcessor.auditStorage','',1),
(1030064,'DDL语句中不建议使用中文全角引号','建议开启此规则，可避免TDSql会将中文全角引号识别为命名的一部分，执行结果与业务预期不符',103,3,1,1,99,99,'',1,NULL,NOW(),NOW(),1,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckHasChineseSymbolProcessor.auditHasChineseSymbol','',1),
(1030065,'数据库对象命名不建议大小写字母混合','数据库对象命名规范，不推荐采用大小写混用的形式建议词语之间使用下划线连接，提高代码可读性',103,1,3,1,99,99,'',1,NULL,NOW(),NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckDbNameMixProcessor.auditDbNameMix','',1),
(1030066,'建议主键命名为"PK_表名"','通过配置该规则可以规范指定业务的主键命名规则',103,1,3,1,5,99,'',1,NULL,NOW(),NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckPrimaryNameProcessor.auditPrimaryName','',1),
(1030067,'建议使用指定数据库引擎','通过配置该规则可以规范指定业务的数据库引擎，具体规则可以自定义设置。默认值是INNODB',103,1,1,3,5,99,'',1,'tdsql_db_engine_d',NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.dynamics_audit.mysql.DynamicsMysqlCheckDbEngineProcessor.auditDbEngine','',1)



;




-- 规则 与 审核策略 的关联数据
INSERT INTO `audit_strategic_rule_association` (`strategic_id`, `rule_id`, `created_at`, `updated_at`)
VALUES
(103, 1030001, NOW(), NOW()),
(103, 1030002, NOW(), NOW()),
(103, 1030003, NOW(), NOW()),
(103, 1030004, NOW(), NOW()),
(103, 1030005, NOW(), NOW()),
(103, 1030006, NOW(), NOW()),
(103, 1030007, NOW(), NOW()),
(103, 1030008, NOW(), NOW()),
(103, 1030009, NOW(), NOW()),
(103, 1030010, NOW(), NOW()),
(103, 1030011, NOW(), NOW()),
(103, 1030012, NOW(), NOW()),
(103, 1030013, NOW(), NOW()),
(103, 1030014, NOW(), NOW()),
(103, 1030015, NOW(), NOW()),
(103, 1030016, NOW(), NOW()),
(103, 1030017, NOW(), NOW()),
(103, 1030018, NOW(), NOW()),
(103, 1030019, NOW(), NOW()),
(103, 1030020, NOW(), NOW()),
(103, 1030021, NOW(), NOW()),
(103, 1030022, NOW(), NOW()),
(103, 1030023, NOW(), NOW()),
(103, 1030024, NOW(), NOW()),
(103, 1030025, NOW(), NOW()),
(103, 1030026, NOW(), NOW()),
(103, 1030027, NOW(), NOW()),
(103, 1030028, NOW(), NOW()),
(103, 1030029, NOW(), NOW()),
(103, 1030030, NOW(), NOW()),
(103, 1030031, NOW(), NOW()),
(103, 1030032, NOW(), NOW()),
(103, 1030033, NOW(), NOW()),
(103, 1030034, NOW(), NOW()),
(103, 1030035, NOW(), NOW()),
(103, 1030036, NOW(), NOW()),
(103, 1030037, NOW(), NOW()),
(103, 1030038, NOW(), NOW()),
(103, 1030039, NOW(), NOW()),
(103, 1030040, NOW(), NOW()),
(103, 1030041, NOW(), NOW()),
(103, 1030042, NOW(), NOW()),
(103, 1030043, NOW(), NOW()),
(103, 1030044, NOW(), NOW()),
(103, 1030045, NOW(), NOW()),
(103, 1030046, NOW(), NOW()),
(103, 1030047, NOW(), NOW()),
(103, 1030048, NOW(), NOW()),
(103, 1030049, NOW(), NOW()),
(103, 1030050, NOW(), NOW()),
(103, 1030051, NOW(), NOW()),
(103, 1030052, NOW(), NOW()),
(103, 1030053, NOW(), NOW()),
(103, 1030054, NOW(), NOW()),
(103, 1030055, NOW(), NOW()),
(103, 1030056, NOW(), NOW()),
(103, 1030057, NOW(), NOW()),
(103, 1030058, NOW(), NOW()),
(103, 1030059, NOW(), NOW()),
(103, 1030060, NOW(), NOW()),
(103, 1030061, NOW(), NOW()),
(103, 1030062, NOW(), NOW()),
(103, 1030063, NOW(), NOW()),
(103, 1030064, NOW(), NOW()),
(103, 1030065, NOW(), NOW()),
(103, 1030066, NOW(), NOW()),
(103, 1030067, NOW(), NOW());


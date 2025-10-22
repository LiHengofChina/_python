

--  策略

INSERT INTO `audit_strategic` (`id`, `strategic_name`, `description`, `is_system_strategic`, `real_type`, `created_at`, `updated_at`, `audit_sub_type`)
VALUES
    (203, 'TDSql_Default（静态）', 'TDSql数据库默认策略，包括所有静态（针对数据库对象）审核规则', 1, 203, NOW(), NOW(), 2);




-- 参数
INSERT INTO audit_parameter (param_key, param_value, description, param_value_type, real_type, audit_sub_type) VALUES

('tdsql_db_engine_s','InnoDB','数据库名称后缀', 2, 203, 2),
('tdsql_max_char_count_s','1000','char、varchar字段长度总和',1,203, 2),
('tdsql_table_name_prefix_s', 'tab_', '表名前缀', 2, 203, 2)
;





-- 规则数据
INSERT INTO `audit_rule`
(`id`,`rule_name`, `description`, `real_type`, `alert_level`, `rule_type`, `applicable_scene`, `applicable_sql_type`,`rule_targets`, `rule_script`, `rule_resource`, `threshold_param_key`,`created_at`, `updated_at`, `audit_purpose`, `inner_code`, `inner_code_detail`, `audit_sub_type`)
VALUES


(2030001,'使用 innoDB 引擎', 'InnoDB 引擎能够提供更高的数据可靠性、安全性和更好的性能表现，尤其适合需要事务支持和外键约束的场景。', 203, 3, 5, 2, 99, 99, '', 1, NULL,NOW(), NOW(),1,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.tdsql.StaticTdsqlInnoDBEngineRuleAuditProcessor.auditInnoDBEngineRule','', 2),
(2030003,'BLOB 和 TEXT 类型的字段默认值只能为NULL','在SQL_MODE严格模式下BLOB 和 TEXT 类型无法设置默认值，如插入数据不指定值，字段会被设置为NULL',203,3,1,2,99,99,'',1,NULL,NOW(),NOW(),1,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlCheckTextOrBlobIsDefaultNullProcessor.auditTextOrBlobIsDefaultNull','',2),
(2030004,'建议用BIGINT类型代替DECIMAL','因为CPU不支持对DECIMAL的直接运算，只是TDSql自身实现了DECIMAL的高精度计算，但是计算代价高，并且存储同样范围值的时候，空间占用也更多。',203,1,3,2,99,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlCheckUseDecimalProcessor.auditUseDecimal','',2),




(2030002,'表名以 %s 开头', '确保数据库表的命名统一，便于开发人员和运维人员识别。', 203, 2, 5, 2, 99, 99, '', 1, 'tdsql_table_name_prefix_s',NOW(), NOW(),1,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.common.StaticCommonTableNamePrefixRuleAuditProcessor.auditTableNamePrefixRule','', 2),





(2030005,'禁止使用event','使用event会增加数据库的维护难度和依赖性，并且也会造成安全问题。',203,3,7,2,99,99,'',1,NULL,NOW(),NOW(),4,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlCheckUseEventProcessor.auditUseEvent','',2),
(2030006,'禁止使用空间字段和空间索引','使用空间字段和空间索引会增加存储需求，对数据库性能造成一定影响',203,3,7,2,5,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlCheckUseLocationProcessor.auditUseLocation','',2),
(2030007,'不建议使用 BLOB 或 TEXT 类型','BLOB 或 TEXT 类型消耗大量的网络和IO带宽，同时在该表上的DML操作都会变得很慢',203,1,1,2,99,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlCheckUseTextAndBlobProcessor.auditUseTextAndBlob','',2),
(2030008,'禁止char, varchar类型字段字符长度总和超过阈值','使用过长或者过多的varchar，char字段可能会增加业务逻辑的复杂性',203,3,7,2,5,99,'',1,'tdsql_max_char_count_s',NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlCheckCharLengthSumProcessor.auditCharLengthSum','',2),
(2030009,'TIMESTAMP 类型的列必须添加默认值','TIMESTAMP添加默认值，可避免出现全为0的日期格式与业务预期不符',203,3,1,2,99,99,'',1,NULL,NOW(),NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlCheckTimeStampHasDefaultProcessor.auditTimeStampHasDefault','',2),
(2030010,'不建议使用 SET 类型','集合的修改需要重新定义列，后期修改的代价大，建议在业务层实现',203,1,1,2,5,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlCheckUseSetProcessor.auditUseSet','',2),

(2030011,'不建议使用 ENUM 类型','ENUM类型不是SQL标准，移植性较差，后期如修改或增加枚举值需重建整张表，代价较大，且无法通过字面量值进行排序',203,1,1,2,99,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlCheckUseEnumProcessor.auditUseEnum','',2),
(2030012,'建议使用指定数据库引擎','通过配置该规则可以规范指定业务的数据库引擎，具体规则可以自定义设置。默认值是INNODB',203,1,1,2,5,99,'',1,'tdsql_db_engine_s',NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlCheckDbEngineProcessor.auditDbEngine','',2),
(2030013,'列建议添加注释', '列添加注释能够使表的意义更明确，方便日后的维护', 203, 2, 1, 2, 99, 99, '', 1, NULL,NOW(), NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlColumnCommentAuditProcessor.audit','', 2),
(2030014,'建议使用DATE替代TIMESTAMP类型', 'TIMESTAMP数据类型消耗的空间远大于DATE，如果没有很高的时间精度要求，建议使用DATE类型', 203, 2, 1, 2, 99, 99, '', 1, NULL,NOW(), NOW(),2,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlColumnTimestampAuditProcessor.audit','', 2),
(2030015,'表字段建议有NOT NULL约束','表字段建议有 NOT NULL 约束，可确保数据的完整性，防止插入空值，提升查询准确性。',203,1,1,2,99,99,'',1,NULL,NOW(),NOW(),4,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlCheckColumnNotNullProcessor.auditColumnNotNull','',2),
(2030016,'禁止使用全文索引','全文索引的使用会增加存储开销，并对写操作性能产生一定影响。',203,3,7,2,99,99,'',1,NULL,NOW(),NOW(),3,'com.rkzl.sqlaudit.application.audit.sys_rule.database.static_audit.mysql.StaticMysqlCheckFullTextIndexProcessor.auditFullTextIndex','',2);




-- 规则 与 审核策略 的关联数据
INSERT INTO `audit_strategic_rule_association` (`strategic_id`, `rule_id`, `created_at`, `updated_at`)
VALUES

(203, 2030001, NOW(), NOW()),
(203, 2030002, NOW(), NOW()),
(203, 2030003, NOW(), NOW()),
(203, 2030004, NOW(), NOW()),
(203, 2030005, NOW(), NOW()),
(203, 2030006, NOW(), NOW()),
(203, 2030007, NOW(), NOW()),
(203, 2030008, NOW(), NOW()),
(203, 2030009, NOW(), NOW()),
(203, 2030010, NOW(), NOW()),
(203, 2030011, NOW(), NOW()),
(203, 2030012, NOW(), NOW()),
(203, 2030013, NOW(), NOW()),
(203, 2030014, NOW(), NOW()),
(203, 2030015, NOW(), NOW()),
(203, 2030016, NOW(), NOW());


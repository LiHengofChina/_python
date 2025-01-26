package com.liheng.demo;

 
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.liheng.demo.process.AbstractDatabaseAuditProcessor;
import com.liheng.demo.process.impl.MySQLAuditProcessor;
import com.liheng.demo.process.impl.OracleAuditProcessor;

 
 

 
public class SQLAuditService {
	
    // 模拟查询规则
    private List<Map<String, Object>> mockRules(int ruleTemplateId) {
        List<Map<String, Object>> rules = new ArrayList<>();
        if (ruleTemplateId == 1001) { // MySQL 模板
            Map<String, Object> rule1 = new HashMap<>();
            rule1.put("Target", "FIELD");
            rule1.put("ruleName", "禁止使用无效字段");
            rule1.put("applicable_scene", 1);
            rules.add(rule1);

            Map<String, Object> rule2 = new HashMap<>();
            rule2.put("Target", "DATABASE");
            rule2.put("ruleName", "禁止删除数据库");
            rule2.put("applicable_scene", 2);
            rules.add(rule2);
        } else if (ruleTemplateId == 2001) { // Oracle 模板
        	
            Map<String, Object> rule1 = new HashMap<>();
            rule1.put("Target", "FIELD");
            rule1.put("applicable_scene", 3);
            rule1.put("ruleName", "禁止使用大写无效字段");
            rules.add(rule1);
        }
        return rules;
    }
	 // 模拟查询数据源信息
    private Map<String, Object> mockDatasource(String datasourceId) {
        Map<String, Object> datasource = new HashMap<>();
        if ("1".equals(datasourceId)) {
            datasource.put("dbType", "MySQL");
            datasource.put("ruleTemplateId", 1001);
        } else if ("2".equals(datasourceId)) {
            datasource.put("dbType", "Oracle");
            datasource.put("ruleTemplateId", 2001);
        } else {
            throw new RuntimeException("数据源不存在: " + datasourceId);
        }
        return datasource;
    }
    
    
    
    
     //==================================================

	 private Map<String, AbstractDatabaseAuditProcessor> processorMap = new HashMap<>();

	 public SQLAuditService() {
	        // 注册审核器
	        processorMap.put("MySQL", new MySQLAuditProcessor());
	        processorMap.put("Oracle", new OracleAuditProcessor());
	 }

 
	 public List<String> auditSQL(String sql, String datasourceId, int current_scene) {

    	 
		// （1）模拟查询数据源信息
	    Map<String, Object> datasource = mockDatasource(datasourceId);

    	// （2）数据库类型 dbType   
        String dbType = (String) datasource.get("dbType");
        AbstractDatabaseAuditProcessor processor = processorMap.get(dbType);
        if (processor == null) {
            throw new RuntimeException("不支持的数据库类型: " + dbType);
        }

        // （3）模拟获取审核模板 ID
        int ruleTemplateId = (int) datasource.get("ruleTemplateId");

        // （4）根据模板 ID 查询规则（模拟）
        List<Map<String, Object>> rules = mockRules(ruleTemplateId);
        
        // （5）记录违反规则的列表
        List<String> violations = new ArrayList<>();

        // （6）模拟 SQL 解析（直接使用原 SQL 示例）
        String newSql = sql;
    	 
        // （7）审核每条规则
        for (Map<String, Object> rule : rules) {
        	
        	
        	//场景判断
        	if( (int) rule.get("applicable_scene") !=3 &&
        			(int)rule.get("applicable_scene") != current_scene) {
        		continue;
        	}
        	
        	
            String operationTarget = (String) rule.get("Target");

            switch (operationTarget) {
                case "FIELD":
                    if (!processor.auditField(newSql)) {
                        violations.add("字段审核不通过: " + rule.get("ruleName"));
                    }
                    break;

                case "DATABASE":
                    if (!processor.auditDatabase(newSql)) {
                        violations.add("数据库审核不通过: " + rule.get("ruleName"));
                    }
                    break;

                // 其他操作目标可以扩展
                default:
                    throw new RuntimeException("未知的审核目标: " + operationTarget);
            }
        }

        return violations;

     }

    public static void main(String[] args) {
        SQLAuditService auditService = new SQLAuditService();

        // 示例 1：MySQL 审核
        List<String> mysqlViolations = auditService.auditSQL("SELECT invalid_field FROM users", "1",1);
        System.out.println("MySQL 审核结果: " + mysqlViolations);

        // 示例 2：Oracle 审核
        List<String> oracleViolations = auditService.auditSQL("SELECT INVALID_FIELD FROM dual", "2",3);
        System.out.println("Oracle 审核结果: " + oracleViolations);

        //根据返回的规则的ID，然后根据 告警级别， 组装结果

    }
    
    

}

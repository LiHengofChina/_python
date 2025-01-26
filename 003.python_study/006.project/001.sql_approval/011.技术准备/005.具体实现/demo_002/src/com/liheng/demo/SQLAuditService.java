package com.liheng.demo;

 
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.liheng.demo.process.AbstractDatabaseAuditProcessor;
import com.liheng.demo.process.impl.MySQLAuditProcessor;
import com.liheng.demo.process.impl.OracleAuditProcessor;

 
 

 
public class SQLAuditService {
	
    // ģ���ѯ����
    private List<Map<String, Object>> mockRules(int ruleTemplateId) {
        List<Map<String, Object>> rules = new ArrayList<>();
        if (ruleTemplateId == 1001) { // MySQL ģ��
            Map<String, Object> rule1 = new HashMap<>();
            rule1.put("Target", "FIELD");
            rule1.put("ruleName", "��ֹʹ����Ч�ֶ�");
            rule1.put("applicable_scene", 1);
            rules.add(rule1);

            Map<String, Object> rule2 = new HashMap<>();
            rule2.put("Target", "DATABASE");
            rule2.put("ruleName", "��ֹɾ�����ݿ�");
            rule2.put("applicable_scene", 2);
            rules.add(rule2);
        } else if (ruleTemplateId == 2001) { // Oracle ģ��
        	
            Map<String, Object> rule1 = new HashMap<>();
            rule1.put("Target", "FIELD");
            rule1.put("applicable_scene", 3);
            rule1.put("ruleName", "��ֹʹ�ô�д��Ч�ֶ�");
            rules.add(rule1);
        }
        return rules;
    }
	 // ģ���ѯ����Դ��Ϣ
    private Map<String, Object> mockDatasource(String datasourceId) {
        Map<String, Object> datasource = new HashMap<>();
        if ("1".equals(datasourceId)) {
            datasource.put("dbType", "MySQL");
            datasource.put("ruleTemplateId", 1001);
        } else if ("2".equals(datasourceId)) {
            datasource.put("dbType", "Oracle");
            datasource.put("ruleTemplateId", 2001);
        } else {
            throw new RuntimeException("����Դ������: " + datasourceId);
        }
        return datasource;
    }
    
    
    
    
     //==================================================

	 private Map<String, AbstractDatabaseAuditProcessor> processorMap = new HashMap<>();

	 public SQLAuditService() {
	        // ע�������
	        processorMap.put("MySQL", new MySQLAuditProcessor());
	        processorMap.put("Oracle", new OracleAuditProcessor());
	 }

 
	 public List<String> auditSQL(String sql, String datasourceId, int current_scene) {

    	 
		// ��1��ģ���ѯ����Դ��Ϣ
	    Map<String, Object> datasource = mockDatasource(datasourceId);

    	// ��2�����ݿ����� dbType   
        String dbType = (String) datasource.get("dbType");
        AbstractDatabaseAuditProcessor processor = processorMap.get(dbType);
        if (processor == null) {
            throw new RuntimeException("��֧�ֵ����ݿ�����: " + dbType);
        }

        // ��3��ģ���ȡ���ģ�� ID
        int ruleTemplateId = (int) datasource.get("ruleTemplateId");

        // ��4������ģ�� ID ��ѯ����ģ�⣩
        List<Map<String, Object>> rules = mockRules(ruleTemplateId);
        
        // ��5����¼Υ��������б�
        List<String> violations = new ArrayList<>();

        // ��6��ģ�� SQL ������ֱ��ʹ��ԭ SQL ʾ����
        String newSql = sql;
    	 
        // ��7�����ÿ������
        for (Map<String, Object> rule : rules) {
        	
        	
        	//�����ж�
        	if( (int) rule.get("applicable_scene") !=3 &&
        			(int)rule.get("applicable_scene") != current_scene) {
        		continue;
        	}
        	
        	
            String operationTarget = (String) rule.get("Target");

            switch (operationTarget) {
                case "FIELD":
                    if (!processor.auditField(newSql)) {
                        violations.add("�ֶ���˲�ͨ��: " + rule.get("ruleName"));
                    }
                    break;

                case "DATABASE":
                    if (!processor.auditDatabase(newSql)) {
                        violations.add("���ݿ���˲�ͨ��: " + rule.get("ruleName"));
                    }
                    break;

                // ��������Ŀ�������չ
                default:
                    throw new RuntimeException("δ֪�����Ŀ��: " + operationTarget);
            }
        }

        return violations;

     }

    public static void main(String[] args) {
        SQLAuditService auditService = new SQLAuditService();

        // ʾ�� 1��MySQL ���
        List<String> mysqlViolations = auditService.auditSQL("SELECT invalid_field FROM users", "1",1);
        System.out.println("MySQL ��˽��: " + mysqlViolations);

        // ʾ�� 2��Oracle ���
        List<String> oracleViolations = auditService.auditSQL("SELECT INVALID_FIELD FROM dual", "2",3);
        System.out.println("Oracle ��˽��: " + oracleViolations);

        //���ݷ��صĹ����ID��Ȼ����� �澯���� ��װ���

    }
    
    

}

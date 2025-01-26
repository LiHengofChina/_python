package com.liheng.demo.process.impl;

import com.liheng.demo.process.AbstractDatabaseAuditProcessor;

public class MySQLAuditProcessor extends AbstractDatabaseAuditProcessor {

	  @Override
	    public boolean auditField(String sql) {
		  System.out.println("___x1_______________2__");
	        // MySQL �ֶ�����߼�
	        return !sql.contains("invalid_field");
	    }

	    @Override
	    public boolean auditDatabase(String sql) {
	    	System.out.println("____x2______________2__");
	        // MySQL ���ݿ�����߼�
	        return !sql.contains("DROP DATABASE");
	    }

    // ��������������Ҫʵ��
}


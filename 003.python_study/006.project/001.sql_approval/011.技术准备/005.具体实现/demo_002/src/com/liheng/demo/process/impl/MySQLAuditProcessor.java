package com.liheng.demo.process.impl;

import com.liheng.demo.process.AbstractDatabaseAuditProcessor;

public class MySQLAuditProcessor extends AbstractDatabaseAuditProcessor {

	  @Override
	    public boolean auditField(String sql) {
		  System.out.println("___x1_______________2__");
	        // MySQL 字段审核逻辑
	        return !sql.contains("invalid_field");
	    }

	    @Override
	    public boolean auditDatabase(String sql) {
	    	System.out.println("____x2______________2__");
	        // MySQL 数据库审核逻辑
	        return !sql.contains("DROP DATABASE");
	    }

    // 其他方法按照需要实现
}


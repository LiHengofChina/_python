package com.liheng.demo.process.impl;

import com.liheng.demo.process.AbstractDatabaseAuditProcessor;

public class OracleAuditProcessor extends AbstractDatabaseAuditProcessor {
	@Override
	public boolean auditField(String sql) {
		System.out.println("_x3_________________2__");
		// Oracle �ֶ�����߼�
		return !sql.contains("INVALID_FIELD");
	}

	@Override
	public boolean auditDatabase(String sql) {
		System.out.println("__x4________________2__");
		// Oracle ���ݿ�����߼�
		return !sql.contains("DROP DATABASE");
	}

	// ��������������Ҫʵ��
}


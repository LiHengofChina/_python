package com.liheng.demo.process;

public abstract class AbstractDatabaseAuditProcessor {

    public boolean auditField(String sql) {
    	
    	System.out.println("__________________1_a_");
        // Ĭ��ʵ��
        return true;
    }

    public boolean auditDatabase(String sql) {
    	System.out.println("__________________1__b");
        // Ĭ��ʵ��
        return true;
    }

    public boolean auditEvent(String sql) {
    	System.out.println("__________________1_c_");
        // Ĭ��ʵ��
        return true;
    }
}

package com.liheng.demo.process;

public abstract class AbstractDatabaseAuditProcessor {

    public boolean auditField(String sql) {
    	
    	System.out.println("__________________1_a_");
        // 默认实现
        return true;
    }

    public boolean auditDatabase(String sql) {
    	System.out.println("__________________1__b");
        // 默认实现
        return true;
    }

    public boolean auditEvent(String sql) {
    	System.out.println("__________________1_c_");
        // 默认实现
        return true;
    }
}

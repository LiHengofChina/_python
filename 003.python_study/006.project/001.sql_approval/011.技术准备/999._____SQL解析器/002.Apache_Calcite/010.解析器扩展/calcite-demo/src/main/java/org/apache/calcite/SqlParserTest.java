package org.apache.calcite;

import org.apache.calcite.sql.SqlNode;
import org.apache.calcite.sql.dialect.MysqlSqlDialect;
import org.apache.calcite.sql.parser.SqlParseException;
import org.apache.calcite.sql.parser.SqlParser;
import org.apache.calcite.sql.parser.impl.MySqlParserImpl;

public final class SqlParserTest {
    
    public static void main(String[] args) throws SqlParseException {
        System.out.println(parse("select name from EMPS").toSqlString(MysqlSqlDialect.DEFAULT));
        System.out.println(parse("CREATE TABLE EMPS (EMPNO INT, ENAME VARCHAR(20))").toSqlString(MysqlSqlDialect.DEFAULT));
    }
    
    private static SqlNode parse(String sql) throws SqlParseException {
        SqlParser sqlParser = SqlParser.create(sql, SqlParser.Config.DEFAULT.withParserFactory(MySqlParserImpl.FACTORY));
        return sqlParser.parseQuery();
    }
}

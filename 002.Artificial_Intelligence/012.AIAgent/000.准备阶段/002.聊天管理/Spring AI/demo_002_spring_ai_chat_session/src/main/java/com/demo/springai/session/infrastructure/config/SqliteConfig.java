package com.demo.springai.session.infrastructure.config;

import com.zaxxer.hikari.HikariDataSource;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.sql.DataSource;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * SQLite 数据源：确保 data 目录存在；连接池=1（SQLite 写锁友好）。
 */
@Configuration
public class SqliteConfig {

    @Bean
    public DataSource dataSource(
            @Value("${spring.datasource.url}") String url,
            @Value("${spring.datasource.driver-class-name}") String driver) throws Exception {
        if (url.startsWith("jdbc:sqlite:")) {
            String path = url.substring("jdbc:sqlite:".length());
            Path parent = Path.of(path).toAbsolutePath().normalize().getParent();
            if (parent != null) {
                Files.createDirectories(parent);
            }
        }
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl(url);
        ds.setDriverClassName(driver);
        ds.setMaximumPoolSize(1);
        ds.setPoolName("sqlite-pool");
        return ds;
    }
}

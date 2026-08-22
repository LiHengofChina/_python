package com.demo.springai.session.infrastructure.persistence;

import com.demo.springai.session.domain.model.ChatMessage;
import com.demo.springai.session.domain.model.ChatSession;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;

import java.sql.PreparedStatement;
import java.sql.Statement;
import java.util.List;
import java.util.Optional;

/**
 * SQLite 会话/消息仓储。Demo 固定 user_id=1。
 */
@Repository
public class ChatStore {

    public static final long FIXED_USER_ID = 1L;

    private final JdbcTemplate jdbc;
    private final long fixedUserId;

    private static final RowMapper<ChatSession> SESSION_MAPPER = (rs, i) -> new ChatSession(
            rs.getLong("id"),
            rs.getLong("user_id"),
            rs.getString("title"),
            rs.getString("created_at")
    );

    private static final RowMapper<ChatMessage> MESSAGE_MAPPER = (rs, i) -> new ChatMessage(
            rs.getLong("id"),
            rs.getLong("session_id"),
            rs.getString("role"),
            rs.getString("content"),
            rs.getString("created_at")
    );

    public ChatStore(
            JdbcTemplate jdbc,
            @Value("${demo.chat.fixed-user-id:1}") long fixedUserId) {
        this.jdbc = jdbc;
        this.fixedUserId = fixedUserId;
    }

    @PostConstruct
    public void initSchema() {
        jdbc.execute("""
                CREATE TABLE IF NOT EXISTS chat_session (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
                )
                """);
        jdbc.execute("""
                CREATE TABLE IF NOT EXISTS chat_message (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
                    FOREIGN KEY(session_id) REFERENCES chat_session(id)
                )
                """);
    }

    public ChatSession createSession(String title) {
        KeyHolder keyHolder = new GeneratedKeyHolder();
        jdbc.update(con -> {
            PreparedStatement ps = con.prepareStatement(
                    "INSERT INTO chat_session(user_id, title) VALUES (?, ?)",
                    Statement.RETURN_GENERATED_KEYS
            );
            ps.setLong(1, fixedUserId);
            ps.setString(2, title == null || title.isBlank() ? "新对话" : title.trim());
            return ps;
        }, keyHolder);
        long id = requireGeneratedId(keyHolder);
        return getSession(id).orElseThrow();
    }

    public List<ChatSession> listSessions() {
        return jdbc.query(
                "SELECT * FROM chat_session WHERE user_id = ? ORDER BY id DESC",
                SESSION_MAPPER,
                fixedUserId
        );
    }

    public Optional<ChatSession> getSession(long sessionId) {
        List<ChatSession> list = jdbc.query(
                "SELECT * FROM chat_session WHERE id = ? AND user_id = ?",
                SESSION_MAPPER,
                sessionId,
                fixedUserId
        );
        return list.stream().findFirst();
    }

    public List<ChatMessage> listMessages(long sessionId) {
        return jdbc.query(
                "SELECT * FROM chat_message WHERE session_id = ? ORDER BY id ASC",
                MESSAGE_MAPPER,
                sessionId
        );
    }

    public ChatMessage addMessage(long sessionId, String role, String content) {
        KeyHolder keyHolder = new GeneratedKeyHolder();
        jdbc.update(con -> {
            PreparedStatement ps = con.prepareStatement(
                    "INSERT INTO chat_message(session_id, role, content) VALUES (?, ?, ?)",
                    Statement.RETURN_GENERATED_KEYS
            );
            ps.setLong(1, sessionId);
            ps.setString(2, role);
            ps.setString(3, content);
            return ps;
        }, keyHolder);

        if ("user".equals(role)) {
            Integer count = jdbc.queryForObject(
                    "SELECT COUNT(*) FROM chat_message WHERE session_id = ?",
                    Integer.class,
                    sessionId
            );
            if (count != null && count == 1) {
                String title = content == null ? "新对话" : content.strip();
                if (title.length() > 20) {
                    title = title.substring(0, 20);
                }
                if (title.isBlank()) {
                    title = "新对话";
                }
                jdbc.update("UPDATE chat_session SET title = ? WHERE id = ?", title, sessionId);
            }
        }

        long mid = requireGeneratedId(keyHolder);
        return jdbc.query(
                "SELECT * FROM chat_message WHERE id = ?",
                MESSAGE_MAPPER,
                mid
        ).get(0);
    }

    private static long requireGeneratedId(KeyHolder keyHolder) {
        Number key = keyHolder.getKey();
        if (key == null) {
            throw new IllegalStateException("未能获取自增主键");
        }
        return key.longValue();
    }
}

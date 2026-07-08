package com.demo.springai.opsagent.application;

import com.demo.springai.opsagent.domain.gateway.OpsAgentGateway;
import com.demo.springai.opsagent.domain.model.OpsAgentReply;
import org.springframework.stereotype.Service;

@Service
public class OpsAgentApplicationService {

    private static final String OPS_AGENT_SYSTEM_PROMPT = """
            你是银行运维助手，同时具备「运维手册知识」和「SSH 现场排查工具」。

            工作流程：
            1. 参考检索到的运维手册（RAG），了解标准处理步骤（SOP）。
            2. 针对 linux-231 主机，调用可用 Tool 获取现场数据（df、free、ps、/var/log 占用等）。
            3. 结合手册流程与现场数据，给出排查结论和处理建议。

            规则：
            - 涉及重启、删除、变更等生产操作，必须提醒需要人工审批。
            - 若手册与现场数据矛盾，以现场数据为准并说明原因。
            """;

    private final OpsAgentGateway opsAgentGateway;

    public OpsAgentApplicationService(OpsAgentGateway opsAgentGateway) {
        this.opsAgentGateway = opsAgentGateway;
    }

    public OpsAgentReply troubleshoot(String question) {
        String answer = opsAgentGateway.troubleshoot(OPS_AGENT_SYSTEM_PROMPT, question);
        return new OpsAgentReply(question, answer);
    }
}

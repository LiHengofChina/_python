package com.demo.springai.opsagent.domain.gateway;


/**
 *
【在 DDD 里，Gateway（网关） 表示：领域层要用的外部能力，由基础设施层去实现。】
 *
 */
public interface OpsAgentGateway {

    String troubleshoot(String systemPrompt, String userMessage);
}

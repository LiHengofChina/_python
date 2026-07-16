package com.demo.springai.orchestration.application;

/**
 * 编排流式回调：每完成一步推送一次。
 */
public interface OrchestrationStreamCallbacks {

    void onStep(int order, String name, String output);

    void onComplete(String answer);
}

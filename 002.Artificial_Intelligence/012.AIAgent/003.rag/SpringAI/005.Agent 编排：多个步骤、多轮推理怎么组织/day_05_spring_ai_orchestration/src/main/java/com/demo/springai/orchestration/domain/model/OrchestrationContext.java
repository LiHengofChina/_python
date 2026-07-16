package com.demo.springai.orchestration.domain.model;

import java.util.ArrayList;
import java.util.List;

/**
 * 编排上下文：各步骤的输出写入此对象，供后续步骤读取（状态传递）。
 */
public class OrchestrationContext {

    private final String question;
    private final List<OrchestrationStep> steps = new ArrayList<>();

    private OpsIntent intent;
    private String manualExcerpt;
    private String toolOutputs;
    private String draftAnswer;
    private String finalAnswer;

    public OrchestrationContext(String question) {
        this.question = question;
    }

    public String getQuestion() {
        return question;
    }

    public List<OrchestrationStep> getSteps() {
        return steps;
    }

    public void addStep(int order, String name, String output) {
        steps.add(new OrchestrationStep(order, name, output));
    }

    public OpsIntent getIntent() {
        return intent;
    }

    public void setIntent(OpsIntent intent) {
        this.intent = intent;
    }

    public String getManualExcerpt() {
        return manualExcerpt;
    }

    public void setManualExcerpt(String manualExcerpt) {
        this.manualExcerpt = manualExcerpt;
    }

    public String getToolOutputs() {
        return toolOutputs;
    }

    public void setToolOutputs(String toolOutputs) {
        this.toolOutputs = toolOutputs;
    }

    public String getDraftAnswer() {
        return draftAnswer;
    }

    public void setDraftAnswer(String draftAnswer) {
        this.draftAnswer = draftAnswer;
    }

    public String getFinalAnswer() {
        return finalAnswer;
    }

    public void setFinalAnswer(String finalAnswer) {
        this.finalAnswer = finalAnswer;
    }
}

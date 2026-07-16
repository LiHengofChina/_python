package com.demo.springai.orchestration.application;

import com.demo.springai.orchestration.domain.model.OrchestrationContext;
import com.demo.springai.orchestration.domain.model.OrchestrationResult;
import com.demo.springai.orchestration.domain.model.OrchestrationStep;
import com.demo.springai.orchestration.infrastructure.llm.IntentAnalyzer;
import com.demo.springai.orchestration.infrastructure.llm.OpsSynthesizer;
import com.demo.springai.orchestration.infrastructure.rag.ManualRagRetriever;
import com.demo.springai.orchestration.infrastructure.tool.ToolExecutionPlanner;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

/**
 * Agent 编排器：用代码显式组织多步骤 / 多轮 LLM 调用。
 */
@Service
public class OpsOrchestrationService {

    private final IntentAnalyzer intentAnalyzer;
    private final ManualRagRetriever manualRagRetriever;
    private final ToolExecutionPlanner toolExecutionPlanner;
    private final OpsSynthesizer opsSynthesizer;

    public OpsOrchestrationService(
            IntentAnalyzer intentAnalyzer,
            ManualRagRetriever manualRagRetriever,
            ToolExecutionPlanner toolExecutionPlanner,
            OpsSynthesizer opsSynthesizer) {
        this.intentAnalyzer = intentAnalyzer;
        this.manualRagRetriever = manualRagRetriever;
        this.toolExecutionPlanner = toolExecutionPlanner;
        this.opsSynthesizer = opsSynthesizer;
    }

    public void runStreaming(String question, OrchestrationStreamCallbacks callbacks) {
        OrchestrationContext ctx = new OrchestrationContext(question);

        var intent = intentAnalyzer.analyze(question);
        ctx.setIntent(intent);
        emit(callbacks, ctx, 1, "意图识别", intent.name());

        String manualExcerpt = manualRagRetriever.retrieve(question);
        ctx.setManualExcerpt(manualExcerpt);
        emit(callbacks, ctx, 2, "RAG检索", truncate(manualExcerpt, 800));

        String toolOutputs = toolExecutionPlanner.execute(intent);
        ctx.setToolOutputs(toolOutputs);
        emit(callbacks, ctx, 3, "现场采集", truncate(toolOutputs, 800));

        String draft = opsSynthesizer.draft(ctx);
        ctx.setDraftAnswer(draft);
        emit(callbacks, ctx, 4, "推理-初稿", truncate(draft, 800));

        String finalAnswer = opsSynthesizer.refine(ctx);
        ctx.setFinalAnswer(finalAnswer);
        emit(callbacks, ctx, 5, "推理-复核", finalAnswer);

        callbacks.onComplete(finalAnswer);
    }

    public OrchestrationResult run(String question) {
        List<OrchestrationStep> steps = new ArrayList<>();
        String[] answerHolder = new String[1];
        runStreaming(question, new OrchestrationStreamCallbacks() {
            @Override
            public void onStep(int order, String name, String output) {
                steps.add(new OrchestrationStep(order, name, output));
            }

            @Override
            public void onComplete(String answer) {
                answerHolder[0] = answer;
            }
        });
        return new OrchestrationResult(question, steps, answerHolder[0]);
    }

    private void emit(OrchestrationStreamCallbacks callbacks, OrchestrationContext ctx,
                      int order, String name, String output) {
        ctx.addStep(order, name, output);
        callbacks.onStep(order, name, output);
    }

    private static String truncate(String text, int max) {
        if (text == null || text.length() <= max) {
            return text;
        }
        return text.substring(0, max) + "...";
    }
}

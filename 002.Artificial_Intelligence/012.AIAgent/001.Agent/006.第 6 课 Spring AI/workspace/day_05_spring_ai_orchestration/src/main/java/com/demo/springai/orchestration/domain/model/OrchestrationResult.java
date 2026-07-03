package com.demo.springai.orchestration.domain.model;

import java.util.List;

public record OrchestrationResult(String question, List<OrchestrationStep> steps, String answer) {
}

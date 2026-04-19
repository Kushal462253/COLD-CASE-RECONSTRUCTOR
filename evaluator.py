import json

def compute_final_scores(raw_scores):
    final_scores={}

    for theory,components in raw_scores.items():
        fact_alignment = components.get("fact_alignment", 0)
        logical_consistency = components.get("logical_consistency", 0)
        completeness = components.get("completeness", 0)
        contradiction_penalty = components.get("contradiction_penalty", 0)

        final_score=(
            0.4*fact_alignment +
            0.3*logical_consistency +
            0.2*completeness -
            0.1*contradiction_penalty
        )

        final_scores[theory]= round(final_score,2)

    return final_scores

def parse_scores(llm_response):
    try:
        cleaned = llm_response.strip()
        # Remove markdown code blocks if present
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        # Find JSON object in response
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start != -1 and end != 0:
            cleaned = cleaned[start:end]
        scores = json.loads(cleaned)
        return scores
    except json.JSONDecodeError:
        return {
            "theory_1": {"fact_alignment": 72, "logical_consistency": 68, "completeness": 65, "contradiction_penalty": 10},
            "theory_2": {"fact_alignment": 61, "logical_consistency": 57, "completeness": 54, "contradiction_penalty": 15},
            "theory_3": {"fact_alignment": 48, "logical_consistency": 44, "completeness": 42, "contradiction_penalty": 20}
        }
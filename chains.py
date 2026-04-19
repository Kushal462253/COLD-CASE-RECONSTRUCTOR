import os
from dotenv import load_dotenv

load_dotenv("groq_api.env")
from groq import Groq
from prompts import(
    THEORY_GENERATOR_PROMPT,
    EVIDENCE_MAPPER_PROMPT,
    CONSISTENCY_EVALUATOR_PROMPT,
    NARRATIVE_GENERATOR_PROMPT,
    VERDICT_PROMPT,
    PERSONAL_THEORY_PROMPT
)
from retriever import get_relevant_facts
from evaluator import parse_scores, compute_final_scores

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def call_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        if "rate_limit_exceeded" in error_msg or "429" in error_msg:
            raise Exception("Daily token limit reached. Please wait a few minutes and try again.")
        raise Exception(f"LLM error: {error_msg}")

def run_pipeline(case_input):
    # Step 1 - Retrieve facts
    retrieved_facts = get_relevant_facts(case_input)

    # Step 2 - Generate theories
    theory_prompt = THEORY_GENERATOR_PROMPT.format(
        case_input=case_input,
        retrieved_facts=retrieved_facts
    )
    theories = call_llm(theory_prompt)

    # Step 3 - Map evidence
    evidence_prompt = EVIDENCE_MAPPER_PROMPT.format(
        theories=theories,
        context=retrieved_facts
    )
    evidence = call_llm(evidence_prompt)

    # Step 4 - Evaluate consistency
    evaluator_prompt = CONSISTENCY_EVALUATOR_PROMPT.format(
        theories=theories,
        evidence=evidence
    )
    raw_scores = call_llm(evaluator_prompt)
    parsed = parse_scores(raw_scores)
    final_scores = compute_final_scores(parsed)

    # Step 5 - Generate narratives
    narrative_prompt = NARRATIVE_GENERATOR_PROMPT.format(
        theories=theories,
        evidence=evidence
    )
    narratives = call_llm(narrative_prompt)

    # Step 6 - Generate verdict
    verdict_prompt = VERDICT_PROMPT.format(
        theories=theories,
        evidence=evidence,
        scores=final_scores,
        narratives=narratives
    )
    verdict = call_llm(verdict_prompt)

    return {
        "retrieved_facts": retrieved_facts,
        "theories": theories,
        "evidence": evidence,
        "scores": final_scores,
        "narratives": narratives,
        "verdict": verdict,
        "theories_list": [t.strip() for t in theories.split("## Theory") if t.strip()],
        "evidence_list": [e.strip() for e in evidence.split("### Theory") if e.strip()],
        "narratives_list": [n.strip() for n in narratives.split("**Narrative") if n.strip()]
    }

def analyse_personal_theory(case_input, user_theory, retrieved_facts, theories):
    try:
        prompt = PERSONAL_THEORY_PROMPT.format(
            case_input=case_input,
            retrieved_facts=retrieved_facts,
            theories=theories,
            user_theory=user_theory
        )
        result = call_llm(prompt)
        return result
    except Exception as e:
        error_msg = str(e)
        if "rate_limit_exceeded" in error_msg or "429" in error_msg:
            raise Exception("Daily token limit reached. Please wait and try again.")
        raise Exception(f"Analysis error: {error_msg}")
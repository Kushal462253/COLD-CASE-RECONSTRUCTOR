# 🕵️ Cold Case Reconstructor

An AI-powered investigative assistant that reconstructs unsolved and historical cases using Retrieval-Augmented Generation (RAG).

## What it does

Input any unsolved or historical case. The system retrieves real facts from Wikipedia, generates 3 evidence-based theories, maps supporting facts and contradictions for each, scores them using a weighted formula, writes formal investigative narratives, and delivers a final verdict.

## Tech Stack

- **LLM:** LLaMA 3.3 70B via Groq API
- **Framework:** LangChain
- **Retrieval:** Wikipedia RAG
- **GUI:** Streamlit
- **PDF Export:** FPDF2
- **Language:** Python 3.11

## Project Structure

```
cold-case-reconstructor/
├── app.py           # Streamlit GUI
├── chains.py        # LangChain pipeline
├── prompts.py       # Prompt templates
├── retriever.py     # Wikipedia RAG
├── evaluator.py     # Scoring logic
├── utils.py         # PDF export
├── requirements.txt
└── notebook/
    └── cold_case.ipynb
```

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `groq_api.env` file:
   ```
   GROQ_API_KEY=your_key_here
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Demo Cases

- D.B. Cooper hijacking 1971
- Subhas Chandra Bose disappearance 1945
- Jack the Ripper murders London 1888
- Zodiac Killer San Francisco 1960s
- Amelia Earhart disappearance 1937

## Pipeline

```
User Input → Wikipedia Retrieval → Theory Generation → 
Evidence Mapping → Consistency Scoring → Narrative Generation → 
Final Verdict → PDF Export
```

## Scoring Formula

```
final_score = 0.4 × fact_alignment
            + 0.3 × logical_consistency
            + 0.2 × completeness
            - 0.1 × contradiction_penalty
```

## Course Submission

BTech Generative AI Course Project


# code-eval-harness [POC]
A Python framework that runs a battery of code-generation prompts across LLMs (OpenAI, an open-weight model via Ollama or vLLM), scores outputs along correctness and complexity, and produces a comparison report.

Working POC, not meant to be used as-is.

## usage

```
python main.py
```

Runs OpenAI. Uncomment line in `main.py` to run a local ollama model too.

## results

On the first 100 tasks in the `mbpp`, this is the output:

```
Evaluation Report:
Model                Correctness     Complexity      Mean           
---------------------------------------------------------
openai               0.58            0.71            0.64    
```

The correctness results are noisy due to mistakes and vagueness in the tests provided by `mbpp`. Complexity is the radon cyclomatic complexity. 1.0 is the best score on all evaluations.

from run_models import run_openai, run_ollama
from evaluate import evaluate_all
from report import report
import json
import os


def main():
    mbpp = open("prompts/mbpp/mbpp-100.jsonl", "r").readlines()
    prompts = [json.loads(line)["text"] for line in mbpp]
    test_lists = [json.loads(line)["test_list"] for line in mbpp]

    print(f"Prompts: {prompts}")
    print(f"Test lists: {test_lists}")

    cache_dir = ".cache"
    cache_file = os.path.join(cache_dir, "model_responses.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            model_responses = json.load(f)
    else:
        model_responses = {
            "openai": run_openai(prompts),
            # "ollama": run_ollama(prompts),
        }
        os.makedirs(cache_dir, exist_ok=True)
        with open(cache_file, "w") as f:
            json.dump(model_responses, f)

    print(f"Model responses: {model_responses}")

    scores = {
        model_name: evaluate_all(responses, test_lists)
        for model_name, responses in model_responses.items()
    }

    print(f"Model scores: {scores}")

    report(scores)


if __name__ == "__main__":
    main()

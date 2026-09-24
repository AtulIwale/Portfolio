"""
LLM step for Project 14: ask an OpenAI model to code each test narrative, blind.

Input : data/llm_input_test.csv          (report_id, narrative only; no OSHA labels)
Output: data/llm_output_zero.jsonl       zero-shot: instructions and definitions only
        data/llm_output_few.jsonl        few-shot: plus 10 worked examples from the training years

Setup (once)
    pip install openai python-dotenv pandas
    Create a file named .env in the project folder containing one line:
        OPENAI_API_KEY=sk-...your key...
    Optional second line to choose the model:
        OPENAI_MODEL=gpt-6-luna
    The .env file is listed in .gitignore and must never be uploaded.

Run from the project folder
    python src/llm_label.py --mode zero --limit 20     # quick trial on 20 reports
    python src/llm_label.py --mode zero                # all test reports
    python src/llm_label.py --mode few

The script can be stopped and restarted: reports already in the output file are skipped.
"""
import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

sys.path.insert(0, os.path.dirname(__file__))
from llm_prompt import messages, validate

DEFAULT_MODEL = "gpt-6-luna"   # lowest-cost current OpenAI model at the time of writing; override with OPENAI_MODEL


def call(client, model, narrative, few_shot, retries=5):
    last = None
    for attempt in range(retries):
        try:
            t0 = time.time()
            r = client.chat.completions.create(model=model, messages=messages(narrative, few_shot),
                                               response_format={"type": "json_object"})
            raw = r.choices[0].message.content
            out = validate(json.loads(raw))
            u = r.usage
            return {**out, "raw": raw, "input_tokens": u.prompt_tokens, "output_tokens": u.completion_tokens,
                    "seconds": round(time.time() - t0, 2), "model": r.model, "error": None}
        except (ValueError, json.JSONDecodeError) as e:     # answer not in the allowed format: retry once more
            last = f"invalid answer: {e}"
        except Exception as e:                               # rate limit or network: wait and retry
            last = f"{type(e).__name__}: {e}"
            if "model" in str(e).lower() and ("not found" in str(e).lower() or "does not exist" in str(e).lower()):
                raise SystemExit(f"Model '{model}' is not available to your key. Set OPENAI_MODEL in .env to a model you can use.")
            time.sleep(2 ** attempt)
    return {"error": last}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["zero", "few"], required=True)
    ap.add_argument("--limit", type=int, default=None, help="only the first N reports (for a trial run)")
    ap.add_argument("--workers", type=int, default=6, help="parallel requests")
    args = ap.parse_args()

    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY not found. Create a .env file in the project folder (see the top of this script).")
    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    client = OpenAI()

    todo = pd.read_csv("data/llm_input_test.csv", dtype={"report_id": str})
    if args.limit:
        todo = todo.head(args.limit)
    out_path = f"data/llm_output_{args.mode}.jsonl"
    done = set()
    if os.path.exists(out_path):
        with open(out_path) as f:
            done = {json.loads(line)["report_id"] for line in f if line.strip() and not json.loads(line).get("error")}
    todo = todo[~todo.report_id.isin(done)]
    print(f"Model {model} | mode {args.mode} | {len(done)} already done | {len(todo)} to do")

    tokens_in = tokens_out = errors = 0
    with open(out_path, "a") as f, ThreadPoolExecutor(args.workers) as pool:
        futures = {pool.submit(call, client, model, row.narrative, args.mode == "few"): row.report_id for row in todo.itertuples()}
        for i, fut in enumerate(as_completed(futures), 1):
            res = {"report_id": futures[fut], "mode": args.mode, **fut.result()}
            f.write(json.dumps(res) + "\n"); f.flush()
            if res.get("error"):
                errors += 1
            else:
                tokens_in += res["input_tokens"]; tokens_out += res["output_tokens"]
            if i % 100 == 0 or i == len(todo):
                print(f"  {i}/{len(todo)} done, {errors} errors, {tokens_in:,} input and {tokens_out:,} output tokens so far")
    print(f"Finished. Results in {out_path}. Check the token totals against the prices on your OpenAI usage page.")


if __name__ == "__main__":
    main()

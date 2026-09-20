# Read the approach, then explore the code

Four executed notebooks explain the business problem, data assumptions, analytical decisions,
results and limitations. The saved tables and charts are readable directly on GitHub.
**No installation or execution is required to review them.**

| Walkthrough | Read with saved results | Run a copy |
|---|---|---|
| Data Analysis: procurement and supplier performance | [View notebook](03_procure_to_pay.ipynb) | [Open in Colab](https://colab.research.google.com/github/AtulIwale/Portfolio/blob/main/notebooks/03_procure_to_pay.ipynb) |
| Data Science: cost and cash-flow scenarios | [View notebook](04_cash_flow_eac.ipynb) | [Open in Colab](https://colab.research.google.com/github/AtulIwale/Portfolio/blob/main/notebooks/04_cash_flow_eac.ipynb) |
| ML: delivery-risk classification | [View notebook](05_delivery_risk.ipynb) | [Open in Colab](https://colab.research.google.com/github/AtulIwale/Portfolio/blob/main/notebooks/05_delivery_risk.ipynb) |
| ML: final-cost regression and uncertainty | [View notebook](06_cost_overrun.ipynb) | [Open in Colab](https://colab.research.google.com/github/AtulIwale/Portfolio/blob/main/notebooks/06_cost_overrun.ipynb) |

## Suggested reading route

1. Read the opening business question and data assumptions.
2. Inspect the charts and the decisions explained beside them.
3. Read the recommendation and limitations at the end.
4. Expand code only when you want implementation detail.

The two business projects are better read as illustrated case studies:
[ERP transformation](../projects/01-erp-transformation/APPROACH.md) and
[variation governance](../projects/02-variation-governance/APPROACH.md).

## Reproduce locally

```bash
python -m pip install -r requirements-notebooks.txt
python scripts/execute_notebooks.py
```

The runner launches a fresh Jupyter kernel for each notebook, executes every code cell,
checks for errors and saves outputs. To edit, open `.ipynb` files in JupyterLab, VS Code's
notebook editor or Colab. Install your preferred editor separately.

If the environment disallows kernel sockets, use `python scripts/execute_notebooks.py --in-process`.
This executes every cell with IPython rich output capture in a fresh Python process per notebook.

The authoring source is `scripts/build_notebooks.py`; rerunning it resets saved outputs.
Execute again before committing. Chart PNGs also appear in `outputs/notebook-figures/`.

## Colab behaviour and reproducibility

Use a fresh CPU runtime and **Runtime → Run all**. The setup cell clones the public repository
when the source is absent and checks out computational source revision
`363f7edcd6c2357bc167257fce4e36b771b216d6`. This pins the tested data and model implementation.
It installs the pinned core requirements plus matplotlib before importing numerical libraries.
No Drive mount, personal data, GPU or API key is required. Network is needed for setup.

If you already imported numerical packages in a Colab runtime before installing the pinned
versions, restart the session and run from the top. Locally the notebook uses your current
checkout; it does not silently fetch or overwrite local work. Dataset hashes are checked.

Validation used **fresh Python processes with IPython rich output capture** because local
kernel sockets were unavailable. It did not use a Jupyter kernel or an authenticated hosted
Colab session. Colab links and setup code are provided; service-specific runtime behaviour
can vary. The notebooks do not write to GitHub or modify client systems.

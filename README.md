# Life Insurance Predictor

A small Python project for training a model to predict life/health insurance charges from common features (age, sex, BMI, children, smoker status, region).

**Repository structure**

- `app.py` : minimal web/app interface to load the trained model and serve predictions.
- `generate_data.py` : utility to generate or preprocess the `insurance_dataset.csv` used for training.
- `insurance_dataset.csv` : dataset used by the project (columns: `age`, `sex`, `bmi`, `children`, `smoker`, `region`, `charges`).
- `train_model.py` : training script — loads dataset, trains model, saves trained artifact.

**Getting started (Windows - `cmd.exe`)**

1. Create and activate a virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

2. Install required packages (common dependencies used by the project):

```
pip install pandas numpy scikit-learn joblib flask
```

3. (Optional) If you need to regenerate or preprocess the dataset:

```
python generate_data.py
```

4. Train the model:

```
python train_model.py
```

This should produce a saved model file (e.g., `model.joblib` or similar) — check `train_model.py` for the exact output name and adjust `app.py` accordingly.

5. Run the app (if `app.py` is a Flask or similar app):

```
python app.py
```

Then open the web UI or POST to the prediction endpoint as implemented in `app.py`.

**Dataset**

The project includes `insurance_dataset.csv`. Typical columns are:

- `age` (int)
- `sex` (male/female)
- `bmi` (float)
- `children` (int)
- `smoker` (yes/no)
- `region` (categorical)
- `charges` (target: float)

If your dataset differs, inspect `train_model.py` to confirm expected column names and preprocessing.

**How the code is organized**

- `generate_data.py` : data creation / preprocessing steps; run this if you want to regenerate `insurance_dataset.csv`.
- `train_model.py` : contains the feature pipeline and model training flow. It typically:
  - loads the CSV,
  - splits train/test,
  - fits a model (e.g., LinearRegression, RandomForest),
  - evaluates performance (e.g., MSE, R2),
  - saves the model to disk.
- `app.py` : loads the saved model and exposes a simple interface (CLI/HTTP) for making predictions.

**Tips & troubleshooting**

- If `python` points to Python 2 on your system, use `python3` instead.
- If `train_model.py` fails with missing packages, install them with `pip install <package>`.
- Ensure `insurance_dataset.csv` is in the project root or update the path used in the scripts.

**Extending the project**

- Add a `requirements.txt` by running `pip freeze > requirements.txt` after installing packages.
- Add CLI arguments to `train_model.py` for hyperparameters and output paths.
- Add unit tests around preprocessing and the model pipeline.

**License & Contact**

This repository does not include an explicit license file. Add a `LICENSE` if you plan to make the project public.

For questions or improvements, open an issue or contact the project owner.

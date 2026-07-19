# Dataset Instructions

## Required Dataset

This project uses the **Updated Resume Dataset** from Kaggle for training the resume classifier.

### Download Steps

1. Visit: https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset
2. Click **Download** (requires Kaggle account)
3. Extract the ZIP file
4. Place `UpdatedResumeDataSet.csv` in this directory (`server/dataset/`)

### Expected CSV Format

The CSV should have these columns:

| Column   | Description                              |
|----------|------------------------------------------|
| Category | Job domain label (e.g., "Data Science")  |
| Resume   | Full resume text content                 |

### Categories in Dataset

The dataset contains ~2,400 resumes across 25 categories including:
- Data Science, Java Developer, Python Developer, DevOps Engineer
- Web Designing, Database, Hadoop, HR, Sales, and more

The training script (`server/ml/train_model.py`) will map these to the target categories.

### After Download

Run the training script:
```bash
cd server
python ml/train_model.py
```

This will train the model and save it to `server/trained_model/`.

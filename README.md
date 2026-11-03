# Personalized Learning Recommendation System (EduAura)

A full-stack, AI-powered Machine Learning Web Application designed for **BCA / College Capstone Submission**, implementing a complete **15-Module Architecture**.

The system utilizes **K-Means Clustering** for student behavioral segmentation, **Cosine Similarity** for ranked multi-modal resource matchmaking, and supervised classifiers to pinpoint student weak topics and prescribe customized 4-week learning roadmaps.

---

## 🌟 The 15 Project Modules & File Mapping

| # | Module Name | Core Functionality | Primary File |
|:---:|:---|:---|:---|
| **01** | **Student Management Module** | Student registration, authentication, academic records, GPA tracking, and behavioral preference storage. | `modules/module1_student.py` |
| **02** | **Data Collection Module** | Generates and loads multi-feature student datasets (marks, attendance, quizzes, study hours). | `modules/module2_collection.py` |
| **03** | **Data Preprocessing Module** | Deduplication, median/mode imputation, score normalization, outlier clipping, and derived metrics. | `modules/module3_preprocessing.py` |
| **04** | **Exploratory Data Analysis Module** | Publication-grade statistical visuals: correlation heatmaps, score distributions, and regressions. | `modules/module4_eda.py` |
| **05** | **Feature Selection Module** | ColumnTransformer standardizing numeric indicators and encoding categorical preferences. | `modules/module5_features.py` |
| **06** | **Machine Learning Model Module** | K-Means clustering algorithm, Cosine Similarity matching engine, and candidate classifiers. | `modules/module6_models.py` |
| **07** | **Model Training & Testing Module** | Stratified 80/20 train/test evaluation split, cross-validation metrics, and model persistence. | `modules/module7_training.py` |
| **08** | **Personalized Recommendation Module ⭐** | Core intelligence: identifies weak concepts, predicts topic pathways, and curates multi-modal learning assets. | `modules/module8_recommendation.py` |
| **09** | **Recommendation Ranking Module** | Calculates exact multi-factor relevance percentages (95%, 91%, 87%) so highest value materials appear first. | `modules/module9_ranking.py` |
| **10** | **Model Evaluation Module** | Silhouette score, Inertia, Precision@K, Recall@K, Accuracy, F1-scores, and comparative model leaderboards. | `modules/module10_evaluation.py` |
| **11** | **Data Visualization Module** | Dynamic interactive radar competency profiles, progress meters, and cohort performance distributions. | `modules/module11_visualization.py` |
| **12** | **Student Dashboard Module** | Comprehensive portal with diagnosis, 4-week study roadmap, resource catalog, and direct star feedback. | `modules/module12_dashboard.py` |
| **13** | **Admin Management Module** | Administrative management of student rosters, resource CRUD operations, and system telemetry monitoring. | `modules/module13_admin.py` |
| **14** | **Feedback Module** | Students evaluate recommended materials with 1-5 star ratings and relevance feedback saved to database. | `modules/module14_feedback.py` |
| **15** | **Report & Result Module** | Generates comprehensive individual diagnostic reports and cohort summaries with 1-click Markdown download. | `modules/module15_reports.py` |

---

## 🛠️ Technology Stack

- **Backend**: Python Flask (`app.py`)
- **Database**: SQLite (`learning_system.db`)
- **Machine Learning**: Scikit-Learn (`KMeans`, `Cosine Similarity`, `Random Forest`, `Logistic Regression`, `Decision Tree`, `KNN`)
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Matplotlib, Seaborn, and Client-Side Chart.js
- **Frontend**: Responsive HTML5, Bootstrap 5, Modern Vanilla CSS with Glassmorphism & Dark Luxury Aesthetics

---

## 🚀 How to Run the Project

### 1. Activate Environment & Install Dependencies
```bash
# If using the included virtual environment:
.\.venv\Scripts\activate

# Install dependencies:
pip install -r requirements.txt
```

### 2. Start the Web Application
```bash
python app.py
```
Open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## 🔑 Demo Access Credentials

### 1. Student Demo Profiles
- **Suman Jana**: Student ID: `S001` • Password: `student123`
- **Priya Sharma**: Student ID: `S002` • Password: `student123`
- **Rahul Roy**: Student ID: `S003` • Password: `student123`
*(Or use the 1-Click Fast Login buttons on the Sign In page, or register a new student!)*

### 2. Administrator Portal
- **Username**: `admin`
- **Password**: `admin123`
*(Enables student roster deletion, adding new curated resources, and re-training the ML pipeline)*

---

## 📊 Complete Project Architecture Workflow

```text
              PERSONALIZED LEARNING
              RECOMMENDATION SYSTEM
                       │
        ┌──────────────┴──────────────┐
        │                             │
   Student Module                Admin Module
        │                             │
        ↓                             ↓
   Student Data                  Resource Management
        │
        ↓
   Data Collection (Module 2)
        │
        ↓
   Data Preprocessing (Module 3)
        │
        ↓
   EDA & Visualization (Module 4)
        │
        ↓
   Feature Selection (Module 5)
        │
        ↓
   Machine Learning (Module 6 & 7)
        │
   ┌────┴───────────┐
   │                │
K-Means          Cosine
Clustering       Similarity
(Personas)       (Ranking)
   │                │
   └───────┬────────┘
           ↓
   Personalized Recommendation (Module 8)
           │
           ↓
   Recommendation Ranking (Module 9)
           │
           ↓
   Student Dashboard (Module 12)
           │
           ↓
   Feedback & Rating (Module 14)
           │
           ↓
   Model Evaluation (Module 10)
           │
           ↓
   Results & Reports (Module 15)
```

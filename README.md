# Medal Backend

Backend for ML models that analyze lab results, generate workout plans, diet recommendations, and provide health/self-help guidance.

## ⚡ Features

- Lab results analysis  
- Personalized workout plans  
- Diet recommendations  
- Self-help tips (sleep, stress, health)  
- API-first: easily integrate with frontend or mobile apps  

## 🛠 Tech Stack

Python + FastAPI | PostgreSQL | PyTorch/TensorFlow | JWT Auth | Docker

## 🚀 Installation

```bash
git clone https://github.com/yourusername/healthai-backend.git
cd healthai-backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn src.main:app --reload

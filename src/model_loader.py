# src/services/model_loader.py
from transformers import ViTImageProcessor, ViTForImageClassification
import torch

MELANOMA_MODEL_HF_ID = "UnipaPolitoUnimore/vit-large-patch32-384-melanoma"

class ModelRegistry:
    melanoma_model = None
    melanoma_processor = None
    device = None

def load_models():
    ModelRegistry.device = torch.device(
        "cuda" if torch.cuda.is_available() else
        "mps" if torch.backends.mps.is_available() else
        "cpu"
    )

    ModelRegistry.melanoma_processor = ViTImageProcessor.from_pretrained(MELANOMA_MODEL_HF_ID)
    ModelRegistry.melanoma_model = ViTForImageClassification.from_pretrained(MELANOMA_MODEL_HF_ID)
    ModelRegistry.melanoma_model = ModelRegistry.melanoma_model.to(ModelRegistry.device)
    ModelRegistry.melanoma_model.eval()
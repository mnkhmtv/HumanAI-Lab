import base64
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import torch
import torchvision.transforms as transforms
from PIL import Image
from transformers import AutoModelForImageClassification, AutoFeatureExtractor
from io import BytesIO
import shelve
import uuid

app = FastAPI(docs_url="/")

# Load the pretrained model and feature extractor
model_name = "hilmansw/resnet18-catdog-classifier"
model = AutoModelForImageClassification.from_pretrained(model_name)
feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
model.eval()

# Define image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=feature_extractor.image_mean, std=feature_extractor.image_std),
])

# Define class labels
labels = ["Cat", "Dog"]
REPORT_DB = "reports"
TRUE_REPORTS_DB = "true_reports"

class ReviewReportRequest(BaseModel):
    report_id: str
    is_true: bool


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(BytesIO(await file.read())).convert("RGB")
    image = transform(image).unsqueeze(0)  # Add batch dimension
    
    with torch.no_grad():
        outputs = model(image)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        confidence, predicted_class = torch.max(predictions, dim=-1)
    
    return {"label": labels[predicted_class.item()], "confidence": confidence.item()}

@app.post("/report/")
async def report(file: UploadFile = File(...), correct_label: str = "Neither"):
    image_data = await file.read()
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    report_id = str(uuid.uuid4())
    with shelve.open(REPORT_DB) as db:
        db[report_id] = {"label": correct_label, "image": encoded_image}
    return {"message": "Report submitted", "report_id": report_id}

@app.get("/reports/")
async def get_reports():
    with shelve.open(REPORT_DB) as db:
        reports = ... # TODO: return all reported images with the reported class 
    return reports

@app.post("/review_report/")
async def review_report(request: ReviewReportRequest):
    with shelve.open(REPORT_DB) as db:
        if request.report_id in db:
            ...
            # TODO: move the report to True Reports if is_true
    return {"error": "Report not found"}

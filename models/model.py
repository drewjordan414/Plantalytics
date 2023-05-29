import torch
import torchvision.models as models
import cv2

model1 = models.resnet18(pretrained=False)
num_ftrs = model1.fc.in_features
model1.fc = torch.nn.Linear(num_ftrs, 38)
model1.load_state_dict(torch.load('plant-disease-model-complete.pth'))

model2 = models.resnet18(pretrained=False)
num_ftrs = model2.fc.in_features
model2.fc = torch.nn.Linear(num_ftrs, 38)
model2.load_state_dict(torch.load('plant-disease-model.pth'))

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model1.to(device)
model2.to(device)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
frame = cv2.resize(frame, (224, 224))
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame = frame.transpose((2, 0, 1))
frame = frame/255.0

model1.eval()
model2.eval()
with torch.no_grad():
    input = torch.from_numpy(frame).unsqueeze(0).float().to(device)
    output1 = model1(input)
    output2 = model2(input)
    _, preds1 = torch.max(output1, 1)
    _, preds2 = torch.max(output2, 1)
    pred = preds1.item() if preds1.item() == preds2.item() else 38

print(pred)


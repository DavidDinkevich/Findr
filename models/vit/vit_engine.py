import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image

# Load pre-trained ViT model
model = torch.hub.load('facebookresearch/dino:main', 'dino_vits8')

# Set model to evaluation mode
model.eval()

# Load and preprocess image
image = Image.open('../resources/giraffe.png')
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

image = transform(image)

# Load and preprocess text
text = 'giraffe'
text = model.transformer.tokenizer(text, return_tensors='pt')['input_ids']

# Encode image and text
with torch.no_grad():
    image_embedding = model.backbone(image.unsqueeze(0))
    text_embedding = model.transformer(text).last_hidden_state.mean(dim=1)

# Compute cosine similarity between image and text embeddings
similarity = F.cosine_similarity(image_embedding.squeeze(0), text_embedding)
print(similarity.item())

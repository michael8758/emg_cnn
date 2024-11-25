import torch
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from model import CNN
from preprocess import preprocess_data

def evaluate_model(checkpoint_path, test_data_path):
    # Load the model
    model = CNN()
    model.load_state_dict(torch.load(checkpoint_path))
    model.eval()

    # Preprocess test data
    inputs, targets = preprocess_data(test_data_path)
    test_dataset = torch.utils.data.TensorDataset(inputs, targets)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

    # Run evaluation
    all_preds = []
    all_targets = []

    with torch.no_grad():  # No gradient computation during evaluation
        for inputs, targets in test_loader:
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)  # Get predicted class
            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(targets.cpu().numpy())

    # Calculate accuracy
    accuracy = accuracy_score(all_targets, all_preds)
    print(f"Accuracy: {accuracy:.4f}")

    # Detailed metrics
    print("\nClassification Report:")
    print(classification_report(all_targets, all_preds, digits=4))

    # Confusion matrix
    cm = confusion_matrix(all_targets, all_preds)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=range(7), yticklabels=range(7))
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.show()

if __name__ == "__main__":
    checkpoint_path = "checkpoints/best_model.pt"  # Path to saved model
    test_data_path = "data/raw/emg_data.csv"       # Path to test data
    evaluate_model(checkpoint_path, test_data_path) 
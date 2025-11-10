import hashlib
import matplotlib.pyplot as plt

def hash_text_content(content):
    return hashlib.sha256(content.encode()).hexdigest()

def plot_similarity(results, labels):
    plt.bar(labels, results)
    plt.xlabel("Document/Image")
    plt.ylabel("Similarity Score")
    plt.show()

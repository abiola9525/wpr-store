import nltk
import os

nltk_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nltk_data')
nltk.data.path.append(nltk_data_path)
nltk.download('punkt', download_dir=nltk_data_path)

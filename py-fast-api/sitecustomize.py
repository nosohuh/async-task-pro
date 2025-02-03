import sys
import os

# 'src' dizinini PYTHONPATH'a ekle
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(project_root)

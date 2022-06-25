#pip install -r requirements.txt
#python -m spacy download en
#sh preprocess.sh
CUDA_VISIBLE_DEVICES=0 python main.py --model conve --data LegalCaseStudy --epochs 80
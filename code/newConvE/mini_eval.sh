#pip install -r requirements.txt
#python -m spacy download en
#sh preprocess.sh
python modelEvaluation.py --model conve --data LegalCaseStudy --epochs 1 --preprocess
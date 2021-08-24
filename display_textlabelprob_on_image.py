import argparse
from PIL import Image
import requests
from transformers import CLIPProcessor, CLIPModel
from pprint import pprint

parser = argparse.ArgumentParser(description='')    #
parser.add_argument('--image_file')
parser.add_argument('args', nargs=argparse.REMAINDER)
args = parser.parse_args()
image_file = args.image_file
token_list = args.args
	
def get_textlabel_prob_on_image(text_label_list, image_file):
	model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
	processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
	image = Image.open(image_file)
	inputs = processor(text=text_label_list, images=image, return_tensors="pt", padding=True)
	outputs = model(**inputs)
	logits_per_image = outputs.logits_per_image
	probs = logits_per_image.softmax(dim=1)
	
	return probs

def main():		
	prob_list = get_textlabel_prob_on_image(token_list , image_file)
	#prob_list = get_textlabel_prob_on_image(["cat", "dog"], "doraemon.jpg")
	print("次の画像を解析します。：　", image_file)
	print("次のラベルの該当確率を推定します。　：　", token_list)
	#print(prob_list.tolist())
	tmp_double_list = prob_list.tolist() # 結果は二重リスト
	probability_list = tmp_double_list[0]
	probability_list = [round(prob, 2) for prob in probability_list]
	#print(probability_list)
	output_list = ["ラベル名： {label}   該当確率： {prob}".format(label=label,  prob=str(prob*100)+"%") for label, prob  in zip(token_list, probability_list)]  
	for label_prob_str in output_list:
		print(label_prob_str)
	
if __name__ == "__main__":
    main()
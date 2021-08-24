## 使い方

### （画像１）
 
```bash:Terminal
electron@diynoMacBook-Pro Desktop % ls doraemon.jpg                                                          
doraemon.jpg
electron@diynoMacBook-Pro Desktop % open doraemon.jpg 
```

https://user-images.githubusercontent.com/87643752/130586549-beb07952-24ae-418c-beab-1c14ca611e87.png


```bash:Terminal
electron@diynoMacBook-Pro Desktop % python3 display_textlabeLprob_on_image.py --image_file doraemon.jpg 'cat' 'dog'
次の画像を解析します。：　 doraemon.jpg
次のラベルの該当確率を推定します。　：　 ['cat', 'dog']
ラベル名： cat   該当確率： 91.0%
ラベル名： dog   該当確率： 9.0%
electron@diynoMacBook-Pro Desktop %
```

```bash:Terminal
electron@diynoMacBook-Pro Desktop % python3 display_textlabeLprob_on_image.py --image_file doraemon.jpg 'cat' 'dog' 'human' 'pig' '
raccoon dog' 'house' 'robot' 'sky'
次の画像を解析します。：　 doraemon.jpg
次のラベルの該当確率を推定します。　：　 ['cat', 'dog', 'human', 'pig', '\nraccoon dog', 'house', 'robot', 'sky']
ラベル名： cat   該当確率： 52.0%
ラベル名： dog   該当確率： 5.0%
ラベル名： human   該当確率： 14.000000000000002%
ラベル名： pig   該当確率： 3.0%
ラベル名： 
raccoon dog   該当確率： 1.0%
ラベル名： house   該当確率： 1.0%
ラベル名： robot   該当確率： 18.0%
electron@diynoMacBook-Pro Desktop %
```

### （画像２） 

```bash:Terminal
electron@diynoMacBook-Pro Desktop % open nozomi.jpg 
electron@diynoMacBook-Pro Desktop % 
```

https://user-images.githubusercontent.com/87643752/130586573-035a2380-acdb-4385-9cd1-bec76ee705e9.png


```bash:Terminal
electron@diynoMacBook-Pro Desktop % python3 display_textlabeLprob_on_image.py --image_file nozomi.jpg 'cat' 'dog' 'human' 'woman' 'girl'
次の画像を解析します。：　 nozomi.jpg
次のラベルの該当確率を推定します。　：　 ['cat', 'dog', 'human', 'woman', 'girl']
ラベル名： cat   該当確率： 0.0%
ラベル名： dog   該当確率： 0.0%
ラベル名： human   該当確率： 4.0%
ラベル名： woman   該当確率： 48.0%
ラベル名： girl   該当確率： 48.0%
electron@diynoMacBook-Pro Desktop %
```

```bash:Terminal
electron@diynoMacBook-Pro Desktop % python3 display_textlabeLprob_on_image.py --image_file nozomi.jpg 'cute' 'beautiful' 'elegant' 'awful' 'boyish' 'big' 'small'       
次の画像を解析します。：　 nozomi.jpg
次のラベルの該当確率を推定します。　：　 ['cute', 'beautiful', 'elegant', 'awful', 'boyish', 'big', 'small']
ラベル名： cute   該当確率： 15.0%
ラベル名： beautiful   該当確率： 19.0%
ラベル名： elegant   該当確率： 61.0%
ラベル名： awful   該当確率： 0.0%
ラベル名： boyish   該当確率： 1.0%
ラベル名： big   該当確率： 1.0%
ラベル名： small   該当確率： 4.0%
electron@diynoMacBook-Pro Desktop %
```

```bash:Terminal
electron@diynoMacBook-Pro Desktop %python3 display_textlabeLprob_on_image.py --image_file nozomi.jpg 'cute' 'awful' 'boyish' 'big' 'small'          
次の画像を解析します。：　 nozomi.jpg
次のラベルの該当確率を推定します。　：　 ['cute', 'awful', 'boyish', 'big', 'small']
ラベル名： cute   該当確率： 72.0%
ラベル名： awful   該当確率： 1.0%
ラベル名： boyish   該当確率： 6.0%
ラベル名： big   該当確率： 3.0%
ラベル名： small   該当確率： 18.0%
electron@diynoMacBook-Pro Desktop %
```






## ソースコード

```Python3: display_textlabeLprob_on_image.py
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
```

import torch
import os
import json
from transformers import BertForSequenceClassification, BertTokenizer

# 初始化和加载模型


def map_train_id_to_real_type(train_ids):
    with open("data/tag_mapping.json", "r", encoding="utf-8") as f:
        tag_mapping = json.load(f)
    # 根据值找键
    types = []
    for train_id in train_ids:
        types.append(tag_mapping[str(train_id)])
    return types


def load_model(model_path, tokenizer_path='bert-base-multilingual-cased'):
    # 使用绝对路径
    model_path = os.path.abspath(model_path)

    # 加载模型
    model = BertForSequenceClassification.from_pretrained(
        model_path,
        revision="safetensors",
        torch_dtype=torch.float16,
        trust_remote_code=True
    )
    model.eval()  # 切换到评估模式

    # 检查是否有可用的 GPU
    if torch.cuda.is_available():
        model.cuda()

    # 加载分词器
    tokenizer = BertTokenizer.from_pretrained(tokenizer_path)

    return model, tokenizer

# 预处理文本


def preprocess(text, tokenizer):
    # 对文本进行分词处理
    encoded = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    return encoded

# 使用模型进行预测


def predict(text, model, tokenizer, count=3):
    # 预处理文本
    encoded_input = preprocess(text, tokenizer)

    # 将处理好的数据移至模型所在设备
    input_ids = encoded_input['input_ids']
    attention_mask = encoded_input['attention_mask']

    # 检查模型是否在 GPU 上，并将输入张量移动到相同的设备
    device = next(model.parameters()).device
    input_ids = input_ids.to(device)
    attention_mask = attention_mask.to(device)

    # 模型预测
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)

    # 获取 logits 并计算概率
    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=1)

    # 返回最大count个概率的标签

    top_probs, top_indices = torch.topk(probs, count)
    top_probs = top_probs.squeeze().tolist()
    top_indices = top_indices.squeeze().tolist()

    predicted_labels = map_train_id_to_real_type(top_indices)
    results = {label: prob for label, prob in zip(predicted_labels, top_probs)}
    return results


def main():

    model_path = './model'  # 模型存储路径

    # 预测文本
    sample_text_path = './data/test_problem.txt'
    with open(sample_text_path, 'r', encoding='utf-8') as f:
        sample_text = f.read()
    # sample_text = "Example text that you want to classify."

    # 加载模型和分词器
    model, tokenizer = load_model(model_path)

    # 进行预测
    result = predict(sample_text, model, tokenizer, count=5)
    print(result)


# 如果这个文件被直接运行，执行main函数
if __name__ == "__main__":
    main()

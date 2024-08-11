import json
import csv

# 读取标签数据
with open('./data/tags.json', 'r') as f:
    tag_data = json.load(f)

    algo_type = 2
    valid_ids = set()
    for tag in tag_data["tags"]:
        if tag['type'] == algo_type:
            valid_ids.add(tag['id'])

    print(f"{len(valid_ids)} tags in total.")

# 创建从原始标签到连续整数的映射
tag_id_to_index = {tag: idx for idx, tag in enumerate(valid_ids)}

# 创建从连续整数到标签字符串的映射
with open('./data/tags.json', 'r') as f:
    tag_data = json.load(f)
    # index_to_tag_str =
    # 从tag_id_to_index获取值对应的键id的名称
    index_to_tag_str = {tag_id_to_index[tag['id']]: tag['name'] for tag in tag_data["tags"] if tag['id'] in valid_ids}

# 保存标签映射关系
with open('./data/tag_mapping.json', 'w') as f:
    json.dump(index_to_tag_str, f, indent=4, ensure_ascii=False)


# 处理问题数据
with open("./data/problems.csv", "r") as f:
    reader = csv.reader(f)
    problems = list(reader)
    print(f"{len(problems)} problems before processing.")
    algo_problems = []
    # 处理问题，过滤和重新标记标签
    idx = 1
    for problem in problems[1:]:  # 跳过标题行
        tags = json.loads(problem[3])
        new_tags = [tag_id_to_index[tag] for tag in tags if tag in valid_ids]
        if new_tags:
            algo_problems.append([idx, problem[2], json.dumps(new_tags)])
            idx += 1
    print(f"{idx - 1} problems after processing.")

# 保存处理后的问题数据
with open("./data/algo_problems.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "text", "tags"])
    writer.writerows(algo_problems)

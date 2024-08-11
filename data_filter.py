import json
import csv

# tags.json数据来自 https://www.luogu.com.cn/_lfe/tags
with open('./data/tags.json') as f:
    tag_data = json.load(f)

    algo_type = 2
    # 保留json中type为"type": 2, 的数据，返回一个有效id的集合
    valid_ids = set()
    for tag in tag_data["tags"]:
        if tag['type'] == algo_type:
            valid_ids.add(tag['id'])

    # print(valid_ids)
    print(f"{len(valid_ids)} tags in total.")

with open("./data/problems.csv", "r") as f:
    # 把已有的csv文件过滤掉不含有效标签的题目，并且重新生成一个csv文件，滤去无关的标签，其中最右边一侧是tags

    reader = csv.reader(f)
    problems = list(reader)
    print(f"{len(problems)} problems before processing.")
    algo_problems = []
    # id,title,text,tags,url
    idx = 1
    for problem in problems[1:]:
        tags = json.loads(problem[3])
        if any(tag in valid_ids for tag in tags):
            for tag in tags:
                if tag not in valid_ids:
                    tags.remove(tag)
            algo_problems.append([idx, problem[2], json.dumps(tags)])
            idx += 1
    print(f"{idx} problems after processing.")

    with open("./data/algo_problems.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(algo_problems)

    # print(algo_problems)

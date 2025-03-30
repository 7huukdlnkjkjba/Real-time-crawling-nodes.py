import requests
import time
import os

# 文件名
FILE_NAME = "节点.txt"

# 请求头
HEADERS = {
    "referer": "https://www.github.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}

# GitHub仓库信息
REPOS = [
    # url1: 从README中提取<code>内容
    {
        "type": "html",
        "url": "https://github.com/yushion/PublicNodes-Free",
        "raw_url": "https://raw.githubusercontent.com/yushion/PublicNodes-Free/main/README.md"
    },
    # url2: 直接获取文本内容
    {
        "type": "raw",
        "url": "https://raw.githubusercontent.com/xiaoji235/airport-free/main/v2ray.txt"
    },
    # url3: 追加的文本内容
    {
        "type": "raw",
        "url": "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/README.md"
    }
]


def get_html_content(url):
    """获取HTML内容并提取<code>标签内容"""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        # 使用BeautifulSoup解析HTML
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        codes = soup.find_all('code')
        return '\n'.join(code.get_text() for code in codes)
    except Exception as e:
        print(f"解析HTML失败: {e}")
        return None


def get_raw_content(url):
    """获取原始文本内容"""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"获取内容失败: {e}")
        return None


def save_content(content, mode='w'):
    """保存内容到文件"""
    if not content:
        return
    with open(FILE_NAME, mode, encoding='utf-8') as f:
        f.write(content + '\n')


def main():
    # 首次运行时清空文件
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)

    while True:
        print(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} 开始更新节点...")

        # 处理前两个URL（覆盖写入）
        main_content = []
        for repo in REPOS[:2]:
            if repo['type'] == 'html':
                content = get_html_content(repo['url'])
            else:
                content = get_raw_content(repo['url'])

            if content:
                main_content.append(content)

        # 合并内容并写入文件
        if main_content:
            save_content('\n'.join(main_content), 'w')

        # 处理第三个URL（追加写入）
        if len(REPOS) >= 3:
            append_content = get_raw_content(REPOS[2]['url'])
            if append_content:
                save_content(append_content, 'a')

        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} 节点更新完成")
        time.sleep(3600)  # 每小时运行一次


if __name__ == "__main__":
    main()

'''
requests + bs4 实现百度贴吧帖子信息抓取
保存信息到txt文件中
'''


# 引入相关库
import requests
from bs4 import BeautifulSoup
import time
import random

# 设置随机user-agent
def get_agent():
	agents = [
		'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'
	]
	agent = {}
	agent['User-Agent'] = random.choice(agents)

	return agent

# 使用requests获取页面内容
def get_html(url):
	try:
		r = requests.get(url, headers=get_agent(), timeout=30)
		r.raise_for_status()
		r.encoding = 'utf-8'
		return r.text
	except:
		return "get html error"

# 使用bs4库解析页面内容
def parse_html(url, base_url):
	html = get_html(url) # 获取页面内容
	soup = BeautifulSoup(html, 'lxml') # 解析页面内容
	comments = [] # 用来存储所有帖子的信息

	# 获取所有包含帖子信息的li
	lis = soup.find_all('li', class_=" j_thread_list clearfix")
	for li in lis:
		# 遍历列表，将每个帖子信息分别保存
		comment = {}
		comment['title'] = li.find('a', class_="j_th_tit ")['title'] # 标题
		comment['link'] = base_url + li.find('a', class_="j_th_tit ")['href'] # 帖子链接
		comment['author'] = li.find('a', class_="frs-author-name").text.strip() # 作者
		comment['time'] = li.find('span', class_="pull-right is_show_create_time").text.strip() # 创建时间
		comment['reply'] = li.find('span', class_="threadlist_rep_num").text.strip() # 回复数量
		comments.append(comment) # 将帖子信息添加到列表中

	return comments

# 将帖子信息存入文件中
def save_file(result):
	with open('bdtb.txt', 'a+', encoding='utf-8') as f:
		for comment in result:
			f.write('标题: {}\t作者: {}\n链接: {}\n发帖时间: {}\t回复数量: {}\n\n'.format(
				comment['title'], comment['author'], comment['link'], comment['time'], comment['reply']))
		print('当前页面存储完成')

# 主函数执行过程
def main(page):
	base_url = "https://tieba.baidu.com"
	main_url = "https://tieba.baidu.com/f?ie=utf-8&kw=fgo&pn="
	url_list = []

	for i in range(page):
		url_list.append(main_url + str(i*50))
	print('网页下载完成')

	for url in url_list:
		result = parse_html(url, base_url)
		save_file(result)

# 执行程序
if __name__ == '__main__':
	offset = 3
	main(offset)
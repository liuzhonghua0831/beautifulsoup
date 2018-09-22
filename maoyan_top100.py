'''
使用requests + bs4抓取猫眼电影top100排行榜电影信息
保存数据到txt文件与json文件
'''
# 引入相关库
import requests
from bs4 import BeautifulSoup
import random
import json

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

# 获取页面内容
def get_html(url):
	try:
		r = requests.get(url, headers=get_agent(), timeout=30)
		r.raise_for_status()
		r.encoding = 'utf-8'
		return r.text
	except:
		return "get html error"

# 解析页面内容
def parse_html(url, base_url):
	html = get_html(url)
	soup = BeautifulSoup(html, 'lxml')
	comments = [] # 存放所有电影信息
	all_info = soup.find('dl', class_="board-wrapper") # 确定所有电影信息存放位置
	dds = all_info.find_all('dd') # 获取所有电影内容
	for dd in dds:
		# 存放每部电影信息
		comment = {}
		# 电影排名
		comment['index'] = dd.find('i', class_="board-index").text
		# 电影标题
		comment['title'] = dd.find('p', class_="name").a.text
		# 主演
		comment['actor'] = dd.find('p', class_="star").text.strip()[3:]
		# 电影链接
		comment['link'] = base_url + dd.find('p', class_="name").a['href']
		# 上映时间
		comment['time'] = dd.find('p', class_="releasetime").text.strip()[5:]
		# 评分
		int_s = dd.find('i', class_="integer").text
		fra_s = dd.find('i', class_="fraction").text
		comment['score'] = int_s + fra_s
		# 电影宣传图
		comment['image'] = dd.find('img', class_="board-img")['data-src']

		comments.append(comment)

	return comments

# 保存文件
def save_file(result):
	# 保存到txt
	with open('mytop100.txt', 'a+', encoding='utf-8') as f:
		for comment in result:
			f.write('排名: {}\t标题: {}\t主演: {}\n链接: {}\n上映时间: {}\t评分: {}\n宣传图: {}\n\n'.format(
				comment['index'], comment['title'], comment['actor'], comment['link'], comment['time'],comment['score'],comment['image']))

	# 保存到json
	with open('mytop100.json', 'a+', encoding='utf-8') as f:
		f.write(json.dumps(result, ensure_ascii=False) + '\n')

	print("当前页面保存完成")
# 保存图片
def save_image(result):
	for comment in result:
		with open('{}.jpg'.format(comment['title']), 'wb+') as f:
			f.write(requests.get(comment['image']).content)

# 主程序执行过程
def main(page):
	base_url = 'http://maoyan.com'
	main_url = 'http://maoyan.com/board/4?offset='
	url_list = []

	# 保存所有页面
	for i in range(page):
		url = main_url + str(i*10)
		url_list.append(url)

	# 解析每一个页面
	for url in url_list:
		result = parse_html(url, base_url)
		save_file(result)
		save_image(result)

# 执行主程序
if __name__ == '__main__':
	offset = 10
	main(offset)
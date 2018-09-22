'''
抓取音悦台MV排行榜信息
数据保存到txt和json
'''

# 引入相关库
import requests
from bs4 import BeautifulSoup
import random
import json
import time


def get_agent():
	agents = [
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    	"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    	"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    	"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    	"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3"
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
def parse_html(url):
	html = get_html(url)
	soup = BeautifulSoup(html, 'lxml')
	comments = []
	# 获取榜单所属区域
	area = soup.find('a', class_="J_cur").text.strip()
	# 获取榜单信息
	ul = soup.find('ul', id="rankList")
	lis = ul.find_all('li', class_="vitem J_li_toggle_date ")
	for li in lis:
		comment = {}
		# MV标题
		comment['title'] = li.find('a', class_="mvname").text.strip()
		# MV排名
		comment['index'] = li.find('div', class_="top_num").text.strip()
		# MV演唱者
		singers = li.find_all('a', class_="special")
		if len(singers) == 1:
			comment['singer'] = singers[0].text.strip()
		else:
			comment['singer'] = singers[0].text.strip()
			for singer in singers[1:]:
				comment['singer'] = comment['singer'] + '&' + singer.text.strip()
		# MV发布时间
		comment['time'] = li.find('p', class_="c9").text.strip()[5:]
		# MV链接
		comment['link'] = li.find('a', class_="mvname")["href"]
		# MV封面
		comment['image'] = 'http:' + li.find('a', class_="img video-bo-img").img['src']
		# MV评分
		if li.find('h3', class_="asc_score"):
			comment['score'] = li.find('h3', class_="asc_score").text.strip()
		else:
			comment['score'] = li.find('h3', class_="desc_score").text.strip()

		comments.append(comment)

	return area, comments

# 保存文件到txt
def save_txt(result):
	area, comments = result
	with open('MVpaihangbang.txt', 'a+', encoding='utf-8') as f:
		f.write('地区: {}\n'.format(area))
		for comment in comments:
			f.write('标题: {}\n排名: {}\t评分: {}\n演唱者: {}\t发布时间: {}\nMV链接: {}\nMV封面: {}\n\n'.format(
				comment['title'],comment['index'],comment['score'],comment['singer'],comment['time'],comment['link'], comment['image']))
	print('txt保存完成')

# 保存文件到json
def save_json(result):
	area, comments = result
	with open('MVpaihangbang.json', 'a+', encoding='utf-8') as f:
		f.write('地区: {}\n'.format(area))
		f.write(json.dumps(comments, ensure_ascii=False) + '\n')
	print('json保存完成')

# 保存图片
def save_image(result):
	area, comments = result
	for comment in comments:
		with open('{}.jpg'.format(comment['title']), 'wb+') as f:
			f.write(requests.get(comment['image']).content)
	print('图片保存完成')

# 主程序执行过程
def main():
	main_url = 'http://vchart.yinyuetai.com/vchart/trends?area='
	area_list = ['ML', 'HT', 'US', 'KR', 'JP']
	url_list = []
	for item in area_list:
		url = main_url + item
		url_list.append(url)

	for url in url_list:
		print(url)
		result = parse_html(url)
		save_txt(result)
		save_json(result)
		save_image(result)
		time.sleep(2)

# 执行主程序
if __name__ == '__main__':
	main()
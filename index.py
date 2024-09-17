import requests
import json
import time
import warnings
from requests.packages import urllib3
urllib3.disable_warnings()
warnings.filterwarnings('ignore')

startTime = time.time()

print('免责声明：本软件仅限用于学习和研究目的，不得将本软件用于任何非法用途，否则一切后果请用户自负。您必须在下载后的24个小时之内将本软件“易班劣课.exe”从您的电脑中彻底删除。')
print('开源协议：本软件遵循协议GPLv3协议，开源地址: https://github.com/EnderWolf006/YiBanClassGroupAutoViewer\n')
print('第一步: 自行在浏览器上登录“易班劣课”')
print('第二步: 在主页右上角头像下拉菜单中选择“我的课群”')
print('第三步: 按键盘上的F12或Fn+F12键打开开发者工具')
print('第四步: 在新打开的边栏窗口上方标签中点击Network或网络')
print('第五步: 选中下面的Fetch/XHR，然后刷新网页')
print('第六步: 刷新后下方会显示出记录，单击任选其一(joined.../managing...)')
print('第七步: 在新打开的窗口中选中Headers或标头')
print('第八步: 在下方滚动滚轮找到Request Headers或请求标头')
print('第九步: 展开它，复制Cookie后面的所有文字并粘贴在本软件中(右键粘贴)')
cookie = input('请粘贴后按回车运行: ')
csrfmiddlewaretoken = cookie.split('csrftoken=')[1].split(';')[0]
headers = {
  'Cookie': cookie,
  'X-CSRFToken': csrfmiddlewaretoken
}


def watchClassGroup(classGroup):
  url = 'https://www.yooc.me{}/courses'.format(classGroup['url'])
  res = requests.get(url, headers=headers, verify=False).text
  pages = int(res.split("!($('#newpageid').val()>")[1].split(") && $('#newpageid').val().match(/^[0-9]*[1-9][0-9]*$/)){")[0])
  print('>> 正在读取课群: ' + classGroup['title'])
  for i in range(1, pages + 1):
    url = 'https://www.yooc.me{}/courses?page={}'.format(classGroup['url'], i)
    res = requests.get(url, headers=headers, verify=False).text
    items = res.split('<div class="page" style="border-top:none;">')[0].split('<div class="detail-holder">')[1:]
    for item in items:
      url2 = item.split('<a href=')[1].split(' target="_blank"><img data-src="')[0]
      title = item.split('<p class="na" title="')[1].split('">')[0]
      if '图文' in item:
        url2 += '/review'
      requests.post(url2, headers=headers, verify=False, allow_redirects=True)
      if 'inside' in item:
        location = requests.post(url2, headers=headers, verify=False, allow_redirects=False).headers['Location']
        location = requests.post(location, headers=headers, verify=False, allow_redirects=False).headers['Location']
        res2 = requests.get(location, headers=headers, verify=False).text
        payload = 'course_id={}&enrollment_action=enroll&csrfmiddlewaretoken={}'.format(location.split('courses/')[1].split('/about')[0], csrfmiddlewaretoken)
        requests.post('https://xueyuan.yooc.me/change_enrollment',verify=False, data=payload, headers=headers)
        print('   已报名站内课程: ' + title)
        items2 = res2.split('<a href="/courses/')[1:]
        for item2 in items2:
          url3 = 'https://xueyuan.yooc.me/courses/' + item2.split('">')[0]
          res3 = requests.get(url3, headers=headers, verify=False).text
          url4 = 'https://xueyuan.yooc.me/courses' + res3.split('/save_user_state')[0].split('/courses')[-1] + '/save_user_state'
          res4 = requests.post(url4, headers=headers, verify=False, data='csrfmiddlewaretoken={}&saved_video_position=00:00:01&video_duration=00:00:02&done=true'.format(csrfmiddlewaretoken)).text
          title2 = item2.split('<h4>')[1].split('/h4')[0]
          if json.loads(res4)['success']:
            print('      >> 已浏览完成站内子课程: ' + title2)
          else:
            print('      Error >> ' + title2)
      else:
        print('   已浏览完成站外课程: ' + title)

# 获取加入课群列表
def getClassGroupList():
  result = []
  for i in range(1, 100):
    url = f"https://www.yooc.me/group/joined?_={int(1000 * time.time())}&page={i}"
    res = json.loads(requests.get(url, headers=headers, verify=False).text)
    for classGroup in res['items']:
      result.append({
        'url': classGroup['url'],
        'title': classGroup['title']
      })
    if not res['more']:
      return result

classGroupList = getClassGroupList()
for classGroup in classGroupList:
  watchClassGroup(classGroup)

print('\n================================================')
print('>> 已全部完成！用时{}秒，您可以关闭此程序了 <<'.format(int(time.time() - startTime)))
print('================================================')
input()
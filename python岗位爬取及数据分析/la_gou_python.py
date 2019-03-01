import time
import requests


class LaGouSpider(object):

    def __init__(self):
        # 招聘数据网址
        self.url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'


        self.header = {
            'Host': 'www.lagou.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.lagou.com/jobs/list_Python?labelWords=&fromSearch=true&suginput=',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Anit-Forge-Token': 'None',
            'X-Anit-Forge-Code': '0',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '26',
            'Cookie': '_ga=GA1.2.426059804.1543821485; user_trace_token=20181203151805-93da1104-f6cb-11e8-896c-525400f775ce; LGUID=20181203151805-93da1893-f6cb-11e8-896c-525400f775ce; JSESSIONID=ABAAABAAAIAACBIC43C890165AA2A9390534B64A8208149; _gat=1; LGSID=20190109102444-ba39f840-13b5-11e9-8a39-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DJuVDJASm3ZIZK1jshnmn40lRmN9RSfkscK64rjoL_4_%26ck%3D1387.1.96.310.146.309.140.192%26shh%3Dwww.baidu.com%26sht%3Dmonline_4_dg%26wd%3D%26eqid%3Dcc14287200062734000000055c355b66; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20190109102451-be0c708e-13b5-11e9-8a39-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; SEARCH_ID=ade86a19ca6f4433aea49b8d9641f284',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }

    def laGouSpider(self, pageNum):
        '''获取数据'''

        for pn in range(1, pageNum):

            # 表单数据
            data = {
                'first': 'false',
                'kd': 'Python',  # 采集Python数据
                'pn': pn
            }
            # 暂停1s
            time.sleep(1)
            # 提交表单数据
            response = requests.post(self.url, data=data, headers=self.header)

            yield response.json()

    def parseResponse(self, response):
        '''解析数据 提取数据'''
        data = response['content']['positionResult']
        # 遍历提取数据
        for dat in data['result']:
            # 岗位职称
            positionName = dat['positionName']
            # 工作经验
            workYear = dat['workYear']
            # 学历要求
            education = dat['education']
            # 工作类型
            jobNature = dat['jobNature']
            # 公司发展
            financeStage = dat['financeStage']
            # 工作地点
            city = dat['city']
            # 工资
            salary = dat['salary']
            # 工作福利
            #positionAdvantage = dat['positionAdvantage']
            # 公司名称
            companyShortName = dat['companyShortName']

            print(f'{positionName},{workYear},{education},{jobNature},{financeStage},{city},{salary},{companyShortName}')
            data = f'{positionName},{workYear},{education},{jobNature},{financeStage},{city},{salary},{companyShortName}'
            
            # 保存数据
            self.saveFile(data)

    def saveFile(self, data):
        '''保存数据'''

        with open('LaGouData.csv', 'a', encoding='utf-8') as fp:
            fp.write(data+'\n')


if __name__ == '__main__':

    lagouspider = LaGouSpider()
    # 调用爬取数据的方法
    jsonResponse = lagouspider.laGouSpider(31)
    # 循环遍历数据并解析保存
    for jsondata in jsonResponse:
        lagouspider.parseResponse(jsondata)


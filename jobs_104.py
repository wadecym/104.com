'''
作者 : wade chen
測試日期 : 2019/3/6
'''

import requests
import os
import time
import jsonpath
import json


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }

    #查詢的關鍵字
    kw ='爬蟲'

    # 104網站使用的地區對應號碼 = {
    #     '台北市全部':6001001000
    #     '新北市全部':6001002000
    #     '宜蘭縣全部':6001003000
    #     '基隆市全部':6001004000
    #     '桃園市全部':6001005000
    #     '新竹市全部':6001006000
    #     '苗栗縣全部':6001007000
    #     '台中市全部':6001008000
    #     '彰化縣全部':6001010000
    #     '南投縣全部':6001011000
    #     '雲林縣全部':6001012000
    #     '嘉義縣市全部':6001013000
    #     '台南市全部':6001014000
    #     '高雄市全部':6001016000
    #     '屏東縣全部':6001018000
    #     '台東縣全部':6001019000
    #     '花蓮縣全部':6001020000
    #     '澎湖縣全部':6001021000
    #     '金門縣全部':6001022000
    #     '連江縣全部':6001023000
    #
    # }
    #地區代碼 :台北市全區及新竹縣市全區,地區中間使用%2C連接,最多只能輸入10組地區號,超過的地區號會被網站過濾掉
    area='6001001000%2C6001006000'

    #建立連接
    s = requests.Session()

    #先搜尋第一頁
    url = 'https://www.104.com.tw/jobs/search/list?ro=0&kwop=7&keyword='+kw+'&area='+area+'&order=11&asc=0&page=1&mode=s'
    html = s.get(url=url, headers=headers).content.decode('utf-8')
    jsonobj = json.loads(html)

    #查詢總頁數
    totalpage = jsonpath.jsonpath(jsonobj, '$.[totalPage]')[0]
    print('此職缺總頁數 : ' ,totalpage)

    #列出第一頁項目

    jobname_list = jsonpath.jsonpath(jsonobj,'$.data.list.[jobName]')
    custname_list = jsonpath.jsonpath(jsonobj,'$.data.list.[custName]')
    jobaddrnodesc_list = jsonpath.jsonpath(jsonobj,'$.data.list.[jobAddrNoDesc]')
    perioddesc_list = jsonpath.jsonpath(jsonobj,'$.data.list.[periodDesc]')
    salarydesc_list = jsonpath.jsonpath(jsonobj,'$.data.list.[salaryDesc]')
    print('第1頁資料 : ')
    for k in range(0,len(jobname_list)):
        print('第1頁第%s項資料 : ' %(k+1))
        print('職稱: %s ; 公司名稱 : %s ; 公司地點 : %s ; 需求經驗 : %s ; 待遇 : %s' % (
        jobname_list[k], custname_list[k], jobaddrnodesc_list[k], perioddesc_list[k], salarydesc_list[k]))

        #搜尋資料儲存成文件
        data = jobname_list[k] + ';' + custname_list[k] + ';' + jobaddrnodesc_list[k] + ';' + perioddesc_list[k] + ';' + \
               salarydesc_list[k] + '\n\n'
        #文件名稱
        filename = '104jobs_' + kw + '.text'
        #文件路徑
        base_path = 'D:\\'
        filepath = os.path.join(base_path, filename)

        with open(filepath, 'a+', encoding='utf-8') as f:
            f.write(data)

    # 切換頁面時等待1秒
    time.sleep(1)

    if totalpage > 2 :
        #搜尋其他頁數
        for i in range(2,totalpage+1):

            url = 'https://www.104.com.tw/jobs/search/list?ro=0&kwop=7&keyword='+kw+'&area='+area+'&order=11&asc=0&page='+str(totalpage)+'&mode=s'
            html = s.get(url=url, headers=headers).content.decode('utf-8')
            jsonobj=json.loads(html)

            print('第%s頁資料 : ' %i)

            jobname_list = jsonpath.jsonpath(jsonobj,'$.data.list.[jobName]')
            custname_list = jsonpath.jsonpath(jsonobj,'$.data.list.[custName]')
            jobaddrnodesc_list = jsonpath.jsonpath(jsonobj,'$.data.list.[jobAddrNoDesc]')
            perioddesc_list = jsonpath.jsonpath(jsonobj,'$.data.list.[periodDesc]')
            salarydesc_list = jsonpath.jsonpath(jsonobj,'$.data.list.[salaryDesc]')

            for j in range(0,len(jobname_list)):
                print('第%s頁第%s項 : ' %(i,j+1))
                # print('totalpage',totalpage_list[j])
                # print('jobname',jobname_list[j])
                # print('custname',custname_list[j])
                # print('jobaddrnodesc',jobaddrnodesc_list[j])
                # print('perioddesc',perioddesc_list[j])
                # print('salarydesc',salarydesc_list[j])

                print('職稱: %s ; 公司名稱 : %s ; 公司地點 : %s ; 需求經驗 : %s ; 待遇 : %s' %(jobname_list[j],custname_list[j],jobaddrnodesc_list[j],perioddesc_list[j],salarydesc_list[j]))

                data = jobname_list[j] + ';' + custname_list[j]  + ';' + jobaddrnodesc_list[j]  + ';' + perioddesc_list[j]  + ';' + salarydesc_list[j] +'\n\n'

                filename = '104jobs_'+kw+'.text'
                base_path = 'D:\\'
                filepath = os.path.join(base_path,filename)

                with open(filepath,'a+',encoding='utf-8') as f:
                    f.write(data)

            #等待1秒後再請求下一頁資料
            time.sleep(1)

if __name__ == '__main__':
    main()
from bs4 import BeautifulSoup
import logging
import csv

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

data = []
count = 0


def parse(soup, _tag):
    root = soup.select('#sdMajorsFirstCollegeList')[0]  # 所有志愿
    for aspiration in root.contents:  # 每个志愿
        try:
            if aspiration=="\n":
                continue
            asData=aspiration.contents
            predictedRanking=asData[1].select("div")[0].text
            logging.info("录取概率:"+asData[1].select("div")[0].text)
            collegeName=asData[3].text.split("\n")[1]
            logging.info("学校:"+asData[3].text.split("\n")[1])
            _type=asData[3].text.split("\n")[2].split('\xa0/\xa0')[0]
            logging.info("学校类型:"+asData[3].text.split("\n")[2].split('\xa0/\xa0')[0])
            location=asData[3].text.split("\n")[2].split('\xa0/\xa0')[1]
            logging.info("地区:"+asData[3].text.split("\n")[2].split('\xa0/\xa0')[1])
            isPublic=asData[3].text.split("\n")[2].split('\xa0/\xa0')[2]
            logging.info("公办/民办:"+asData[3].text.split("\n")[2].split('\xa0/\xa0')[2])
            belongTo=asData[3].text.split("\n")[2].split('\xa0/\xa0')[3]
            logging.info("隶属单位:"+asData[3].text.split("\n")[2].split('\xa0/\xa0')[3])
            collegeRank=asData[3].text.split("\n")[3].split(" ")[2]
            logging.info("学校排名:"+asData[3].text.split("\n")[3].split(" ")[2])
            logging.info("学校代码:"+asData[3].text.split("\n")[3].split(" ")[1][:-2])
            major=asData[5].text.split("\n")[1]
            logging.info("专业名称:"+asData[5].text.split("\n")[1])
            marjorNumber=asData[5].text.split("\n")[2].split(' ')[1]
            if asData[5].text.split("\n")[2].split(' ')[1][-2:]=='专科':
                majorType='专科'
            else:
                majorType='本科'
            logging.info("专业代码:"+asData[5].text.split("\n")[2].split(' ')[1])
            logging.info("学制:"+asData[7].text.split(' ')[64].split('\n')[2])
            fee=asData[7].text.split(' ')[64].split('\n')[3]
            logging.info("年度学费:"+asData[7].text.split(' ')[64].split('\n')[3])
            preMajor=asData[7].text.split(' ')[64].split('\n')[4]
            logging.info("选考科目:"+asData[7].text.split(' ')[64].split('\n')[4])
            planNumber=asData[7].text.split(' ')[0].replace('\n','').split('/')[0]
            logging.info("招生人数:"+planNumber)
            try:
                rank2019=asData[11].select('.historyYearWrapper')[1].text
                logging.info("2019最低录取位次:"+asData[11].select('.historyYearWrapper')[1].text)
            except:
                rank2019="该年度未招生"
                logging.info("2019最低录取位次:"+"该年度未招生")
            try:
                rank2018=asData[11].select('.historyYearWrapper')[4].text
                logging.info("2018最低录取位次:"+asData[11].select('.historyYearWrapper')[4].text)
            except:
                rank2018="该年度未招生"
                logging.info("2018最低录取位次:"+"该年度未招生")
            try:
                rank2017=asData[11].select('.historyYearWrapper')[7].text
                logging.info("2017最低录取位次:"+asData[11].select('.historyYearWrapper')[7].text)
            except:
                rank2017="该年度未招生"
                logging.info("2017最低录取位次:"+"该年度未招生")
            
            data.append((collegeName, major,majorType, predictedRanking, _tag, location, fee,_type, belongTo, isPublic, planNumber, collegeRank,rank2019,rank2018,rank2017))
        except Exception as e:
            logging.error(e)


def output():
    logging.info('开始写入文件')
    try:
        csvfile = open('志愿数据.csv', 'w')
        writer = csv.writer(csvfile)
        writer.writerow(['学校', '专业','本科/专科', '录取概率', '风险', '地区', '年度学费',
                         '学校类型', '隶属单位', '公办/民办', '招生人数', '学校排名','2019最低录取位次','2018最低录取位次','2017最低录取位次'])
        writer.writerows(data)
        csvfile.close()
    except Exception as e:
        logging.critical('文件写入失败，错误信息如下：')
        raise
    else:
        logging.info('文件写入成功!')


def main():
    logging.info('开始解析数据')
    soup = BeautifulSoup(open('aspirationHtmlParser/material/冲.html', encoding='utf-8'))
    parse(soup, '冲')
    soup = BeautifulSoup(open('aspirationHtmlParser/material/稳.html', encoding='utf-8'))
    parse(soup, '稳')
    soup = BeautifulSoup(open('aspirationHtmlParser/material/保.html', encoding='utf-8'))
    parse(soup, '保')
    logging.info('数据解析完成')
    output()


if __name__ == '__main__':
    logging.info('程序开始')
    main()
    logging.info('程序结束')
else:
    logging.info('非法调用!')

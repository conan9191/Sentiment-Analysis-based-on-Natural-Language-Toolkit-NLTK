import requests
from lxml import etree
import time
import emoji
url = 'https://www.amazon.com/Greenlights-Matthew-McConaughey-ebook/product-reviews/B086823SWK/ref=cm_cr_getr_d_paging_btm_next_%d?ie=UTF8&reviewerType=all_reviews&pageNumber=%d'

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
# 'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
'cache-control': 'max-age=0',
'cookie': 'ubid-main=135-3761994-2155044; skin=noskin; lc-main=en_US; csd-key=eyJ2IjoxLCJraWQiOiJmMGYzOTEiLCJrZXkiOiJmbHVkaEhsbWhGMnBER2hoRUlseUNhYTBIcG1NUVEzRHUzb2FYOWdkdUZsaHhxV1VzUzJtSm1RSVl4ajBmR2N3OFkwTEJjQ2FqRVQxU3ZkQWlwTCtRcFhvUkFKbUNIYzByWUJSditxd2Z3VGJvdjFRN3ROS3hKNEIxY0w0TmkvamluYkp6di83K0Ribk9CekVWYUtqWHZUdEd0MUcra2M2MmlHME1kWUc2THVIcmV6SEVJbk1JSFlhY3Iwdi9qMVBQNnBSdk1Oc1FsdHhBdWdReGV4U01MNWNHbmJPTW1aMzloU1RjZjQyeVUrdmx0VEI2bmtGdHlublVFZ0pDZDQ0UGkxU2lwT05CbGpnN0Z2NUdjMnRuMTZxMnl0SDVwTkFpekEzTGxocThTMFMxaTNOMVdreTZuN3kxSmpaclllMDhrd29pcnJkajhjWUlRUlhNT1h5T3c9PSJ9; x-main="9s32qVz?p84Ee229esyjNhCHPczlr8vnhnVfQOCCTjNV6BloSwnOVsB7U@jP8k7z"; at-main=Atza|IwEBIJAQ5GskRV373AcCbIg6T9nOvN8MhQfnDlamIQLZs2nu4G7myYp9HASVl3Pu6621vrh1mC1qtItY4mGiF51Q_j7IJSG5lRCsipKrPbdb_-gP9ngRTkVuoiofYTQ9CLzVyV1JOiySchWb7XyiAZcw93rIEJGs4zKL34RVk9BfFOpEKU8srhGgUI-WzWDYl24KYnuKcWxzjy8rYeuRx1Mx6kd_; sess-at-main="zDsI5S/FalOoZCpy3e1ggavVYZNKkvrrvCNeNiM5OAs="; sst-main=Sst1|PQHgFUUEX9gO1C_49GY4osRTCcgf99tVA9KvKJSmwjryovtWnhWadsFeRgjYS9qa6ONqbx2vI_1paATyiUPDiydJuhZg8GvtQcyQg0Gsdir-nEZizxPcE8AR5XEiVmISCpdzM90aa3QGQ56noJFiLGBr94PLCB9p-BQ82MfmZG4FRFrLcaxExwbJHk9QWdq2lVQ_4gayNAkZfHYxWmoii6Y3NQ0nUO4fAXMlTECGbRvbEL4eSWfMzAqMPVVJSxwL2QPaYca0-5elzwWY31NhooLOR2w2dWoqUzWjKq98k6-z2QY; i18n-prefs=USD; session-id=133-7188628-4125453; session-id-apay=133-7188628-4125453; session-id-time=2082787201l; session-token="ueoFxGQ+4DV0Ht2B+TLhbco4jH8+8mzKKv2ztNPpQc2QAGSNIsxj67CGKB1DiXxi4+LOVJMvk1+z6x69n9E+OUhTEN9NGrV04h2h7ifzW+QKyOAz+vVvde8ql0qls+eqMSCSWtcDad6mf2+dfW1oVbgUIgdluZqzdSIQMxHDBwbNYYPN+2oaqyWzJ8VOuXp8z3dAOKf9CUI6C+iLj1g0Tg=="; csm-hit=tb:Z50E5WS90EWNM52B1EB4+sa-QBEJJA43F4K7H4X7ERVB-974TCS0ZKPN2V1VR0S76|1608002380977&t:1608002380977&adb:adblk_no',
'downlink': '10',
'ect': '4g',
'referer': 'https://www.amazon.com/dp/B086823SWK',
'rtt': '0',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'same-origin',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

if __name__ == '__main__':
    fp = open('climb.csv', mode='w',encoding='utf-8')
    fp.write('comment\trate\n')
    for i in range(1,79):
        page = url%(i, i)
        response = requests.get(page,headers=headers)
        response.encoding = 'utf-8'
        text = response.text
        html = etree.HTML(text)
        comments = html.xpath('//div[@id="cm_cr-review_list"]/div[@class="a-section review aok-relative"]')
        for comment in comments:
            c = comment.xpath('.//span[@class="a-size-base review-text review-text-content"]/span/text()')[0].strip()
            rate = comment.xpath('.//span[@class="a-icon-alt"]/text()')[0].strip()
            c = emoji.demojize(c)
            fp.write('%s\t%s\n' % (c, rate))
        print('Page ',i,' saved!')
        time.sleep(1)
    fp.close()
import requests
from bs4 import BeautifulSoup

# class crawl():
#     """
#     """
#     def 

# re.compile("")
# def crawl(url, name, class_, id, href, string):
#     req = requests.get(url)
#     soup = BeautifulSoup(r.text,"html.parser")

def en_dictionary(keyword):
    """
    return: list -> dict
        'part_of_speech': string
        'uk_kk': string
        'us_kk': string
        'uk_audio': string(url)
        'us_audio': string(url)
        'description': list -> dict
            'guide_word': string
            'def': list -> dict
                'def_en': string
                'def_tw': string
                'sentences': list -> string
    """
    desktop = "https://dictionary.cambridge.org"
    url = "https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{}".format(keyword)
    req = requests.get(url)
    soup = BeautifulSoup(req.text,"html.parser")

    word = soup.find(name='span', class_='hw dhw').text
    result = []
    word_def = soup.find_all(name='div', class_='pr entry-body__el')
    for define in word_def:
        res = dict()
        res['part_of_speech'] = define.find(name='span', class_='pos dpos').text
        kk_pronounce = define.find_all(name='span', class_='ipa dipa lpr-2 lpl-1')
        res['uk_kk'] = '/' + kk_pronounce[0].text + '/'
        res['us_kk'] = '/' + kk_pronounce[1].text + '/'
        audio = soup.find_all(name='source', type='audio/mpeg')
        res['uk_audio'] = desktop + audio[0].get('src')
        res['us_audio'] = desktop + audio[1].get('src')

        res['description'] = list()
        descripe = define.find_all(name='div', class_='pr dsense')
        for description in descripe:
            des = dict()
            des['guide_word'] = description.find(name='span', class_='guideword dsense_gw').find('span').text
        
            des['def'] = list()
            blocks = description.find_all(name='div', class_='def-block ddef_block')
            for b in blocks:
                def_block = dict()
                def_block['def_en'] = b.find(name='div', class_='def ddef_d db').text
                def_block['def_tw'] = b.find(name='span', class_='trans dtrans dtrans-se').text
                def_block['sentences'] = [s.text for s in b.find_all(name='div', class_='examp dexamp')]

                des['def'].append(def_block)

            res['description'].append(des)

        result.append(res)

    return result

# def ko_dictionary(keyword):
#     """
#     """
#     result = dict()

#     url = "https://zh.dict.naver.com/#/search?query={}".format(keyword)
#     req = requests.get(url)
#     soup = BeautifulSoup(req.text,"html.parser")

#     content = soup.find(name='div', class_='section section_keyword') \
#         .find_all(name='div', class_='row')
#     audio = content[0].find(name='button', class_='btn_listen play').get('purl')
#     for word_def in content:
#         mean_l = word_def.find_all(name='p', class_='mean')
        
#         mean_list = list()
#         for mean in mean_l:
#             mean_list.append(mean)
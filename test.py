import re

text = "Мои каналы товаров👇\nMy channels 👇\n\n01, Мужские и женские кроссовки и др спортивная обувь!👇(Sneakers)\n\nhttps://t.me/joinchat/AAAAAEe69TkviZJSruK91whttps://t.me/joinchat/AAAAAEe69TkviZJSruK91w\n----------------------------------\n\n02 Женская одежда 1. ПРЕМИУМ СЕГМЕНТ👇Woman clothes \nhttps://t.me/joinchat/AAAAAFRgscTKOW-SMlu03w\n---------------------------\n02-2.  ЖЕНСКАЯ ОДЕЖДА. 2- КАНАЛ👇\nhttps://t.me/jenskaya2\n‐------------------------------------\n03, Мужская одежда👇Man clothes \n\nhttps://t.me/joinchat/AAAAAEnfQhq9ZoQ5DlOjVg\n-----------------------\n04. Женская обувь👇Woman's shoes\n\nhttps://t.me/joinchat/AAAAAFgIrkNlN4jLg3pKBw\n--------------‐-----------------------------------------\n05. Сумки и аксессуары 1:1 люкс копии 👇\n\nhttps://t.me/sumkilux2022\n-------------------‐-----------------------------------\n06. Сумки и аксессуары Bags and accessories \n\nhttps://t.me/+V6onvS3AAjnCIG4t\n\n07. Штучные товары👇(retail channel)\nhttps://t.me/+T_KdCUEN3KCiy5C6\n\n\n08. Детская одежда 👇\n\nhttps://t.me/detskiye2021\n\n\n\n\n\nКак делать заказ?)\n\n1) Выбираем товары и пересылаем в личку  @uzbekkonsertstudio прямо из группы. \nДля оптовых каналов - Просьба не скринить фото либо отправлять из галереи. Только пересылка из канала.\nДля штучного канала - пересыл с указанием цены на след канале. Это ускорит подсчёт.\n2) Я делаю итоговый расчет.  Иногда приходится узнавать цены на фабриках или в магазинах, если не указаны они. \n3) После формирования заказа оплата принимается по золотой короне на мое имя либо другого представителя. \n4) После оплаты собирается весь заказ в течении одного- двух дней и сдается на карго (компания отправки). \n❇️❇️❇️❇️❇️❇️❇️❇️❇️❇️❇️❇️❇️\n\nМои контакты:\n+905369314628\nТелеграм @uzbekkonsertstudio\nМашхур"
pattern = re.compile(r'\bhttps://t\.me/(joinchat/).{4,}?\b')
a = list(map(lambda x: x.group(), re.finditer(r'\bhttps://t\.me/(joinchat/)?.{4,}?\b', text)))
for k in re.sub(r'(https://t\.me/(joinchat/)?(.+?))+', r' \3', ''.join(a)).split():
    print(k)


import datetime
notis = []
arhiv = []
arhivtoday = []
kontracts = {}
prodajy_za_mesatz = {}
prodajy_za_day = {}
prodaji_for_staticrica = {}
zakazy = {}
tovary = {}
nedela = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
mesazy = dict.fromkeys([4, 6, 9, 11], 30)                             #словарь "месяц: день"
m_31 = dict.fromkeys([1, 3, 5, 7, 8, 10, 12], 31)
m_2 = {2: 28} 
mesazy.update(m_31)
mesazy.update(m_2)

def dobavit():               
    flag = True
    while flag:
        otd = input('Введите наименование отдела, в который будет добавлен товар')
        if otd != '':
            tovary.setdefault(otd, {})
            flag = False
        else:
            print('А вы всё же введите')
    flag = True
    while flag:
        code = input('введите штрих-код товара')
        if len(code) == 13 and code.isdigit():
            if code in tovary[otd]:
                Flag = True
            else:
                Flag = False    
            tovary[otd].setdefault(code, {})
            flag = False    
        else:
            print('Некорректный ввод')                       
    flag = True
    if not Flag:
        while flag:
            tovar = input('Введите наименование товара')
            if tovar == '':
                print('А вы всё же введите')
            else:
                tovary[otd][code]['название'] = tovar
                flag = False
    flag = True        
    while flag:
        kol_sclad = input('Введите кол-во товара на складе')
        if kol_sclad.isdigit():
            kol_sclad = int(kol_sclad)
            flag = False
        else:
            print('Некорректный ввод')
    flag = True        
    while flag:
        kol_vmestimost = input('Введите примерное кол-во вместимости товара на полках')
        if kol_vmestimost.isdigit():
            kol_vmestimost = int(kol_vmestimost)    
            flag = False
        else:
            print('Некорректный ввод')        
    flag = True        
    while flag:
        kol_polka = input('Введите кол-во товара на полках')
        if kol_polka.isdigit():
            kol_polka = int(kol_polka) 
            if kol_polka <= kol_vmestimost:   
                flag = False
            else:
                print('Перепроверьте выставленное кол-во. Оно не может быть больше вместимости на полке')    
        else:
            print('Некорректный ввод')                                
    flag = True         
    fleg = False
    while flag:
        nachgodn, kongodn = input('Введите дату выпуска товара '), input('Введите дату окончания срока годности товара ')
        if all([nachgodn.count('.') == 2, kongodn.count('.') == 2, nachgodn.replace('.', '').isdigit(), kongodn.replace('.', '').isdigit()]):
            nachday, nachmunth, nachyear = nachgodn.split('.')
            nachday, nachmunth, nachyear = int(nachday), int(nachmunth), int(nachyear)
            konday, konmunth, konyear = kongodn.split('.')
            konday, konmunth, konyear = int(konday), int(konmunth), int(konyear)
            if all([nachyear > 0, nachmunth > 0, nachmunth in mesazy, 0 < nachday <= mesazy[nachmunth]]):
                if all([konyear > 0, konmunth > 0, konmunth in mesazy, 0 < konday <= mesazy[konmunth]]):
                    kondata = datetime.date(konyear, konmunth, konday)
                    nachdata = datetime.date(nachyear, nachmunth, nachday)
                    fleg = True
                else:
                    print('введена несуществующая дата "годен до"') 
            else:
                print('введена несуществующая дата "произведен"')
            if fleg:               
                fleg = False
                if date > nachdata:
                    if kondata > date:
                        fleg = True
                        flag = False
                    else:
                        print('в добавлении просроченного товара отказать')    
                else:
                    print('перепроверьте правильность даты производства')
        else:
            print('Некорректный ввод')            
    if fleg:
        flag = True
        if not Flag:                                   
            while flag:                      
                postavshik = input('Введите поставщика товара ')
                if postavshik != '':
                    tovary[otd][code]['поставщик'] = postavshik
                    if postavshik not in kontracts:
                        fleg = True
                        while fleg:
                            fleg = False
                            datepr = input('данный поставщик нам неизвестен. Пажалуйста, введите дату последнего привоза товара ')
                            if all([datepr.count('.') == 2, datepr.replace('.', '').isdigit()]):
                                prday, prmunth, pryear = datepr.split('.')
                                prday, prmunth, pryear = int(prday), int(prmunth), int(pryear)
                                if all([pryear > 0, prmunth > 0, prmunth in mesazy, 0 < prday <= mesazy[prmunth]]):
                                        prdata = datetime.date(pryear, prmunth, prday)
                                        fleg = True
                                else:
                                    print('введена несуществующая дата ')
                                if fleg:               
                                    if prdata <= date:
                                        if prdata >= nachdata:
                                            fleg = False
                                        else:    
                                            print('перепроверьте правильность даты')        
                                    else:
                                        print('перепроверьте правильность даты')
                            else:
                                print('Некорректный ввод')
                        fleg = True
                        while fleg:
                            interval = input('Пажалуйста, введите интервал поездок(в днях) для занесения в базу данных ')
                            if interval.isdigit():
                                interval = int(interval)
                                if prdata + datetime.timedelta(days=interval) >= date:
                                    fleg = False                              
                                else:
                                    print('перепроверьте интервал либо дату последнего привоза ')    
                            else:
                                print('Некорректный ввод')
                        fleg = True
                        while fleg:
                            day_zakaza = input('Пажалуйста, введите, за какое кол-во дней до привоза нужно заказывать товар ')
                            if day_zakaza.isdigit():
                                day_zakaza = int(day_zakaza)
                                kontracts.setdefault(postavshik, {})
                                kontracts[postavshik]['интервал поездок'] = interval
                                kontracts[postavshik]['день заказа за'] = day_zakaza
                                kontracts[postavshik]['следующий приезд'] = prdata + datetime.timedelta(days=interval)
                                fleg = False                              
                            else:
                                print('Некорректный ввод')
                        flag = False                
                    else:
                        flag = False        
                else:
                    print('Некорректный ввод')            
            flag = True
        if not Flag:
            while flag:
                upa = input('Введите кол-во товара в одной упаковке ')
                if upa.isdigit():
                    upa = int(upa)
                    tovary[otd][code]['Штук в упаковке'] = upa
                    flag = False
                else:
                    print('Некорректный ввод')   
        godn = str(nachgodn) + '-' + str(kongodn)
        if 'сроки годности' in tovary[otd][code]:
            if godn in tovary[otd][code]['сроки годности']:
                fleg = False 
        kol = kol_polka + kol_sclad                   
        tovary[otd][code].setdefault('сроки годности', {}) 
        tovary[otd][code]['оставшееся кол-во'] = tovary[otd][code].get('оставшееся кол-во', 0) + kol
        tovary[otd][code]['кол-во выставленных'] = tovary[otd][code].get('кол-во выставленных', 0) + kol_polka
        tovary[otd][code]['кол-во на складе'] = tovary[otd][code].get('кол-во на складе', 0) + kol_sclad
        tovary[otd][code]['вместимость'] = tovary[otd][code].get('вместимость', kol_vmestimost) 
        pr = int((prdata + datetime.timedelta(days=interval) - date).days)
        tovary[otd][code]['привоз через'] = pr
        tovary[otd][code]['заказ через'] = pr - day_zakaza
        tovary[otd][code]['сроки годности'].setdefault(godn, {})
        tovary[otd][code]['сроки годности'][godn]['кол-во'] = tovary[otd][code]['сроки годности'][godn].get('кол-во', 0) + kol
        tovary[otd][code]['сроки годности'][godn]['кол-во выставленных'] = tovary[otd][code]['сроки годности'][godn].get('кол-во выставленных', 0) + kol_polka
        tovary[otd][code]['сроки годности'][godn]['кол-во на складе'] = tovary[otd][code]['сроки годности'][godn].get('кол-во на складе', 0) + kol_sclad
        k = kondata - date
        tovary[otd][code]['сроки годности'][godn]['дни'] = k.days
        while fleg:
            first_price, last_price = input('Введите закупочную цену(в долларах) '), input('Введите цену продажи(в долларах) ')
            if first_price.isdigit() and last_price.isdigit():
                first_price, last_price = int(first_price), int(last_price)
                if first_price < last_price: 
                    tovary[otd][code]['сроки годности'][godn]['закупочная цена'] = first_price
                    tovary[otd][code]['сроки годности'][godn]['цена продажи'] = last_price   
                    fleg = False
                else:
                    print('Хм... разве вы будете продавать товар себе в убыток? неее, мы Вам не позволим')    
            else:
                print('Некорректный ввод')
        tovary[otd][code]['динамика продаж (в процентах)'] = tovary[otd][code].get('динамика продаж (в процентах)', 'Товар только поступил в продажу')
        tovary[otd][code]['дней осталось до полной продажи'] = tovary[otd][code].get('дней осталось до полной продажи', 'Товар только поступил в продажу')
        tovary[otd][code]['Статистика'] = tovary[otd][code].get('Статистика', {'пн': 0, 'вт': 0, 'ср': 0, 'чт': 0, 'пт': 0, 'сб': 0, 'вс': 0})    
        print(tovary)
        print(prodajy_za_mesatz)
        print(prodajy_za_day)
        print(zakazy)
        print(kontracts)
def prodaja():
    flag = True
    while flag:
        code = input('введите штрих-код товара')
        if len(code) == 13 and code.isdigit():
            flag = False
        else:
            print('Некорректный ввод')
    for otd in tovary:
        if code in tovary[otd]:
            tovary[otd].setdefault(code, {})
            tovar = tovary[otd][code]['название']
            flag = True
            break
    if flag:               
        while flag:
            kol = input('Введите кол-во проданного товара')
            if not kol.isdigit():
                print('Некорректный ввод')   
            else:       
                kol = int(kol)
                godn = list(tovary[otd][code]['сроки годности'].keys())[0]
                if tovary[otd][code]['кол-во выставленных'] - kol >= 0:
                    flag = False
                    fleg = True
                else:
                    flag = False
                    fleg = False
                    print('перепроверьте проданное кол-во')
        if fleg:
            if tovary[otd][code]['сроки годности'][godn]['кол-во выставленных'] >= kol:                  
                tovary[otd][code]['сроки годности'][godn]['кол-во выставленных'] -= kol
                tovary[otd][code]['сроки годности'][godn]['кол-во'] -= kol
                tovary[otd][code]['оставшееся кол-во'] -= kol
                tovary[otd][code]['кол-во выставленных'] -= kol
            else:
                tovary[otd][code]['оставшееся кол-во'] -= kol
                tovary[otd][code]['кол-во выставленных'] -= kol
                for godn in tovary[otd][code]['сроки годности']:
                    if kol > tovary[otd][code]['сроки годности'][godn]['кол-во выставленных']:
                        tovary[otd][code]['сроки годности'][godn]['кол-во'] -= tovary[otd][code]['сроки годности'][godn]['кол-во выставленных']
                        kol -= tovary[otd][code]['сроки годности'][godn]['кол-во выставленных']
                        tovary[otd][code]['сроки годности'][godn]['кол-во выставленных'] = 0 
                    else:
                        tovary[otd][code]['сроки годности'][godn]['кол-во выставленных'] -= kol
                        tovary[otd][code]['сроки годности'][godn]['кол-во'] -= kol
                        break
            if tovary[otd][code]['кол-во выставленных'] <= 0.5 * tovary[otd][code]['вместимость']:
                notis.append(f'{datetime.datetime.now()}. Товара {tovar}, штрих-код {code}, осталось на полке меньше 50%. рекомендуется выставить еще.')        
            prodajy_za_day.setdefault(otd, {})
            prodajy_za_day[otd].setdefault(code, {})
            prodajy_za_day[otd][code]['название'] = prodajy_za_day[otd][code].get('название', tovar)
            prodajy_za_day[otd][code]['проданное кол-во'] = prodajy_za_day[otd][code].get('проданное кол-во', 0) + kol
            prodaji_for_staticrica.setdefault(otd, {})
            prodaji_for_staticrica[otd].setdefault(code, {})
            prodaji_for_staticrica[otd][code]['проданное кол-во'] = prodaji_for_staticrica[otd][code].get('проданное кол-во', 0) + kol                      
            prodajy_za_mesatz.setdefault(otd, {})
            prodajy_za_mesatz[otd].setdefault(code, {})
            prodajy_za_mesatz[otd][code]['название'] = prodajy_za_mesatz[otd][code].get('название', tovar)
            prodajy_za_mesatz[otd][code]['проданное кол-во'] = prodajy_za_mesatz[otd][code].get('проданное кол-во', 0) + kol
            tovary[otd][code]['Статистика'][den_nedeli] += kol 
            flag = True
            din = prodajy_za_day[otd][code]['проданное кол-во'] / (prodajy_za_day[otd][code]['проданное кол-во'] + tovary[otd][code]['оставшееся кол-во']) * 100
            tovary[otd][code]['динамика продаж (в процентах)'] = din                
            tovary[otd][code]['дней осталось до полной продажи'] = 100 // din - 1
            print(tovary)
            print(prodajy_za_mesatz)
            print(prodajy_za_day)
            print(zakazy)
            print(kontracts)
            print(prodaji_for_staticrica)
            print(notis)
    else:
        print('штрих-код не найден')        

def priezd():
    flag = True
    while flag:
        code = input('введите штрих-код товара')
        if len(code) == 13 and code.isdigit():
            flag = False
        else:
            print('Некорректный ввод')
    for otd in tovary:
        if code in tovary[otd]:
            flag = True
            break    
    if flag:         
        while flag:
            upa = input('Введите кол-во упаковок привезенного товара')
            if not (upa.isdigit() and int(upa) > 0):
                print('Некорректный ввод')
            else:
                upa = int(upa)
                flag = False
        flag = True
        while flag:
            nachgodn, kongodn = input('Введите дату выпуска товара '), input('Введите дату окончания срока годности товара ')
            if nachgodn.count('.') == 2 and kongodn.count('.') == 2 and nachgodn.replace('.', '').isdigit() and kongodn.replace('.', '').isdigit():
                nachday, nachmunth, nachyear = nachgodn.split('.')
                nachday, nachmunth, nachyear = int(nachday), int(nachmunth), int(nachyear)
                konday, konmunth, konyear = kongodn.split('.')
                konday, konmunth, konyear = int(konday), int(konmunth), int(konyear)
                if all([nachyear > 0, nachmunth > 0, nachmunth in mesazy, 0 < nachday <= mesazy[nachmunth]]):
                    if all([konyear > 0, konmunth > 0, konmunth in mesazy, 0 < konday <= mesazy[konmunth]]):
                        kondata = datetime.date(konyear, konmunth, konday)
                        nachdata = datetime.date(nachyear, nachmunth, nachday)
                        fleg = True
                    else:
                        print('введена несуществующая дата "годен до"') 
                else:
                    print('введена несуществующая дата "произведен"')
                if fleg:               
                    fleg = False
                    if date > nachdata:
                        if kondata > date:
                            fleg = True
                            flag = False
                        else:
                            print('в добавлении просроченного товара отказать')    
                    else:
                        print('перепроверьте правильность даты производства')           
            else:
                print('Некорректный ввод')
        tovary[otd][code].setdefault('сроки годности', {})
        godn = nachgodn + '-' + kongodn        
        if code in zakazy:
            if zakazy[code]['заказанное кол-во'] - upa == 0:
                first_price = zakazy[code]['закупочная цена']
                last_price = zakazy[code]['цена продажи']
                del zakazy[code]
            elif zakazy[code]['заказанное кол-во'] - upa > 0:
                print('НЕ поступили', zakazy[code]['заказанное кол-во'] - upa, 'упаковок')
                first_price = zakazy[code]['закупочная цена']
                last_price = zakazy[code]['цена продажи']
                zakazy[code]['заказанное кол-во'] -= upa
            else:
                print(upa - zakazy[code]['заказанное кол-во'], 'упаковок лишние')
                first_price = zakazy[code]['закупочная цена']
                last_price = zakazy[code]['цена продажи']
                upa = zakazy[code]['заказанное кол-во'] 
                del zakazy[code]
            kol = upa * tovary[otd][code]['Штук в упаковке']    
            tovary[otd][code]['оставшееся кол-во'] += kol
            tovary[otd][code]['кол-во на складе'] += kol
            tovary[otd][code]['сроки годности'].setdefault(godn, {})
            tovary[otd][code]['сроки годности'][godn]['кол-во'] = tovary[otd][code]['сроки годности'][godn].get('кол-во', 0) + kol
            tovary[otd][code]['сроки годности'][godn]['кол-во выставленных'] = tovary[otd][code]['сроки годности'][godn].get('кол-во выставленных', 0)
            tovary[otd][code]['сроки годности'][godn]['кол-во на складе'] = tovary[otd][code]['сроки годности'][godn].get('кол-во на складе', 0) + kol
            k = kondata - date
            tovary[otd][code]['сроки годности'][godn]['дни'] = k.days
            tovary[otd][code]['сроки годности'][godn]['закупочная цена'] = first_price
            tovary[otd][code]['сроки годности'][godn]['цена продажи'] = last_price
            if str(tovary[otd][code]['динамика продаж (в процентах)']).isdigit():
                if tovary[otd][code]['динамика продаж (в процентах)'] > 0:
                    din = tovary[otd][code]['динамика продаж (в процентах)']    
                    tovary[otd][code]['дней осталось до полной продажи'] = 100 // din - 1    
        else:
            print('заказа данного товара не было')
    else:
        print('неизвестный штрих-код')
    print(tovary)
    print(prodajy_za_mesatz)
    print(prodajy_za_day)
    print(zakazy)
    print(kontracts)              

def zakazat():
    flag = True
    while flag:
        code = input('введите штрих-код товара, который вы хотите заказать. ')
        if len(code) == 13 and code.isdigit():
            flag = False
        else:
            print('Некорректный ввод')
    for otd in tovary:
        if code in tovary[otd]:
            flag = True
            tovar = tovary[otd][code]['название']
            break
    if flag: 
        Flag = True            
        if code in zakazy:
            answer = input(f'на данный момент заказано {zakazy[code]['заказанное кол-во']} упаковок данного товара. вы действительно желаете увеличить заказ?').upper()
            while flag:
                if answer == 'НЕТ':
                    flag = False
                    fleg = False
                elif answer == 'ДА':
                    flag = False
                    fleg = True
                    Flag = False
                    first_price = zakazy[code]['закупочная цена']
                    last_price = zakazy[code]['цена продажи']
                else:
                    print('некорректный ввод. Попробуйте еще раз')            
        else:
            fleg = True
        if fleg:
            flag = True
            while flag:
                kol = input('введите кол-во упаковок, которые будут заказаны')
                if kol.isdigit():
                    kol = int(kol)
                    flag = False
                else:
                    print('некорректный ввод. Попробуйте еще раз')
            flag = True
            while Flag:
                answer = input('вы хотите использовать последнюю установленную цену на товар или ввести новую?').lower()
                if 'нов' in answer:
                    fleg = True
                    while fleg:
                        first_price, last_price = input('Введите закупочную цену(в долларах) '), input('Введите цену продажи(в долларах) ')
                        if first_price.isdigit() and last_price.isdigit():
                            first_price, last_price = int(first_price), int(last_price)
                            if first_price < last_price:    
                                fleg = False
                            else:
                                print('Хм... разве вы будете продавать товар себе в убыток? неее, мы Вам не позволим')    
                        else:
                            print('Некорректный ввод')
                    Flag = False
                elif 'послед' in answer:
                    godn = list(tovary[otd][code]['сроки годности'].keys())[-1]
                    first_price = tovary[otd][code]['сроки годности'][godn]['закупочная цена']
                    last_price = tovary[otd][code]['сроки годности'][godn]['цена продажи']
                    Flag = False
                else:
                    print('некорректный ввод')    
            price = kol * first_price * tovary[otd][code]['Штук в упаковке']
            flag = True       
            while flag:
                answer = input(f'будет заказано {kol} упаковок. стоимость составит {price} долларов США. Подтвердить операцию?').lower()
                if answer == 'да':
                    zakazy.setdefault(code, {})
                    zakazy[code]['название'] = tovar
                    zakazy[code]['заказанное кол-во'] = zakazy[code].get('заказанное кол-во', 0) + kol
                    zakazy[code]['стоимость (доллары США)'] = zakazy[code].get('стоимость (доллары США)', 0) + price
                    zakazy[code]['закупочная цена'] = first_price
                    zakazy[code]['цена продажи'] = last_price
                    flag = False
                elif answer == 'нет':
                    print('операция отменена')
                    flag = False
                else:
                    print('некорректный ввод. Попробуйте еще раз')       
    else:
        print('штрих-код не найден. Выберете соответствующую ф-цию, чтобы добавить информацию о товаре')
    print(tovary)
    print(prodajy_za_mesatz)
    print(prodajy_za_day)
    print(zakazy)
    print(kontracts)
def place():
    flag = True
    while flag:
        code = input('введите штрих-код товара, который вы хотите выставить. ')
        if len(code) == 13 and code.isdigit():
            flag = False
        else:
            print('Некорректный ввод')
    for otd in tovary:
        if code in tovary[otd]:
            flag = True
            break
    if flag:
        flag = True
        while flag:            
            godn = input(f'введите срок годности. доступные: {list(tovary[otd][code]['сроки годности'].keys())}')
            if godn not in list(tovary[otd][code]['сроки годности'].keys()):
                print('срок г-сти не найден')
            else:
                flag = False
        flag = True        
        while flag:
            kol = input('Введите кол-во выставленного товара')
            if not kol.isdigit():
                print('Некорректный ввод')   
            else:       
                kol = int(kol)
                if kol > tovary[otd][code]['сроки годности'][godn]['кол-во на складе']:
                    print('вы не можете выставить товара бальше, чем его кол-во на складе')
                else:    
                    flag = False
        tovary[otd][code]['кол-во на складе'] -= kol
        tovary[otd][code]['кол-во выставленных'] += kol
        tovary[otd][code]['сроки годности'][godn]['кол-во на складе'] -= kol
        tovary[otd][code]['сроки годности'][godn]['кол-во выставленных'] += kol            
    else:
        print('товар не найден')
    print(tovary)
    print(prodajy_za_mesatz)
    print(prodajy_za_day)
    print(zakazy)
    print(kontracts)     
def uchet():            
    for otd in tovary: 
        for code in tovary[otd]:
            tovary[otd][code]['Статистика'][den_nedeli] = 0                       #статистика
            tovar = tovary[otd][code]['название']
            postavshik = tovary[otd][code]['поставщик']                            #отправка уведомлений
            den_priezda = kontracts[postavshik]['следующий приезд']
            den_zakaza = kontracts[postavshik]['день заказа за']
            den_okonch = tovary[otd][code]['дней осталось до полной продажи']
            if str(den_okonch).isdigit():
                den_okonch = int(den_okonch)
                dni_smauga = (den_priezda - date).days - den_okonch
                Flag = True
            else:
                Flag = False   
            dni_do_zakaza = (den_priezda - datetime.timedelta(days=den_zakaza) - date).days
            interval = kontracts[postavshik]['интервал поездок']
            if otd in prodaji_for_staticrica:
                if code in prodaji_for_staticrica[otd]:
                    din = (prodaji_for_staticrica[otd][code]['проданное кол-во'] / (interval  - tovary[otd][code]['привоз через'])) / (prodaji_for_staticrica[otd][code]['проданное кол-во'] + tovary[otd][code]['оставшееся кол-во']) * 100 
                    tovary[otd][code]['динамика продаж (в процентах)'] = din  
                else:
                    tovary[otd][code]['динамика продаж (в процентах)'] = 0
                tovary[otd][code]['динамика продаж (в процентах)'] = din
            else:
                tovary[otd][code]['динамика продаж (в процентах)'] = 0    
            if Flag:
                if dni_smauga >= 1 and dni_do_zakaza > 1:
                    notis.append(f'{datetime.datetime.now()}. Товар {tovar}, штрих-код {code}, СРОЧНО нуждается в заказе вне очереди, т. к. в противном случае полки будут оставаться пустыми {dni_smauga} дней.')
                elif dni_smauga == 0 and dni_do_zakaza == 1:
                    notis.append(f'{datetime.datetime.now()}. Товар {tovar}, штрих-код {code}, завтра должен быть заказан. \nТовара хватит "впритык", поэтому заказ можно делать такой же, \nкак и в прошлый раз') 
                elif dni_smauga < 0 and dni_do_zakaza == 1:
                    notis.append(f'{datetime.datetime.now()}. Товар {tovar}, штрих-код {code}, завтра должен быть заказан. \nЧасть товара останется на полках,\nпоэтому нужно делать заказ меньше, чем в прошлый раз') 
                elif dni_smauga >= 1 and dni_do_zakaza == 1:
                    notis.append(f'{datetime.datetime.now()}. Товар {tovar}, штрих-код {code}, завтра должен быть заказан. \nТовара до конца не хватит,\nпоэтому нужно делать заказ больше, чем в прошлый раз')     
            else:
                notis.append(f'{datetime.datetime.now()}. Товар {tovar}, штрих-код {code}, завтра должен быть заказан. \n однако делать заказ не рекоммендуется по причине того, что товар вообще не продается')                    
            for godn in tovary[otd][code]['сроки годности']:
                tovary[otd][code]['сроки годности'][godn]['дни'] -= 1
            tovary[otd][code]['привоз через'] -= 1
            tovary[otd][code]['заказ через'] -= 1                

def change():
    pass
sostoyanie = input('Начать новый день? ').upper()
   
if sostoyanie == 'ДА' or sostoyanie == 'НАЧАТЬ НОВЫЙ ДЕНЬ':
    while sostoyanie != 'НЕТ':
        date = datetime.date.today()
        weekday = date.weekday()
        den_nedeli = nedela[weekday]
        prodajy_za_day = {}
        operation = ''
        while operation != 'закончить день':
            operation = input('Введите операцию ').lower()
            if operation == 'добавить':
                while True:
                    dobavit()
                    fleg = True
                    while fleg:
                        answer = input('добавить еще один товар?').lower()
                        if answer != 'нет' and answer != 'да':
                            print('некорректный ввод')
                        else:
                            fleg = False
                    if answer == 'нет':
                        break        

                print(tovary)   
            elif operation == 'продажа':
                prodaja()                                                                             #операция продажа                  
            elif operation == 'приехал':
                priezd()
            elif operation == 'заказать':
                zakazat()
            elif operation == 'выставить':
                place()                       
        uchet()
        print(tovary)
        print(prodajy_za_mesatz)
        print(prodaji_for_staticrica)
        print(prodajy_za_day)
        print(zakazy)
        print(kontracts)
        print(notis)
        while True:
            sostoyanie = input('Начать новый день? ').upper()
            if sostoyanie == 'ЭКСТРЕННОЕ ВКЛЮЧЕНИЕ':
                sostoyanie = 'ДА'
                break
            elif sostoyanie in 'ДАНЕТ':
                if sostoyanie == 'ДА':
                    dateprov = datetime.date.today()
                    if dateprov == date:
                        print('новый день не начался')
                    else:
                        break
                else:
                    break    

        
elif not(sostoyanie == 'НЕТ'):
    print('Неверный запрос')         
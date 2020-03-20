import psycopg2

def group_tabel(): #maakt de tabel aan met de users en groepen
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()
    cur.execute("DROP TABLE IF EXISTS groepen CASCADE")
    cur.execute("""CREATE TABLE groepen
                    (id VARCHAR PRIMARY KEY,
                     groep VARCHAR);""")
    c.commit()
    c.close

def pgload_group(id,group):
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()
    cur.execute("insert into groepen values (%s,%s)", (id,group,))
    c.commit()
    c.close
    print('Inserted')

def user_groups(userlist):
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()
    group_dict = {}
    count = 0 #alleen om te kijken hoe snel de tests gaan
    for user in userlist:
        count += 1
        #print('===============================')
        print(count)
        cur.execute("""select ppv.profid, ppv.prodid, prof.segment, prod.name, prod.category, prod.targetaudience
                from profiles_previously_viewed as ppv inner join profiles as prof on ppv.profid = prof.id inner join products as prod on ppv.prodid = prod.id 
                where profid =%s
                order by profid desc,
                prodid desc """, (user,))
        table = cur.fetchall()
        cat_dict = {}
        target_dict = {}
        for product in table:
            #print('\nProfId = ', product[0],'\nProdId = ', product[1],'\nSegment = ', product[2],'\nNaam = ', product[3],'\nCat = ', product[4],'\nTarget = ', product[5])
            target = product[5]
            cat = product[4]
            if target in target_dict:
                target_dict[target] +=1
            else:
                if target == None or target == 'Grootverpakking' or target == 'zwangere vrouw' or target == 'Unisex' or target == '65+' or target == 'Baby' or target == 'Mannen/vrouwen' or target == 'Vrouw':
                    pass  # slaat lege targets over en targets met maar enkele items
                else:
                    target_dict[target] = 1
            if cat in cat_dict:
                cat_dict[cat] += 1
            else:
                if cat == None or cat == 'Folder artikelen' or cat == 'op=opruiming' or cat == 'Nieuw' or cat == '50% korting' or cat == 'Opruiming' or cat == 'Cadeau ideeën':
                    pass  # slaat lege targets en cats over en targets met maar enkele items
                else:
                    cat_dict[cat] = 1
        #print('targetdict:', target_dict)
        #print('catdict:', cat_dict)
        if target_dict == {}:
            biggest_target = 'Volwassenen' #standaard, als targetdict leeg is
        else:
            biggest_target = max(target_dict, key=target_dict.get)  # verkrijg meest gekochte target
        if cat_dict == {}:
            biggest_cat = 'Gezond & verzorging' # standaard (meest gebruikt), als catdict leeg is
        else:
            biggest_cat = max(cat_dict, key=cat_dict.get)  # verkrijg meest gekochte category

        group = '{}_{}'.format(biggest_target,biggest_cat)
        #print(group)
        pgload_group(user,group)
        if group in group_dict:
            group_dict[group] += 1
        else:
            group_dict[group] = 1
    #print('',group_dict)

def userlijst():
    group_tabel()
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()
    userlist = []
    cur.execute("""select id from profiles where segment = 'buyer' or segment = 'BUYER'""")
    tabel = cur.fetchall()
    for row in tabel:
        userlist.append(row[0])
    print('lente userlijst:', len(userlist))
    user_groups(userlist)

userlijst()



"""Alles hieronder was voor het testen"""
def maak_groepen(): #test functie om groepen te maken
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()
    code1 = """select category, targetaudience from products where category != '' and targetaudience != '' AND targetaudience != 'Grootverpakking'AND targetaudience != 'zwangere vrouw'AND targetaudience != 'Unisex'AND targetaudience != '65+'AND targetaudience != 'Baby'AND targetaudience != 'Mannen/vrouwen'AND targetaudience != 'Vrouw'"""
    cur.execute(code1)
    table = cur.fetchall()
    catlist = []
    targetlist = []

    for row in table:
        cat = row[0]
        target = row[1]
        if cat not in catlist:
            catlist.append(cat)
        if target not in targetlist:
            targetlist.append(target)
    groups = []
    print(catlist)
    for target in targetlist:
        for cat in catlist:
            groep = '{}_{}'.format(target,cat)
            #print(groep)
            groups.append(groep)
    input(1)
    return groups
#maak_groepen()








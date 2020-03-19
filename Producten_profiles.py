import psycopg2


def maak_groepen():
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cursor = c.cursor()
    count = 0

    code1 = """select category, targetaudience from products where category != '' and targetaudience != '' AND targetaudience != 'Grootverpakking'AND targetaudience != 'zwangere vrouw'AND targetaudience != 'Unisex'AND targetaudience != '65+'AND targetaudience != 'Baby'AND targetaudience != 'Mannen/vrouwen'AND targetaudience != 'Vrouw'"""


    cursor.execute(code1)
    table = cursor.fetchall()
    catlist = []
    targetlist = []

    for row in table:
        cat = row[0]
        target = row[1]
        if cat not in catlist:
            catlist.append(cat)
        if target not in targetlist:
            targetlist.append(target)
        count += 1
    #print(count,'items')
    #print(catlist)
    #print('\n',targetlist)
    groups = []
    for target in targetlist:
        for cat in catlist:
            groep = '{}_{}'.format(target,cat)
            #print(groep)
            groups.append(groep)
    #print(groups)
    #print(len(catlist),len(targetlist),len(groups))
    return groups


#maak_groepen()

def user_groups(userlist):
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cursor = c.cursor()

    for user in userlist:
        print('===============================')
        cursor.execute("""select ppv.profid, ppv.prodid, prof.segment, prod.name, prod.category, prod.targetaudience
                from profiles_previously_viewed as ppv inner join profiles as prof on ppv.profid = prof.id inner join products as prod on ppv.prodid = prod.id 
                where profid =%s
                order by profid desc,
                prodid desc """, (user,))
        table = cursor.fetchall()
        cat_dict = {}
        target_dict = {}
        for product in table:
            #print('\nProfId = ', product[0],'\nProdId = ', product[1],'\nSegment = ', product[2],'\nNaam = ', product[3],'\nCat = ', product[4],'\nTarget = ', product[5])

            target = product[5]
            cat = product[4]
            if target == None or cat == None or target == 'Grootverpakking'or target == 'zwangere vrouw'or target == 'Unisex'or target == '65+'or target == 'Baby'or target == 'Mannen/vrouwen'or target == 'Vrouw':
                continue #slaat lege targets en cats over en targets met maar enkele items
            if target in target_dict:
                target_dict[target] +=1
            else:
                target_dict[target] = 1
            if cat in cat_dict:
                cat_dict[cat] += 1
            else:
                cat_dict[cat] = 1
        try:
            print('targetdict:', target_dict)
            print('catdict:', cat_dict)
            biggest_target = max(target_dict, key=target_dict.get) #verkrijg meest gekochte target
            biggest_cat = max(cat_dict, key=cat_dict.get) #verkrijg meest gekochte category
            group = '{}_{}'.format(biggest_target,biggest_cat)
            print(group)
        except ValueError:
            print('ERROOOOR')





def userlijst():
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cursor = c.cursor()
    userlist = []
    cursor.execute("""select id from profiles where segment = 'buyer' or segment = 'BUYER' limit 1000""")
    tabel = cursor.fetchall()
    for row in tabel:
        userlist.append(row[0])
    print('lente userlijst:', len(userlist))
    print(userlist)
    #input('doorgaan?')

    user_groups(userlist)

userlijst()

# ding = "5c47034ed8f58d0001706b84"








def prod_prof(userlist):
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cursor = c.cursor()

    code2 = """select ppv.profid, ppv.prodid, prof.segment, prod.name, prod.category, prod.targetaudience
        from profiles_previously_viewed as ppv inner join profiles as prof on ppv.profid = prof.id inner join products as prod on ppv.prodid = prod.id 
        where profid ='5c47034ed8f58d0001706b84'
        order by profid desc,
        prodid desc """

    input('doorgaan')
    ding = "5c47034ed8f58d0001706b84"

    cursor.execute("""select ppv.profid, ppv.prodid, prof.segment, prod.name, prod.category, prod.targetaudience
            from profiles_previously_viewed as ppv inner join profiles as prof on ppv.profid = prof.id inner join products as prod on ppv.prodid = prod.id 
            where profid =%s
            order by profid desc,
            prodid desc """,(ding,))

    table = cursor.fetchall()
    #where segment = 'buyer' or segment = 'BUYER'

    for row in table:
        count += 1
        print('\nProfId = ', row[0],'\nProdId = ', row[1],'\nSegment = ', row[2],'\nNaam = ', row[3],'\nCat = ', row[4],'\nTarget = ', row[5],'\nCount = ',count )




#prod_prof(1)

def sqlload():
    print(1)













def tabelmaken():
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123') #TODO: edit this.
    cur = c.cursor()

    cur.execute("DROP TABLE IF EXISTS products CASCADE")
    cur.execute("DROP TABLE IF EXISTS profiles CASCADE")
    cur.execute("DROP TABLE IF EXISTS profiles_previously_viewed CASCADE")
    cur.execute("DROP TABLE IF EXISTS sessions CASCADE")

    # All product-related tables

    cur.execute("""CREATE TABLE products
                    (id VARCHAR PRIMARY KEY,
                     name VARCHAR,
                     brand VARCHAR,
                     type VARCHAR,
                     category VARCHAR,
                     subcategory VARCHAR,
                     subsubcategory VARCHAR,
                     targetaudience VARCHAR,
                     msrp INTEGER,
                     discount INTEGER,
                     sellingprice INTEGER,
                     deal VARCHAR,
                     description VARCHAR);""")
#tabelmaken()
import psycopg2

def basic_zoeken():
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cursor = c.cursor()
    sql_select = "SELECT * from products"

    cursor.execute(sql_select)
    records = cursor.fetchall()
    print('Aantal rijen: ',cursor.rowcount)
    input("\nAlle rijen printen?: ")
    for row in records:
        print('\nId = ', row[0],)
        print('Naam = ', row[1],)
        print('Merk = ', row[2],)
        print('Prijs = ', row[10])

#basic_zoeken()

def prijs_zoeken():
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cursor = c.cursor()
    prijs = 49700
    #sql_select = "SELECT * from products WHERE sellingprice = (%s) ", (prijs)

    cursor.execute("SELECT * from products WHERE sellingprice = 150 ")
    records = cursor.fetchall()
    print('Aantal rijen: ',cursor.rowcount)
    input("\nAlle rijen printen?: ")
    for row in records:
        print('\nId = ', row[0],)
        print('Naam = ', row[1],)
        print('Merk = ', row[2],)
        print('Category = ', row[4])
        print('Prijs = ', row[10])

#prijs_zoeken()

def hoogste_prijs():
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cursor = c.cursor()
    sql_select = "SELECT * from products WHERE sellingprice > 0 "


    cursor.execute(sql_select)
    records = cursor.fetchall()
    aantal = cursor.rowcount
    print('Aantal rijen: ',aantal)
    input("\nAlle rijen printen?: ")

    totaal = 0
    lijst = []
    for row in records:
        prijs = row[10] / 100 #want prijs staat in centen in database
        print(prijs)
        lijst.append(prijs)
        totaal += prijs
    print('gemiddeld: ', round(totaal/aantal,2))
    print('hoogste: ', max(lijst))

#hoogste_prijs()

def join_profses():
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cursor = c.cursor()

    cursor.execute("select * from profiles where segment = 'buyer' or segment = 'BUYER' or segment = 'B'",
                   "WHERE segment = BUYER ")
    records = cursor.fetchall()
    print('Aantal rijen: ',cursor.rowcount)
    input("\nAlle rijen printen?: ")
    totaal = 0
    for row in records:
        totaal += 1
        print('\nId = ', row[0],)
        print('Naam = ', row[1],)
        print(totaal)



#join_profses()

def cat():
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cursor = c.cursor()
    sql_select = """Select * from products"""
                    #where targetaudience = 'Volwassenen'"""

    cursor.execute(sql_select)
    records = cursor.fetchall()
    print('Aantal rijen: ',cursor.rowcount)
    #input("\nAlle rijen printen?: ")
    vrouw = 0
    man = 0
    kind = 0
    volwas = 0
    baby = 0
    niks = 0
    cat = 0

    for row in records:
        print('\nId = ', row[0],)
        print('Naam = ', row[1],)
        target = row[7]
        cate = row[4]
        print('Target = ', target)
        print('cat = ',cate)

        if cate == 'Huishouden':
            cat += 1
        if target == 'Meisje':
            man += 1
        elif target == 'Vrouwen':
            vrouw += 1
        elif target == 'Kinderen':
            kind += 1
        elif target == 'Volwassenen':
            volwas += 1
        elif target == 'Baby\'s':
            baby += 1
        elif target == None:
            niks += 1

        #print('Merk = ', row[2],)
        #print('Prijs = ', row[10])
        #print('Target = ', row[7])
    print('man {}, vrouw {}, kind {}, volwas {}, baby {} totaal {}'.format(man,vrouw,kind,volwas,baby,man+vrouw+kind+volwas+baby))
    print('niks',niks, man+vrouw+kind+volwas+baby+niks)
    print('cat', cat)
cat()


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
        print('\nProfId = ', row[0],'\nProdId = ', row[1],'\nSegment = ', row[2],'\nNaam = ', row[3],'\nCat = ', row[4],'\nTarget = ', row[5],'\nCount = ' )
import psycopg2

def prod_tabel(): #maakt de tabel aan met de producten en recomendations
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()

    cur.execute("DROP TABLE IF EXISTS rec_prod CASCADE")

    cur.execute("""CREATE TABLE rec_prod
                    (prodid VARCHAR PRIMARY KEY,
                     recid VARCHAR);""")
    c.commit()
    c.close

def pgload_prodrec(prodid,recommendation):
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()
    cur.execute("insert into rec_prod values (%s,%s)", (prodid, recommendation,))
    c.commit()
    c.close
    print('Inserted')

def content(productlijst):
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()
    count = 0
    for prodid in productlijst:
        count +=1
        cur.execute("""select brand, type, category, subcategory, subsubcategory, targetaudience, name from products   
            where id =%s""",(prodid,))
        table = cur.fetchall()
        for row in table:
            brand = row[0]
            type = row[1]
            cat = row[2]
            subcat = row[3]
            subsubcat = row[4]
            target = row[5]
            name = row[6]
        #print('id: ',prodid,'naam:',name,'merk:',brand,'-type:',type,'-cat:',cat,'-subcat:',subcat,'-subsubcat:',subsubcat, '-target:',target)
        maindict = {}

        if brand is not None:
            #print('Heeft merk')
            cur.execute("""select id from products
                            where brand =%s and id !=%s""", (brand,prodid,))
            table = cur.fetchall()
            for row in table:
                if row in maindict:
                    maindict[row] += 1
                else:
                    maindict[row] = 1
        if type is not None:
            #print('Heeft type')
            cur.execute("""select id from products
                            where type =%s and id !=%s""", (type,prodid,))
            table = cur.fetchall()
            for row in table:
                if row in maindict:
                    maindict[row] += 1
                else:
                    maindict[row] = 1
        if target is not None:
            #print('Heeft target')
            cur.execute("""select id from products
                            where targetaudience =%s and id !=%s""", (target,prodid,))
            table = cur.fetchall()
            for row in table:
                if row in maindict:
                    maindict[row] += 1
                else:
                    maindict[row] = 1

        catlist = []
        if subsubcat is not None:
            #print('Heeft subsubcat')
            cur.execute("""select id from products
                where subsubcategory =%s and id !=%s""", (subsubcat,prodid,))
            table = cur.fetchall()
            for row in table:
                catlist.append(row[0])
        elif subcat is not None:
            #print('Heeft subcat')
            cur.execute("""select id from products
                            where subcategory =%s and id !=%s""", (subcat,prodid,))
            table = cur.fetchall()
            for row in table:
                catlist.append(row[0])
        else:
            #print("Heeft cat")
            cur.execute("""select id from products
                            where category =%s and id !=%s""", (cat,prodid,))
            table = cur.fetchall()
            for row in table:
                catlist.append(row[0])
        for product in catlist:
            if product in maindict:
                maindict[product] +=1
            else:
                maindict[product] = 1
        recommendation = max(maindict, key=maindict.get)

        print(prodid)
        print(recommendation)
        print(count)
        pgload_prodrec(prodid,recommendation)

def productlijst():
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()
    prod_tabel()
    prodid_list = []
    cur.execute("""select id from products where name is not null and brand is not null and category is not null """)
    table = cur.fetchall()
    for row in table:
        prodid_list.append(row[0])
    print("Productlijst = Klaar")
    content(prodid_list)

    #print(prodid_list, len(prodid_list))
productlijst()
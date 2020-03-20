import psycopg2


def recommendation_tabel(): #maakt een tabel met de recommendation per groep
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()
    cur.execute("DROP TABLE IF EXISTS rec_groep CASCADE")
    cur.execute("""CREATE TABLE rec_groep 
                    (groep VARCHAR PRIMARY KEY,
                     prodid VARCHAR);""")
    c.commit()
    c.close

def pgload_rec(groep,prodid): #laadt alle recommendations in PG
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cursor = c.cursor()
    cursor.execute("insert into rec_groep values (%s,%s)", (groep,prodid,))
    c.commit()
    c.close

def group_rec(): #maakt de recommendations
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cursor = c.cursor()
    recommendation_tabel()

    cursor.execute("""select distinct groep from groepen""")
    table = cursor.fetchall()
    groep_list = []
    for groep in table:
        groep_list.append(groep)
    for groep in groep_list:
        product_dict = {}
        cursor.execute("""select distinct ppv.profid, ppv.prodid, gr.groep
                from profiles_previously_viewed as ppv
                inner join groepen as gr on ppv.profid = gr.id
                inner join products as prod on ppv.prodid = prod.id
                where groep = %s
                order by prodid desc;""",(groep,))
        table = cursor.fetchall()
        for product in table:
            prodid = product[1]
            #print(product[0],prodid,product[2])
            if prodid in product_dict:
                product_dict[prodid] += 1
            else:
                product_dict[prodid] = 1
        #print(product_dict)
        recommendation = max(product_dict, key =product_dict.get) #meest voorkomende product
        #print(groep,'biggest: ',recommendation)
        pgload_rec(groep,recommendation)

group_rec()
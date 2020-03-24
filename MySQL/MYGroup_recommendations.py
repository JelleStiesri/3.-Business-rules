import mysql.connector as mysql
f = open("password.txt", "r")
password = f.readline()
f.close()

mydb = mysql.connect(
        host="localhost",
        user="root",
        passwd=password,
        database='webshop'
    )
mycursor = mydb.cursor()

def recommendation_tabel(): #maakt een tabel met de recommendation per groep
    mycursor.execute("DROP TABLE IF EXISTS rec_groep CASCADE")
    mycursor.execute("""CREATE TABLE rec_groep 
                    (groep VARCHAR(255) PRIMARY KEY,
                     prodid VARCHAR(255));""")
    mydb.commit()


def pgload_rec(groep,prodid): #laadt alle recommendations in PG
    mycursor.execute("insert into rec_groep values (%s,%s)", (groep,prodid,))
    mydb.commit()


def group_rec(): #maakt de recommendations
    recommendation_tabel()

    mycursor.execute("""select distinct groep from groepen""")
    table = mycursor.fetchall()
    groep_list = []
    for groep in table:
        groep_list.append(groep)
    for groep in groep_list:
        product_dict = {}
        mycursor.execute("""select distinct ppv.profid, ppv.prodid, gr.groep
                from profiles_previously_viewed as ppv
                inner join groepen as gr on ppv.profid = gr.id
                inner join products as prod on ppv.prodid = prod.id
                where groep = %s
                order by prodid desc;""",(groep,))
        table = mycursor.fetchall()
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
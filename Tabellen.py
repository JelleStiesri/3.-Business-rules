import psycopg2

def group_tabel():
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()

    cur.execute("DROP TABLE IF EXISTS groups CASCADE")

    cur.execute("""CREATE TABLE groups
                    (id VARCHAR PRIMARY KEY,
                     groep VARCHAR);""")
    c.commit()
    c.close

def recommendation_tabel():
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()

    cur.execute("DROP TABLE IF EXISTS rec_group CASCADE")

    cur.execute("""CREATE TABLE rec_group 
                    (groep VARCHAR PRIMARY KEY,
                     prodid VARCHAR);""")
    c.commit()
    c.close

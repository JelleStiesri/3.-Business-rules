import psycopg2

def collaborative():
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()
    profid = input('Geef een Klantnummer: ')
    #gebruik bijvoorbeeld: 59ddc3a2a56ac6edb4eb50e0 om te testen
    cur.execute("""select distinct gr.id, rg.groep, rg.prodid
                from rec_groep as rg
                inner join groepen as gr on rg.groep = gr.groep
                where gr.id =%s
                order by prodid desc; """,(profid,))
    table = cur.fetchall()
    for row in table:
        prodid = row[2]

    cur.execute("""select pr.name, pr.brand, pr.sellingprice
            from products as pr
            where id =%s""",(prodid,))
    table = cur.fetchall()
    print('Andere klanten kochten dit:')
    for row in table:
        print('Naam: ',row[0])
        print('Merk: ', row[1])
        print('Prijs: ', row[2]/100,'Euro')


def content():
    c = psycopg2.connect('dbname=Webshopjel user=postgres password=Pindakaas123')
    cur = c.cursor()
    prodid = input('Geef een Productnummer: ')
    # gebruik bijvoorbeeld: 32520 om te testen
    cur.execute("""select recid from rec_prod
        where prodid =%s""", (prodid,))
    table = cur.fetchall()
    for row in table:
        recid = row[0]

    cur.execute("""select pr.name, pr.brand, pr.sellingprice
                    from products as pr
                    where id =%s""", (prodid,))
    table = cur.fetchall()
    print('U kijkt nu naar:')
    for row in table:
        print('Naam: ', row[0])
        print('Merk: ', row[1])
        print('Prijs: ', row[2] / 100, 'Euro')

    cur.execute("""select pr.name, pr.brand, pr.sellingprice
                from products as pr
                where id =%s""", (recid,))
    table = cur.fetchall()
    print('==========================')
    print('U zou ook kunnen kiezen voor:')
    for row in table:
        print('Naam: ', row[0])
        print('Merk: ', row[1])
        print('Prijs: ', row[2] / 100, 'Euro')

def menu():
    keuze = int(input("1: Collaborative\n2: Content\nMaak uw keuze: "))
    print('=======================')
    if keuze == 1:
        collaborative()
    elif keuze == 2:
        content()

menu()

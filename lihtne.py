################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: Bingomäng
#
#
# Autorid: Mia Mõisnik, Elo Liisbet Palmsaar
#
# mõningane eeskuju: klassikaline numbrite jaotus vastavalt 75-pallise bingo reeglitele, 
# koodi mõningane eeskuju: https://www.geeksforgeeks.org/create-bingo-game-using-python/, mõjutanud kõige rohkem funktsiooni 'uus_number'
#
# Mängu käik:
#  Enne mängimist tuleb sisestada mängija nimi.
#  Uue numbri genereerimiseks vajutada 'enter'.
#  Mängija saab ise kontrollida, kas number on kaardil olemas ning seejärel vajutada uuesti 'enter', et kuvada uus seis.
#  Kui kaardil saadakse kokku rida või veerg, tuleb mängijal kirjutada 'bingo' ning programm lõpetab töö.
#  Muul juhul tuleb peale kaardi kuvamist vajutada uuesti 'enter'.
#
##################################################


import random


# numbri genereerimine
def uus_number(olnud_numbrid):
    kõik_numbrid = set(range(1, 76))
    numbreid_alles = kõik_numbrid - olnud_numbrid
    if numbreid_alles == {}:
        return None
    else: 
        number = random.choice(list(numbreid_alles))
        olnud_numbrid.add(number)
        return str(number)
 

# kaardi genereerimine
def bingokaart():
    kaart = [['B', 'I', 'N', 'G', 'O']]
    olnud_numbrid = set()
    for rida in range(5):
        rea_numbrid = []
        for veerg in range(5):
            if rida == 2 and veerg == 2:
                rea_numbrid.append('o')
            elif veerg == 0:
                while True:
                    number = random.randint(1, 15)
                    if number not in olnud_numbrid:
                        rea_numbrid.append(str(number))
                        olnud_numbrid.add(number)
                        break
                    else:
                        continue
            elif veerg == 1:
                while True:
                    number = random.randint(16, 30)
                    if number not in olnud_numbrid:
                        rea_numbrid.append(str(number))
                        olnud_numbrid.add(number)
                        break
                    else:
                        continue
            elif veerg == 2:
                while True:
                    number = random.randint(31, 45)
                    if number not in olnud_numbrid:
                        rea_numbrid.append(str(number))
                        olnud_numbrid.add(number)
                        break
                    else:
                        continue
            elif veerg == 3:
                while True:
                    number = random.randint(46, 60)
                    if number not in olnud_numbrid:
                        rea_numbrid.append(str(number))
                        olnud_numbrid.add(number)
                        break
                    else:
                        continue
            elif veerg == 4:
                while True:
                    number = random.randint(61, 75)
                    if number not in olnud_numbrid:
                        rea_numbrid.append(str(number))
                        olnud_numbrid.add(number)
                        break
                    else:
                        continue
        kaart.append(rea_numbrid)
    return kaart


# mängimine
def main():
    nimi = input('Mängija nimi: ')
    print(f'Tere, {nimi}! Siin on sinu bingokaart:')
    kaart = bingokaart()
    for rida in kaart:
        print('\t'.join(rida))
    
    olnud_numbrid = set()
    while True:
        input('Numbri genereerimiseks vajuta Enter')
        number = uus_number(olnud_numbrid)
        if number == None:
            print('Numbrid on otsas!')
            break
        print(f'uus number on {number}')
        
        input()
        number_oli = 0
        for i in range(1, 6):
            for j in range(5):
                if kaart[i][j] == number:
                    kaart[i][j] = 'X'
                    number_oli += 1
                    for rida in kaart:
                        print('\t'.join(rida))
        if number_oli == 0:
            print('Seis jääb samaks!')
            for rida in kaart:
                        print('\t'.join(rida))
        
        if input() == 'bingo':
            break

    
if __name__ == '__main__':
    main()

import urllib.request
import urlConstants
import mysql.connector
import json

def connectToMySql():

    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        # password="yourpassword",
        database="covid19"
    )

    return mydb

def callApi(route):
    with urllib.request.urlopen(urlConstants.BASE_URL + route) as url:
        data = json.loads(url.read().decode())
        return data

def saveSummary(summary):

    mydb = connectToMySql()

    for country in summary["Countries"]:
        ID = country["ID"]
        Country = country["Country"]
        CoutryCode = country["CountryCode"]
        Slug = country["Slug"]
        NewConfirmed = country["NewConfirmed"]
        TotalConfirmed = country["TotalConfirmed"]
        NewDeaths = country["NewDeaths"]
        TotalDeaths = country["TotalDeaths"]
        NewRecovered = country["NewRecovered"]
        TotalRecovered = country["TotalRecovered"]
        Date = country["Date"]

        mycursor = mydb.cursor()

        sql = "INSERT INTO `dailySummary`(`ID`, `Country`, `CoutryCode`, `Slug`, `NewConfirmed`, `TotalConfirmed`, `NewDeaths`, `TotalDeaths`, `NewRecovered`, `TotalRecovered`, `Date`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (ID,Country,CoutryCode,Slug,NewConfirmed,TotalConfirmed,NewDeaths,TotalDeaths,NewRecovered,TotalRecovered,Date)
        mycursor.execute(sql,val)

        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

    mydb.close()


def saveTotalFromDayOne(data):

    mydb = connectToMySql()

    for element in data:
        Country = element["Country"]
        CountryCode = element["CountryCode"]
        Province = element["Province"]
        City = element["City"]
        CityCode = element["CityCode"]
        Lat = element["Lat"]
        Lon = element["Lon"]
        Confirmed = element["Confirmed"]
        Deaths = element["Deaths"]
        Recovered = element["Recovered"]
        Active = element["Active"]
        Date = element["Date"]
        #Date = datetime.date(DateTime)
        print(Date)
        try:
            mycursor = mydb.cursor()

            sql = "INSERT INTO `totalfromdayone`(`Country`, `CountryCode`, `Province`, `City`, `CityCode`, `Lat`, `Lon`, `Confirmed`, `Deaths`, `Recovered`, `Active`, `Date`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,date(%s))"
            val = (Country, CountryCode, Province, City, CityCode, Lat, Lon, Confirmed, Deaths,
                   Recovered,Active, Date)
            mycursor.execute(sql, val)

            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except:
            print("Error during inserting into totalfromdayone")
    mydb.close()


def saveCountries(countriesData):
    mydb = connectToMySql()

    for element in countriesData:
        Country = element["Country"]
        Slug = element["Slug"]
        ISO2 = element["ISO2"]
        try:
            mycursor = mydb.cursor()

            sql = "INSERT INTO `countries`(`Country`, `Slug`, `ISO2`) VALUES (%s,%s,%s)"
            val = (Country, Slug, ISO2)
            mycursor.execute(sql, val)

            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        except:
            print("Error during inserting into totalfromdayone")
    mydb.close()

def retrieveCountryList():
    mydb = connectToMySql()
    mycursor = mydb.cursor()
    query = "SELECT Country FROM `countries` "
    print(query)
    mycursor.execute(query)

    result = mycursor.fetchall()
    mydb.close()
    return result

def updateDataForAllCountries(countries):
    try:
        for country in countries:
            totalCountry = callApi(urlConstants.TOTAL_FROM_DAY_ONE_BY_COUNTRY + country[0])
            saveTotalFromDayOne(totalCountry)
    except Exception as e:
        print("ERROR DURING updateDataForAllCountries: " + str(e))

if __name__ == '__main__':
    totalCountry = callApi(urlConstants.TOTAL_FROM_DAY_ONE_BY_COUNTRY + "France")
    saveTotalFromDayOne(totalCountry)

    totalCountry = callApi(urlConstants.TOTAL_FROM_DAY_ONE_BY_COUNTRY + "Germany")
    saveTotalFromDayOne(totalCountry)

    totalCountry = callApi(urlConstants.TOTAL_FROM_DAY_ONE_BY_COUNTRY + "Italy")
    saveTotalFromDayOne(totalCountry)
    #countries = callApi("countries")
    #saveCountries(countries)


    #START DAILY UPDATE

    #countries = retrieveCountryList()
    #print(countries[19])
    #updateDataForAllCountries(countries)

    #END DAILY UPDATE
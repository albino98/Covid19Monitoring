import urllib.request
import urlConstants
import mysql.connector
import os
from flask import Flask, render_template, request, redirect, url_for, Markup, send_from_directory
import json
import plotly
from plotly.graph_objs import Scatter, Layout
import plotly.express as px


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

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('/home.html')

def prepareDataForPlot(queryResult, plotType):
    dataDictionary = {
        "X": [],
        "Y": []
    }
    if(plotType == "incremental"):
        for x in queryResult:
            dataDictionary["X"].append(x[0])
            dataDictionary["Y"].append(x[1])
    elif(plotType == "daily"):
        #poichè la tabella totalfromdayone contiene l'incremento dei casi giornalieri (il totale dal primo giorno), faccio la sottrazione del numero di casi di ogni giorno - quella del giorno precedente,
        #per ottenere il numero dei nuovi casi giornalieri
        previousDay = ""
        for x in queryResult:
            if(previousDay != ""):
                dataDictionary["X"].append( x[0] - previousDay[0] )
            else:
                dataDictionary["X"].append(x[0])
            dataDictionary["Y"].append(x[1])
            previousDay = x
    print(dataDictionary)
    return dataDictionary

def buildExamplePlot(dataX, dataY):
    plotly.offline.plot({
        "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
        "layout": Layout(title="hello world")
    })

def buildPlot(dataX, dataY, country, dataType, chartType):
    lineColor = "#498efc"
    if dataType == "Deaths":
        lineColor = "#c21021"

    elif dataType == "Recovered":
        lineColor = "#ff9900"

    if chartType == 'bar':
        plot = plotly.offline.plot({
            "data": [plotly.graph_objs.Bar(x=dataX, y=dataY, marker=dict(color=lineColor))],
            "layout": Layout(title=country + " - Daily " + dataType, height=1000, margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            ))
        }, output_type='div'
        )
        '''
        , include_plotlyjs=False
        , output_type='div'
        '''
        return plot
    elif chartType == 'linear':
        plot = plotly.offline.plot({
            "data": [Scatter(x=dataX, y=dataY,line=dict(color=lineColor, width=2))],
            "layout": Layout(title=country + " - Total " + dataType, height=1000 ,margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            ))
        }, output_type='div'
        )
        '''
        , include_plotlyjs=False
        , output_type='div'
        '''
        return plot

def buildOnlinePlot(dataX, dataY, country, dataType):
    df = px.data.gapminder().query("country=='Canada'")
    fig = px.line(df, x=dataX, y=dataY, title=country + " - " + dataType)
    fig.show()
    return fig.show()

def retrieveDataByCountry(country, dataToRetrieve):
    mydb = connectToMySql()
    mycursor = mydb.cursor()
    query = "SELECT " + dataToRetrieve + ", Date FROM `dailysummary` WHERE CoutryCode = '" + country + "' order by Date"
    print(query)
    mycursor.execute(query)

    result = mycursor.fetchall()
    mydb.close()
    return result

def retrieveDataFromDayOneByCountry(country, field):
    print(country)
    print(field)
    mydb = connectToMySql()
    mycursor = mydb.cursor()
    query = "SELECT  " + field + " , Date FROM `totalfromdayone` WHERE Country = '" + country + "' order by Date"
    print(query)
    mycursor.execute(query)

    result = mycursor.fetchall()
    mydb.close()
    return result

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/createChart', methods=('GET', 'POST'))
def createChart():
    if request.method == 'GET':
        country = request.args.get('country')
        dataType = request.args.get('dataType')
        print(country)
        print(dataType)

        #creo il grafico di tipo plot dei dati giornalieri
        total = retrieveDataFromDayOneByCountry(str(country), str(dataType))
        dataDictionaryDaily = prepareDataForPlot(total, "daily")
        dailyPlot = buildPlot(dataDictionaryDaily["Y"], dataDictionaryDaily["X"], country, dataType, 'bar')
        #print(plot.__str__())
        dailyCasesPlotHtml = Markup(dailyPlot)

        #creo il grafico di tipo lineare con i dati totali incrementali
        dataDictionaryIncremental = prepareDataForPlot(total, "incremental")
        incrementalPlot = buildPlot(dataDictionaryIncremental["Y"], dataDictionaryIncremental["X"], country, dataType, 'linear')
        incrementalPlotHtml = Markup(incrementalPlot)
        return render_template("home.html", dailyCasesPlot=dailyCasesPlotHtml, incrementalPlot=incrementalPlotHtml)


if __name__=='__main__':
    app.env = "debug"
    app.debug = True

    app.run()
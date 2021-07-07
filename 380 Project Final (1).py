#Greg Miller, Akhil Gupta, Ryan Quigley
#ENAE380 Final Project

import selenium     ##Gets URL
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup       ##Converts html data into array data
import lxml
import pandas as pd
import time
import os
import tkinter
from tkinter import *
from PIL import ImageTk,Image 
import datetime
import numpy as np
import itertools 
import timeit
import skcriteria
from skcriteria.madm import simple
from IPython.display import display

def Initializing():

    root3 = Tk()
    root3.geometry("1500x200") 
    root3.title('Welcome!')

    root3['background'] = '#856ff8'
   
    l1 = Label(root3, text = 'How many travellers will be with you today?', bg = '#856ff8', font = ('TkHeadingFont', 11, 'bold')).grid(row = 0, column = 1)
    l2 = Label(root3, text = '                 ', bg = '#856ff8', font = "10").grid(row = 0, column = 2)
    l3 = Label(root3, text ='Where will you be travelling to?', bg = '#856ff8', font = ('TkHeadingFont', 11, 'bold')).grid(row = 0, column = 3)
    l4 = Label(root3, text ='                  ', bg = '#856ff8', font = "10").grid(row = 0, column = 4)
    l5 = Label(root3, text ='Please enter the date for your trip (mm/dd/yyyy)', bg = '#856ff8', font = ('TkHeadingFont', 11,'bold')).grid(row = 0, column = 5)
    l6 = Label(root3, text = 'Please enter the departure location for each passenger, separated by commas', bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 8, column = 1)
    l7 = Label(root3, text = 'Will you be flying First Class or Economy?', bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 8, column = 5)

    def retrieve_input():
        global passengers2
        global arrivals2
        global date2
        global departures2
        global class1
        passengers2 = entry1.get()
        arrivals2 = entry2.get()
        date2 = entry3.get()
        departures2 = entry4.get()
        class1 = entry5.get()
        root3.destroy()

    tot_passengers = StringVar()
    entry1 = Entry(root3,textvariable = tot_passengers)
    entry1.grid(row=4,column = 1)

    arr_destination = StringVar()
    entry2 = Entry(root3,textvariable = arr_destination)
    entry2.grid(row = 4, column = 3)

    date = StringVar()
    entry3 = Entry(root3,textvariable = date)
    entry3.grid(row = 4, column = 5)

    depts = StringVar()
    entry4 = Entry(root3,textvariable = depts)
    entry4.grid(row = 12, column = 1)

    class2 = StringVar()
    entry5 = Entry(root3, textvariable = class2)
    entry5.grid(row = 12, column = 5)

    button = Button(root3, text = 'Finish!', bg = 'red', activebackground = 'black', command = retrieve_input).grid(row = 14, column = 3)
    mainloop()
    departures3 = departures2.split(',')
    return departures3,arrivals2,date2,class1




def webScraper(departure,date,arrival,seat):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    allData = []
    for i in range(0,len(departure)):       #loops through the departure cities of each person in group

        price = []          #initializes arrays for all necessary information
        arrivalTime = []
        departureTime = []
        stop_num = []
        total_time = []
        airline =[]
        departure_airport = []
        arrival_airport = []
        layover_airport = []
        total_info = []
        indices = []


        arrival_edited = arrival.replace(' ','+')       #edits the format of the inputted arrival and departure cities so they can be used in the url
        departure_edited = departure[i].replace(' ','+')

        month = date[0:2]       #edits the format of the inputted date so it can be used in the url
        day = date[3:5]
        year = date[6:10]

        class_edited = class1.replace(' Class', '')

        #creates custom travelocity url to find flights pertaining to the user's inputted data
        url = 'https://www.travelocity.com/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from%3A'+departure_edited+'%2Cto%3A'+arrival_edited+'%2Cdeparture%3A'+month+'%2F'+day+'%2F'+year+'TANYT&options=cabinclass%'+class_edited+'&fromDate=11%2F16%2F2020&d1=2020-11-16&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY'

        wait_time = 2
        a=1
        while a == 1:
        #opens the url in chrome
            driver.get(url)
            time.sleep(wait_time)       #waits for webpage to fully load

            soup = BeautifulSoup(driver.page_source,'lxml')                         #pulls all of the necessary info in html format from webpage using beautiful soup module
            prices = soup.find_all('span', attrs={'class': 'full-bold no-wrap'})
            durations = soup.find_all('span', attrs={'class': 'duration-emphasis'})
            stops = soup.find_all('span', attrs={'class': 'number-stops'})
            deptimes = soup.find_all('span', attrs={'data-test-id': 'departure-time'})
            arrtimes = soup.find_all('span', attrs={'data-test-id': 'arrival-time'})
            airlines = soup.find_all('span', attrs={'data-test-id': 'airline-name'})
            flight_info = soup.find_all('div', attrs={'data-test-id': 'flight-info'})
            for div in prices:              #converts the html format into arrays that are in string formats
                price.append(div.getText())
            
            if len(price) > 1:              #if webpage does not fully load, try again and add 1 second to the wait time
                a = 0
            else:
                wait_time +=1

        for div in durations:               #loops through the list of elements matching each description, saving the inner text to a list
            total_time.append(str(div.getText()).strip())
            
        for div in stops:
            parantheses1 = str(div.getText()).find('(')
            parantheses2 = str(div.getText()).find(')')
            stop_num.append(str(div.getText())[parantheses1+1:parantheses2])

        for div in deptimes:
            departureTime.append(str(div.getText()).strip())

        for div in arrtimes:
            arrivalTime.append(str(div.getText()).strip())
        
        for div in airlines:
            airline.append(str(div.getText()).strip())

        for div in flight_info:
            total_info.append(str(div.getText()).strip())

        for i in range(0,len(total_info)):      #edits the total flight info provided into more specific arrays including departure airport, arrival airport and layover cities
            colons = []
            for k in range(0,len(total_info[i])):
                if total_info[i][k] == ':':
                    colons.append(k)
            if len(colons) < 2:
                departure_airport.append(total_info[i][0:3])
                arrival_airport.append(total_info[i][(len(total_info[i])-4):len(total_info[i])])
                instr = total_info[i].find('in')
                layover_airport.append(total_info[i][instr+3:instr+6])
            elif len(colons) == 2:
                departure_airport.append(total_info[i][colons[0]+1:(colons[0]+5)])
                arrival_airport.append(total_info[i][colons[1]+1:(colons[1]+5)])
                layover_airport.append('None')
            else:
                departure_airport.append(total_info[i][colons[0]+1:(colons[0]+5)])
                arrival_airport.append(total_info[i][colons[len(colons)-1]+1:(colons[len(colons)-1]+5)])
                layovers = ''
                for k in range(1,len(colons)-1):
                    substr = total_info[i][colons[k]:colons[k+1]]
                    instr = substr.find('in')
                    layovers = layovers + substr[instr+3:instr+6]
                    layover_airport.append(layovers)
            indices.append(i)

        new_data = pd.DataFrame({"departure-time" : departureTime,          #creates a pandas dataframe containing formatted data for the flight options for each member of the group
                            "arrival-time"  : arrivalTime,
                            "price" : price,
                            "stops" : stop_num,
                            "travel-time" : total_time,
                            "airline" : airline,
                            "departure-airport" : departure_airport,
                            "layover-airport" : layover_airport,
                            "arrival-airport" : arrival_airport,
                            "indices"   : indices
                            })
        pd.set_option('display.max_columns', None)
        allData.append(new_data)


    driver.close()
   
    def airline_values(allData0): 
        ca = []
        for k in range(0,len(departure)):
            for j in range (0,len(allData0[k]['airline'])):         ##Indexing through airline column and storing it in list
                if allData0[k]['airline'][j] not in ca:
                    ca.append(allData0[k]['airline'][j])
                else:
                    continue
        if 'Multiple Airlines' in ca:
            ca.remove('Multiple Airlines')

        ca = list(set(ca))

        return ca

    ### EXTRACTING AIRPORT COLUMN AND STORING IT
    def airport_values(allData0):
        aps = []
        for k in range(0,len(departure)):
            for j in range (0,len(allData0[k]['departure-airport'])):

                if allData0[k]['departure-airport'][j] not in aps: 
                    aps.append(allData0[k]['departure-airport'][j])         ##Indexing through both airport columns and storing in list
               
                if allData0[k]['arrival-airport'][j] not in aps:
                    aps.append(allData0[k]['arrival-airport'][j])

        apsi = []
        for u in range(0,len(aps)):
            apsi.append(aps[u].strip())                 ## Removing any unnecessary spaces
            
        aps = list(set(apsi))               

        return aps
    

    ### STORING VALUES
    def gui_selections():               ## Retrieves User Selection from the GUI

        v1 = spin1v.get()               
        v2 = spin2v.get()                               ### Getting user ranking values and creating dictionary
        v3 = spin3v.get()
        v4 = spin4v.get()
        preferences = {'Total Price': int(v1), 'Arrival Difference': int(v2), 'Total Stops': int(v3), 'Travel Time': int(v4)}


        selected_airlines = []
        for c in range(0,len(varl)):
            selected_airlines.append(varl[c].get())         ## Getting checked off airlines
        
        selected_airports = []

        for d in range(0,len(varl2)):
            selected_airports.append(varl2[d].get())        ## Getting checked off airports
        
        selections = [selected_airlines,selected_airports]


        return selections, preferences


    

    def convert_data():             ## Uses checked box data to make edits on original airline and airport lists
        selections, preferences = gui_selections()
        caf = ca
        apsf = aps
        
        excl_airlines = []
        for j in range(0,len(selections[0])):
            if selections[0][j] == 1:               ## Finding what airlines to exclude
                excl_airlines.append(ca[j])
            else:
                continue

        excl_airports = []
        for n in range(0,len(selections[1])):
                if selections[1][n] == 1:
                    excl_airports.append(aps[n])       ## Finding what airports to exclude
                else:
                    continue

        for i in range(0,len(excl_airlines)):
            caf.remove(excl_airlines[i])            ## Removing excluded airlines from original list

        for k in range(0,len(excl_airports)):
            apsf.remove(excl_airports[k])           ## Removing excluded airports from original list

        return [caf,apsf], preferences
    
    
     ## AIRLINE & AIRPORT CHECKBUTTON GUI WITH CONTINUE BUTTON

    root = Tk() 
    root.geometry("1500x1000") 
    root.title('Filtering and Preferences')         ## Filtering and Preferences GUI window characteristics
    root['background'] = '#856ff8'
   

    ca = airline_values(allData)                    ## Extracting airline and airport columns 
    aps = airport_values(allData)

    ## Creating 'columns' of GUI
    w1 = Label(root, text = '    Please rank your preferences:', bg = '#856ff8', font = ('TkHeadingFont', 11,'bold')).grid(row = 0, column = 1)
    w2 = Label(root, text = '4 being the most important and 1 being the least.', bg = '#856ff8', font = ('TkHeadingFont', 11,'bold')).grid(row = 0, column = 2)
    w3 = Label(root, text ='                                    ', bg = '#856ff8', font = "10").grid(row = 0, column = 3)
    w4 = Label(root, text ='Select all airlines and airports', bg = '#856ff8', font = ('TkHeadingFont', 11,'bold')).grid(row = 0, column = 4)
    w5 = Label(root, text ='you would like to exclude:', bg = '#856ff8', font = ('TkHeadingFont', 11,'bold')).grid(row = 0, column = 5)
    
    
    ## CREATING PREFERENCES AND RANKING SYSTEM WIDGET

    spin1v = IntVar()
    spin2v = IntVar()
    spin3v = IntVar()
    spin4v = IntVar()

    wFP = Label(root, text = 'Total flight price:',bg = '#856ff8', font = ('TkMenuFont', 10)).grid(row = 4, column = 1)
    spin1 = Spinbox(root, from_= 1, to = 4, width = 4, textvariable = spin1v).grid(row = 4, column = 2)

    wTD = Label(root, text = 'Time difference between arrivals:',bg = '#856ff8', font = ('TkMenuFont', 10)).grid(row = 5, column = 1)
    spin2 = Spinbox(root, from_= 1, to = 4, width = 4, textvariable = spin2v).grid(row = 5, column = 2)

    wNS = Label(root, text = 'Number of stops:',bg = '#856ff8', font = ('TkMenuFont', 10)).grid(row = 6, column = 1)
    spin3 = Spinbox(root, from_= 1, to = 4, width = 4, textvariable = spin3v).grid(row = 6, column = 2)

    wTT = Label(root, text = 'Total travel time:',bg = '#856ff8', font = ('TkMenuFont', 10)).grid(row = 7, column = 1)
    spin4 = Spinbox(root, from_= 1, to = 4, width = 4, textvariable = spin4v).grid(row = 7, column = 2)



    ## CREATING AIRLINE AND AIRPORT CHECKBUTTON EXCLUSION WIDGET 

    varl = []
    for a in range(0,len(ca)):
        var = IntVar()
        varl.append(var)
    
    for x in range(0,len(ca)):
        Checkbutton(root, bg = '#856ff8', text = ca[x],  variable = varl[x], onvalue = 1, offvalue = 0, height = 2, width = 20).grid(row = x+3, column = 4, sticky = W)
        
 
    varl2 = []
    for p in range(0,len(aps)):
         var2 = IntVar()
         varl2.append(var2)

    if len(aps) > 12:

        for n in range(0,12):
            Checkbutton(root, bg = '#856ff8', text = aps[n],  variable = varl2[n], onvalue = 1, offvalue = 0, height = 2, width = 20).grid(row = n+3, column = 5, sticky = W)
    
        for k in range(12,len(aps)):
            Checkbutton(root, bg = '#856ff8', text = aps[k],  variable = varl2[k], onvalue = 1, offvalue = 0, height = 2, width = 20).grid(row = k-9, column = 6, sticky = W)    
    else:

        for j in range(0,len(aps)):
            Checkbutton(root, bg = '#856ff8', text = aps[j],  variable = varl2[j], onvalue = 1, offvalue = 0, height = 2, width = 20).grid(row = j+3, column = 5, sticky = W)

    
    F = tkinter.Button(root, text = 'Finish', bg = 'white', activebackground = 'black', command = root.destroy).grid(row = 14, column = 3)
    

    
    root.mainloop()

    for t in range(0,len(allData)):                         ## Edits original dataframe so that airport columns do not have any unnecessary spaces in each term

        for u in range(0,len(allData[t]['departure-airport'])):  
            allData[t]['departure-airport'] = allData[t]['departure-airport'].replace(allData[t]['departure-airport'][u],allData[t]['departure-airport'][u].strip())
        for z in range(0,len(allData[t]['arrival-airport'])):
            allData[t]['arrival-airport'] = allData[t]['arrival-airport'].replace(allData[t]['arrival-airport'][z],allData[t]['arrival-airport'][z].strip())

    selections, preferences = convert_data()

    return selections,preferences,allData


    

def price_array(data):      ##Takes in prices of filtered data set and stores each price array in a price matrix
    prices_array = []
    prices_matrix = []
    for i in range(0,len(data)):
        price = data[i].get("price")
        for k in range(0,(len(price)-1)):
            if len(price.iloc[k][1::]) > 3:
                prices_array.append(int(price.iloc[k][1::].replace(',','')))
            else:
                prices_array.append(int(price.iloc[k][1::]))
        prices_matrix.append(prices_array)
        prices_array = []
    return prices_matrix

def gen_stops_matrix(data):   ##Takes in number of stops of filtered data set and stores data in a readable matrix
    stops_array = []
    stops_matrix = []
    no_stop_count = 0
    for i in range(0,len(data)):
        stop = data[i].get("stops")
        for k in range(0,len(stop)-1):
            if stop.iloc[k][0] != "N":
                stops_array.append(int(stop.iloc[k][0]))
            else:
                stops_array.append(0)
                no_stop_count+=1
        stops_matrix.append(stops_array)
        stops_array = []
    return stops_matrix

def gen_arr_time_matrix(data):    #reads in the full dictionary, and creates a collection of arrays that contain datetime objects for the arrival time of the flight
    arr_time_array = []
    arr_time_matrix = []
    for i in range(0,len(data)):
        arr_time = data[i].get("arrival-time")
        for k in range(0,len(arr_time)-1):
            arr_time_array.append(datetime.datetime.strptime(str(arr_time.iloc[k]), '%I:%M%p'))
        arr_time_matrix.append(arr_time_array)
        arr_time_array = []
    return arr_time_matrix

def gen_travel_time_matrix(data):       #reads in the full dictionary, and creates a collection of arrays that contain the integer value of the number of mins in the flight
    travel_time_array = []
    travel_time_matrix = []
    for i in range(0,len(data)):
        travel_time = data[i].get("travel-time")
        for k in range(0,len(travel_time)-1):
            hour_index = str(travel_time.iloc[k]).find('h')
            hour = int(str(travel_time.iloc[k])[0:(hour_index)])
            min_index = str(travel_time.iloc[k]).find('m')
            if str(travel_time.iloc[k])[min_index-2] == ' ':
                minute = int(str(travel_time.iloc[k])[min_index-1])
            else:
                minute = int(str(travel_time.iloc[k])[(min_index-2):(min_index)])
            travel_time2 = (60*hour) + minute     
            travel_time_array.append(travel_time2)               
        travel_time_matrix.append(travel_time_array)
        travel_time_array = []
    return travel_time_matrix

def gen_indices_matrix(data):       #reads in the full dictionary, and stores indice values of filtered dataset
    indices_array = []
    indices_matrix = []
    for i in range(0,len(data)):
        indices = data[i].get("indices")
        for k in range(0,len(indices)-1):
            indices_array.append(indices.iloc[k])
        indices_matrix.append(indices_array)
        indices_array = []
    return indices_matrix

def gen_master(prices_matrix):                      ## Generates matrix of tuples of every possible combination
    matrix = list(itertools.product(*prices_matrix))        
    return matrix
    
def sort_prices(prices_master):                 ## Returns total value of each tuple in price matrix
    tot = 0
    tot_prices = []
    for i in range(0,len(prices_master)):
        tot = 0
        for k in range(0,len(prices_master[i])):
            tot = tot + prices_master[i][k]
        tot_prices.append(tot)
    return tot_prices

def sort_stops(stops_master):           ## Returns total value of each tuple in stop matrix
    tot = 0
    tot_stops = []
    for i in range(0,len(stops_master)):
        tot = 0
        for k in range(0,len(stops_master[i])):
            tot = tot + stops_master[i][k]
        tot_stops.append(tot)
    return tot_stops

def sort_arr_times(arr_time_master):            ## Returns total value of each tuple in arrival time matrix
    tot_arr_time = []
    for i in range(0,len(arr_time_master)):
        max_arrival = max(arr_time_master[i])
        min_arrival = min(arr_time_master[i])
        diff = ((max_arrival-min_arrival).total_seconds())/60
        tot_arr_time.append(diff)
    return tot_arr_time

def sort_travel_times(travel_times_master):     ## Returns total value of each tuple in sort arrival time matrix
    tot = 0 
    tot_travel_times = []
    for i in range(0,len(travel_times_master)):
        tot = 0
        for k in range(0,len(travel_times_master[i])):
            tot = tot + travel_times_master[i][k]
        tot_travel_times.append(tot)
    return tot_travel_times

def show_flights(indices,data):
    for i in range(0,len(indices)):
        for k in range(0,len(indices[i])):
            print(data[k].loc[indices[i][k]])

def sort(sorted_data,weights2,indices_master):      #sorts each of the individual passenger's flights
    criteria_data = skcriteria.Data(
        sorted_data,
        [min, min, min, min],
        anames = indices_master,
        cnames = sorted_data.columns,
        weights = weights2
    )
    dm  = simple.WeightedProduct(mnorm="sum",wnorm="sum")
    dec = dm.decide(criteria_data) 
    rankings = dec.rank_
    scores = dec.e_.points
    indices = []
    skindices = []
    top_scores = []
    for i in range(0,len(rankings)):
        if int(rankings[i]) < 4:
            indices.append(indices_master[i])
            skindices.append(i)
            top_scores.append(scores[i])
    return top_scores,indices,skindices

def sort2(sorted_data,weights3,indices_master,chunk_size):      #sorts all of the cobinations of the top flights
    criteria_data = skcriteria.Data(
        sorted_data,
        [min, min, min],
        anames = indices_master,
        cnames = sorted_data.columns,
        weights = weights3
    )
    dm  = simple.WeightedProduct(mnorm="sum",wnorm="sum")
    dec = dm.decide(criteria_data) 
    rankings = dec.rank_
    scores = dec.e_.points
    indices = []
    skindices = []
    top_scores = []
    for i in range(0,len(rankings)):
        if int(rankings[i]) < chunk_size:
            indices.append(indices_master[i])
            skindices.append(i)
            top_scores.append(scores[i])
    return top_scores,indices
    
def mergeSort(alist):
    """
    Insert descriptions here. Make sure to comment this code thoroughly.
    """
    if len(alist)>1:    #splits the list in half and calls merge sort on each sub array
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):     #prints sorted sub sets in temporary arrays
            if lefthalf[i] <= righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
    return alist[-4:-1]



def filter_pandas(a,allData1):      ## Filters original dataframe based on airline and airport selections
    
    allData_filtered = []               ## Looks for airlines and airports which are to be included and adds to filtered dataframe
    for i in range(0,len(allData1)): 
        airlines_filtered = allData1[i][allData1[i]['airline'].isin(a[0])]          
        arrival_airport_filtered = airlines_filtered[airlines_filtered['arrival-airport'].isin(a[1])]
        departure_airport_filtered = arrival_airport_filtered[arrival_airport_filtered['departure-airport'].isin(a[1])]
        allData_filtered.append(departure_airport_filtered)

    return allData_filtered

def search():                                                      # Pulls in all the variables needed to generate the final outputs
    def Outputting(option1,option2,option3,data,final_indices):
        global data_tk
        global final_indices_tk
        data_tk = data
        final_indices_tk = final_indices
        def option1_selected():                                                 # Sets up the functions that are called to display the top 3 flights
            for i in range(0,len(data)):
                display(data_tk[i].iloc[final_indices_tk[0][i]])
        def option2_selected():
            for j in range(0,len(data)):
                display(data_tk[i].iloc[final_indices_tk[1][j]])
        def option3_selected():
            for k in range(0,len(data)):
                display(data_tk[i].iloc[final_indices_tk[2][k]])

        root2 = Tk()                                                            # Builds tkinter window and all entries needed to display the final results

        root2.title('Final Flight Choices')
        root2.geometry('750x200')
        root2['background'] = '#856ff8'

        l1 = tkinter.Label(root2, text = '          ', bg = '#856ff8', font = ('TkHeadingFont', 11, 'bold')).grid(row = 0, column = 1)
        l2 = tkinter.Label(root2, text = 'Total Cost', bg = '#856ff8', font = ('TkHeadingFont', 11, 'bold')).grid(row = 0, column = 2)
        l3 = tkinter.Label(root2, text ='Total Stops', bg = '#856ff8', font = ('TkHeadingFont', 11, 'bold')).grid(row = 0, column = 3)
        l4 = tkinter.Label(root2, text ='Travel Time', bg = '#856ff8', font = ('TkHeadingFont', 11, 'bold')).grid(row = 0, column = 4)
        l5 = tkinter.Label(root2, text ='Arrival Time Difference', bg = '#856ff8', font = ('TkHeadingFont', 11,'bold')).grid(row = 0, column = 5)
        l6 = tkinter.Label(root2, text = 'Option 1', bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 4, column = 1)
        l7 = tkinter.Label(root2, text = option1['total-prices'], bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 4, column = 2)
        l8 = tkinter.Label(root2, text = option1['total-stops'], bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 4, column = 3)
        l9 = tkinter.Label(root2, text = option1['total-travel-time'], bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 4, column = 4)
        l10 = tkinter.Label(root2, text = option1['time-difference'], bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 4, column = 5)
        l11 = tkinter.Label(root2, text = 'Option 2', bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 8, column = 1)
        l12 = tkinter.Label(root2, text = option2['total-prices'], bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 8, column = 2)
        l13 = tkinter.Label(root2, text = option2['total-stops'], bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 8, column = 3)
        l14 = tkinter.Label(root2, text = option2['total-travel-time'], bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 8, column = 4)
        l15 = tkinter.Label(root2, text = option2['time-difference'], bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 8, column = 5)
        l16 = tkinter.Label(root2, text = 'Option 3', bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 12, column = 1)
        l17 = tkinter.Label(root2, text = option3['total-prices'], bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 12, column = 2)
        l18 = tkinter.Label(root2, text = option3['total-stops'], bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 12, column = 3)
        l19 = tkinter.Label(root2, text = option3['total-travel-time'], bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 12, column = 4)
        l20 = tkinter.Label(root2, text = option3['time-difference'], bg = '#856ff8', font  = ('TkHeadingFont', 11, 'bold')).grid(row = 12, column = 5)

        # Buttons take the individual flight data associated with each option and display them in the terminal
        button = tkinter.Button(root2, text = 'Select', bg = 'red', activebackground = 'black', command = option1_selected).grid(row = 4, column = 6)
        button2 = tkinter.Button(root2, text = 'Select', bg = 'red', activebackground = 'black', command = option2_selected).grid(row = 8, column = 6)
        button3 = tkinter.Button(root2, text = 'Select', bg = 'red', activebackground = 'black', command = option3_selected).grid(row = 12, column = 6)
        root2.mainloop()


    start = timeit.default_timer()          #start a timer to measure runtime of algorithm
    prices_matrix = price_array(filtered_data)       #create a list of arrays that contains the prices, formatted as integers, for each flight for each passenger. 
    stops_matrix = gen_stops_matrix(filtered_data)   #create a list of arrays that contains the stops, formatted as integers, for each flight for each passenger. 
    arr_time_matrix = gen_arr_time_matrix(filtered_data)     #create a list of arrays that contains the arrival times, formatted as datetime objects, for each flight for each passenger. 
    travel_times_matrix = gen_travel_time_matrix(filtered_data)  #create a list of arrays that contains the total travel time, formatted as float, for each flight for each passenger. 
    indices_matrix = gen_indices_matrix(filtered_data)           #create a list of arrays that contains the indices, formatted as integers, where each of the other criteria is contained. 

    flight_count = len(prices_matrix)
    inverse = pow(flight_count,-1)
    chunk_size = int(pow(100000,inverse))

    weights2 = []                                           #create an array for the weights that each user places on the criteria, then exponentiate it in a way that magnifies its importance
    weights2.append(pow(int(weights['Total Price']),3))
    weights2.append(pow(int(weights['Arrival Difference']),3))
    weights2.append(pow(int(weights['Total Stops']),3))
    weights2.append(pow(int(weights['Travel Time']),3))

    weights3 = []
    weights3.append(pow(int(weights['Total Price']),2))
    weights3.append(pow(int(weights['Total Stops']),2))
    weights3.append(pow(int(weights['Travel Time']),2))


    bar['value'] += 20      ## Indexes progress and percent
    progress.update_idletasks()

    all_indices = []                                        #weighs all of the flight data for each passenger individually and finds the top flights for each passenger
    for i in range(0,len(prices_matrix)):
        sorted_data = pd.DataFrame({"total-prices" : prices_matrix[i],
                            "total-stops" : stops_matrix[i],
                            "total-travel-time" : travel_times_matrix[i],
                                    })
        scores,indices = sort2(sorted_data,weights3,indices_matrix[i],chunk_size)
        all_indices.append(indices)                             #saves the indices of where the top scoring flights are in the original dataframe

    prices_subset = []                  #initializes arrays for subsets of the data based on the top scores from the first sort
    stops_subset = []
    arr_time_subset = []
    total_time_subset = []
    indices_subset = []

    bar['value'] += 20      ## Indexes progress and percent
    progress.update_idletasks()
    
    for i in range(0,len(all_indices)):     #for each passenger 
        prices = []             #initialize smaller arrays for each passenger
        stops = []
        arrTime = []
        totalTime = []
        indices2 = []
        for k in range(0,len(all_indices[i])-1):        #finds the values for each of the top scoring flights
            prices.append(prices_matrix[i][all_indices[i][k]])
            stops.append(stops_matrix[i][all_indices[i][k]])
            arrTime.append(arr_time_matrix[i][all_indices[i][k]])
            totalTime.append(travel_times_matrix[i][all_indices[i][k]])
            indices2.append(all_indices[i][k])

        indices_subset.append(indices2)                 #creates new arrays containing only the data that yielded the higher rankings
        prices_subset.append(prices)
        stops_subset.append(stops)
        arr_time_subset.append(arrTime)
        total_time_subset.append(totalTime)

    bar['value'] += 20      ## Indexes progress and percent
    progress.update_idletasks()

    prices_master = gen_master(prices_subset)           #finds all of the combinations of the top individual flights and formats them into totals or differences
    sorted_prices = sort_prices(prices_master)

    stops_master = gen_master(stops_subset)
    sorted_stops = sort_stops(stops_master)


    arr_time_master = gen_master(arr_time_subset)
    sorted_arr_times = sort_arr_times(arr_time_master)

    bar['value'] += 20      ## Indexes progress and percent
    progress.update_idletasks()

    travel_times_master = gen_master(total_time_subset)
    sorted_travel_times = sort_travel_times(travel_times_master)

    minimum_travel_times = min(sorted_travel_times)         #keeps track of the absolute minimums in each category to compare to values of top scoring flight combinations
    minimum_arr_times = min(sorted_arr_times)
    minimum_stops = min(sorted_stops)
    minimum_price = min(sorted_prices)

    indices_master = gen_master(indices_subset)         ## Indices of each tuple

    sorted_data2 = pd.DataFrame({"total-prices" : sorted_prices,            #creates a new pandas dataframe of around 100,000 rows 
                        "time-difference"  : sorted_arr_times,
                        "total-stops" : sorted_stops,
                        "total-travel-time" : sorted_travel_times,
                                })
    final_scores,final_indices,skindices = sort(sorted_data2,weights2,indices_master)   #weighs and ranks all of these options to find the top scoring combinations of these flights out of 100,000

    top_index1 = final_scores.index(final_scores[0])            #where the top 3 scores are held in original flight data
    top_index2 = final_scores.index(final_scores[1])
    top_index3 = final_scores.index(final_scores[2])

    option1 = sorted_data2.loc[skindices[top_index1]]           #stores the top ranking totals for prices, stops, difference between arrival time and total travel time
    option2 = sorted_data2.loc[skindices[top_index2]]
    option3 = sorted_data2.loc[skindices[top_index3]]

    print('Min arrival Time:',minimum_arr_times)            #prints out the minimum values of each criteria to compare to weighted products
    print('Min stops:',minimum_stops)
    print('Min price:',minimum_price)
    print('Min travel time:',minimum_travel_times)
    stop = timeit.default_timer()                       
    print('Algorithm Runtime:',stop-start)

    bar['value'] += 20      ## Indexes progress and percent
    progress.update_idletasks()

    progress.destroy()  ###
    Outputting(option1,option2,option3,filtered_data,final_indices)             #passes the top options and data to the UI function for outputting

departure,arrival,date,class1 = Initializing()
data,weights,allData = webScraper(departure,date,arrival,class1)


check = False 
check2 = False
while check == False:
    check2 = False
    if data[0] != [] and data[1] != []:         ## Check to make sure that there are no empty dataframes if a user accidentally excluded too many airlines/airports

        global filtered_data                    ## Create global variable for later use in 'search' function
        filtered_data = filter_pandas(data,allData)
        
        for k in range(0,len(filtered_data)):
            if filtered_data[k].empty == True:  ## Second check for filtered data
                check2 = True

        if check2 == True:                  ## Creating an error message that will prompt user to restart the entire webscraping program
            root2 = Tk()
            root2.title('Error')            
            root2.geometry("300x50")
            ws2 = Label(root2, text = 'Please choose different exclusions!').pack()
            R2 = tkinter.Button(root2, text = 'Restart', bg = 'white', activebackground = 'black', command = root2.destroy).pack(side = BOTTOM)

            root2.mainloop()

            data,weights,allData = webScraper(departure,date,arrival,class1)
            check = False
            continue
        
        else:
            check = True
            break

    elif data[0] == [] or data[1] == []:        ## If user decides to exclude all airports or airlines....
        root3 = Tk()
        root3.title('Error')
        root3.geometry("300x100")
        ws2 = Label(root3, text = 'Please do not exclude all airports or airlines!').pack()
        R = tkinter.Button(root3, text = 'Restart', bg = 'white', activebackground = 'black', command = root3.destroy).pack(side = BOTTOM)
        
        root3.mainloop()

        data,weights,allData = webScraper(departure,date,arrival,class1)
        check = False
        continue

from tkinter.ttk import *

### Implementation of progress bar and percent label in the program
progress = Tk()
progress.title('Compiling best results..')
progress.geometry("300x100")
percent = StringVar()


bar = Progressbar(progress,orient = HORIZONTAL, length = 300)
bar.pack(pady = 10)

percentLabel = Label(progress, textvariable = percent).pack()

button = Button(progress,text = 'Search', command = search).pack()
progress.mainloop()
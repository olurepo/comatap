from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Sensor, Data, TestConfig, Maturity_Data, Strength_Data
from projects.models import Project
from .forms import MaturityForm

import plotly.graph_objs as go 
import plotly.offline as ply


import urllib.request
import json
import numpy as np
import time
import datetime



def get_data(request, pk):
    sensor = Sensor.objects.get(pk=pk)
    project_id = sensor.project.id
    sensor_id = sensor.id

    sensorDB_name = 'sensor'+str(sensor.id)  # e.g. sensor1, sensor2...

    sensorAPI = "https://concrete-maturity.000webhostapp.com/api/"+sensorDB_name+"/read_all.php"

    response = urllib.request.urlopen(sensorAPI, timeout=10).read()
    json_obj = str(response, 'utf-8')
    raw_data = json.loads(json_obj)
    

    timeList = []   # these lists may be useful elsewhere
    tempList = []
    humList = []

    existing_data = Data.objects.filter(sensor=sensor)
    row_count = int(len(existing_data))

    if row_count==0:
        for item in raw_data[sensorDB_name]:   # the 'raw_data' json file from the server
            print(sensor_id)
            temperature = item['temp']
            tempList.append(temperature)
            log_time = (item['log_time'])
            #convert_time = np.datetime64(log_time).astype('float')
            timeList.append(log_time)
            humidity = item['hum']      # remember DUMMY humidity data
            humList.append(humidity)

            save_data = Data(time_taken=log_time, ave_temp=float(temperature), ave_hum=float(humidity), sensor_id=sensor_id)
            save_data.save()

    elif row_count!=0:
        for column in existing_data:
            unique_id = column.sensor_id

            if sensor_id == unique_id:   # confirm first that it is same sensor_id
                
                if len(existing_data)==len(raw_data[sensorDB_name]):     #sensorDB_name has been defined in 'def '
                    print("Database is up-to-date!")

                elif len(existing_data) < len(raw_data[sensorDB_name]):
                    #print("There are " + str(len(raw_data[sensorDB_name][row_count:])) + " lines of fresh data...database update required!")
                    update_data = raw_data[sensorDB_name][row_count:]   # outstanding data from the database
                    for item in update_data:
                        temperature = item['temp']
                        tempList.append(temperature)
                        log_time = (item['log_time'])
                        #convert_time = np.datetime64(log_time).astype('float')
                        timeList.append(log_time)
                        humidity = item['hum']      # remember DUMMY humidity data
                        humList.append(humidity)
                        
                        save_data = Data(time_taken=log_time, ave_temp=float(temperature), ave_hum=float(humidity), sensor_id=sensor_id)
                        save_data.save()
                else:
                    print('Check the list of data in the sever and your local database!')   # can be removed
    
    msg = messages.success(request, f'Update successful. Please confirm test configuration parameters.')

    context = {
        'msg': msg,
        'sensor': sensor,
    }

    return render(request, 'sensors/configuretest.html', context)


#def warning_messages(request):          
        

datum_temp = -10
activation_energy = 40000
gas_constant = 8.314
ref_temp = 23
ultimate_strength = 50 # N/sq.mm
a = 4.0
b = 0.85

def combined_data(request, pk):

    global datum_temp
    global activation_energy
    global gas_constant
    global ref_temp
    global ultimate_strength
    global a
    global b

    # get method, i.e. create form to get params
    form = MaturityForm()

    #do a post and receive data command
    form = MaturityForm(request.POST)
    if form.is_valid():
        datum_temp = form.cleaned_data['datum_temp']
        activation_energy = form.cleaned_data['activation_energy']
        gas_constant = form.cleaned_data['gas_constant']
        ref_temp = form.cleaned_data['ref_temp']
        ultimate_strength  = form.cleaned_data['ultimate_strength']
        a = form.cleaned_data['a']
        b = form.cleaned_data['b']
        print(datum_temp*2)
    else:
        form = MaturityForm() # repeat get command

    tim = []
    temp = [0]
    hum = [0]

    sensor = Sensor.objects.get(pk=pk)
    project_id = sensor.project.id
    sensor_id = sensor.id

    data = Data.objects.filter(sensor=sensor)

    # get all the available data on this sensor
    xList = []
    for item in data:

        log_time = item.time_taken         # time data in np.datetime64
        convert_time = np.datetime64(log_time).astype('float')
        xList.append(convert_time/(3600000000))  # in 'hours'
        #xList.append(convert_time/(3600000000*24))  # to convert age to 'days', multiply by 24
        dt = round(xList[-1] - xList[0], 2)     # time interval btw temp records
        tim.append(dt)
        

        tmp = item.ave_temp     # temperature data
        temp.append(tmp)

        humid = item.ave_hum    # humidity data
        hum.append(humid)


    plot_hum = go.Scatter(dict(x=tim, y=hum, name='humidity', marker={'color': 'blue', 'symbol': 104, 'size': 10}, mode="lines"))
    plot_temp = go.Scatter(dict(x=tim, y=temp, name="temperature", marker={'color': 'red', 'symbol': 104, 'size': 10}, mode="lines"))
    
    data = go.Data([plot_hum, plot_temp])
    layout=go.Layout(title="Concrete Temperature & Humidity Graph", xaxis={'title':'Age (hr)'}, yaxis={'title':'Temperature (C)'})
    figure=go.Figure(data=data,layout=layout)
    temp_graph = ply.plot(figure, auto_open=False, output_type='div')
    

    delta_t = [y-x for x,y in zip(tim, tim[1:])]
    matu = [0]
    for time_int, ave_temp in zip(delta_t, temp):
        M = round(float(ave_temp - datum_temp)*time_int, 2)  # this calculates maturity
        matu.append(M)

    maturity_index = np.round([sum(matu[:i + 1]) for i in range(len(matu))], 2)
    current_maturity = maturity_index[-1] # get last M value to display on results' page
    #current_maturity = matu[-1]
    
    plot_maturity = go.Scatter(dict(x=tim, y=maturity_index, name='Concrete Maturity', marker={'color': 'grey', 'symbol': 104, 'size': 10}, mode="lines"))
    data = go.Data([plot_maturity])
    layout=go.Layout(title="Concrete Maturity Graph", xaxis={'title':'Age (hr)'}, yaxis={'title':'Maturity Index (C-hr)'}, showlegend=True)
    figure=go.Figure(data=data,layout=layout)

    maturity_graph = ply.plot(figure, auto_open=False, output_type='div')

    

   # tim = get_data(sensor_id)[0]
   # temp = get_data(sensor_id)[1]
    age = []                # age on x-axis
    equiv_strength = []     # strength on y-axis

    B = -1 / (activation_energy / gas_constant)  # temperature sensitivity constant
    
    equiv_age = [] # captures age at each average temperature
    for ave_temp in temp:
        eq_age = np.exp(B * (ave_temp - ref_temp)) # see constants at the top (ref.: )
        equiv_age.append(eq_age/24)  

        sum_age = np.round([sum(equiv_age[:i + 1]) for i in range(len(equiv_age))], 2)
        age.append(sum_age[-1])
    
    for predicted_age in age:
        predict_strength = (predicted_age/(a + b*predicted_age))*ultimate_strength  # F = (t/a+bt)*fc'
        equiv_strength.append(predict_strength)
    current_strength = round(equiv_strength[-1], 2)

    plot_strength = go.Scatter(dict(x=age, y=equiv_strength, name='Strength (MPa)', marker={'color': 'brown', 'symbol': 104, 'size': 10}, mode="lines"))
    data = go.Data([plot_strength])
    layout=go.Layout(title="Concrete Strength Graph", xaxis={'title':'Age (days)'}, yaxis={'title':'Concrete Strength (Mpa)'}, showlegend=True)
    figure=go.Figure(data=data,layout=layout)
    strength_graph = ply.plot(figure, auto_open=False, output_type='div')
            
    context = {
        'temp_graph': temp_graph,
        'maturity_graph': maturity_graph,
        'data': Data.objects.last(),
        'current_maturity': current_maturity,
        #'strength_graph': strength_graph, # NEWLY ADDED 
        #'current_strength': current_strength, #NEWLY ADDED
        'matu': matu,
        'maturity_index': maturity_index,
        'sensor': sensor,
        'form': form,
        }
    
    # ====== Save Maturity Data to DB  ======= #
    existing_maturity = Maturity_Data.objects.filter(sensor=sensor)
    counted_mat_row = int(len(existing_maturity))

    if counted_mat_row == 0:    # meaning there are NO previous data
        for d_age, d_maturity in zip(dt, maturity_index):   # maturity_index is the cumulative maturity index value
            maturity_value = Maturity_Data(equivalent_age=d_age, matu_index=d_maturity, sensor_id=sensor_id)
            maturity_value.save()

    elif counted_mat_row != 0:   # meaning there are existing data
        for items in existing_maturity:
            unique_id = items.sensor_id

            if sensor_id == unique_id:   # confirm first that it is same sensor_id (see sensor_id definition above)
                
                if counted_mat_row == len(maturity_index):
                    pass    # no need for any action
                    # line below fits best but it will come up several times as the for loop
                    messages.info(request, f'NOTE: There are no recent changes to Maturity-Index database.')
                
                elif counted_mat_row < len(maturity_index):
                    outstanding_maturity = maturity_index[counted_mat_row:]
                    outstanding_age = dt[counted_mat_row:]
                    Maturity_Data.objects.filter(sensor=sensor).delete()
                    for update_age, update_maturity in zip(outstanding_age, outstanding_maturity):
                        updated_values = Maturity_Data(equivalent_age=update_age, matu_index=update_maturity, sensor_id=unique_id)
                        updated_values.save()
    else:
        messages.warning(request, f'Check the list of data for {sensor.sensor_name} in the sever and/or your local database')

    # ========= END: Save Maturity Data ========= #

    # ====== Save Strength Data to DB  ======= #
    existing_strength = Strength_Data.objects.filter(sensor=sensor)
    counted_str_row = int(len(existing_strength))

    if counted_str_row == 0:    # meaning there are NO previous data
        for d_age, d_strength in zip(age, equiv_strength):
            strength_value = Strength_Data(concrete_age=d_age, concrete_strength=d_strength, sensor_id=sensor_id)
            strength_value.save()

    elif counted_str_row != 0:   # meaning there are existing data
        for items in existing_strength:
            unique_id = items.sensor_id

            if sensor_id == unique_id:   # confirm first that it is same sensor_id (see sensor_id definition above)
                
                if counted_str_row == len(equiv_strength):
                    pass    # no need for any action becos there are no new data
                
                elif counted_str_row < len(equiv_strength):
                    outstanding_strength = equiv_strength[counted_str_row:]
                    outstanding_age = age[counted_str_row:]     # 'age' is defined at the top
                    Strength_Data.objects.filter(sensor=sensor).delete()
                    for update_age, update_strength in zip(outstanding_age, outstanding_strength): 
                        updated_values = Strength_Data(concrete_age=update_age, concrete_strength=update_strength, sensor_id=unique_id)
                        updated_values.save()
    else:
        messages.warning(request, f'Check the list of data for {sensor.sensor_name} in the sever and/or your local database')
    # ========= END: Save Strength Data ========= #


    return render(request, 'sensors/combined_data.html', context)



def Strength(request, pk):
    sensor = Sensor.objects.get(pk=pk)
    project_id = sensor.project.id
    sensor_id = sensor.id

    age = []
    equiv_strength = []

    data = Strength_Data.objects.filter(sensor=sensor)
    
    for items in data:
        d_age = items.concrete_age
        age.append(d_age)
        d_strength = items.concrete_strength
        equiv_strength.append(d_strength)

    plot_strength = go.Scatter(dict(x=age, y=equiv_strength, name='Strength (MPa)', marker={'color': 'brown', 'symbol': 104, 'size': 10}, mode="lines"))
    graph_data = go.Data([plot_strength])
    layout=go.Layout(title="Concrete Strength Graph", xaxis={'title':'Age (days)'}, yaxis={'title':'Concrete Strength (Mpa)'}, showlegend=True)
    figure=go.Figure(data=graph_data,layout=layout)
    strength_graph = ply.plot(figure, auto_open=False, output_type='div')

    last_data = data.last()
    current_strength = round(float(last_data.concrete_strength), 2)
    print(current_strength)

    context = {
        'strength_graph': strength_graph,
        'current_strength': current_strength,
        'sensor': sensor,
        }
    
    return render(request, 'sensors/Strength.html', context)


def Maturity(request, pk):
    sensor = Sensor.objects.get(pk=pk)
    project_id = sensor.project.id
    sensor_id = sensor.id

    age = []
    maturity_index = []

    data = Maturity_Data.objects.filter(sensor=sensor)
    
    for items in data:
        d_age = items.equivalent_age
        age.append(d_age)
        d_maturity = items.matu_index
        maturity_index.append(d_maturity)

    
    plot_maturity = go.Scatter(dict(x=age, y=maturity_index, name='Concrete Maturity Index', marker={'color': 'grey', 'symbol': 104, 'size': 10}, mode="lines"))
    graph_data = go.Data([plot_maturity])
    layout=go.Layout(title="Concrete Maturity Graph", xaxis={'title':'Age (hr)'}, yaxis={'title':'Maturity Index (C-hr)'}, showlegend=True)
    figure=go.Figure(data=graph_data,layout=layout)

    maturity_graph = ply.plot(figure, auto_open=False, output_type='div')

    last_data = data.last()
    current_maturity = round(float(last_data.matu_index), 2)
    print(current_maturity)

    context = {
        'maturity_graph': maturity_graph,
        'current_maturity': current_maturity,
        'sensor': sensor,
        }
    
    return render(request, 'sensors/Maturity.html', context)
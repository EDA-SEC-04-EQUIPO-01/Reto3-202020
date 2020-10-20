"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.DataStructures import listiterator as it
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------
def newAnalyzer():
    analyzer = {"crashes":None,
                "dateIndex":None}
    analyzer["crashes"]=lt.newList("SINGLED_LINKED",compareIds)
    analyzer["dateIndex"]=om.newMap(omaptype="RBT",comparefunction=compareDates)
    analyzer["timeIndex"]= om.newMap(omaptype="RBT",comparefunction=compareTime)
    return analyzer


# Funciones para agregar informacion al catalogo

def addAccident(analyzer,accident):
    lt.addLast(analyzer["crashes"],accident)
    addDate(analyzer["dateIndex"], accident)
    addTime(analyzer["timeIndex"], accident)

def addDate(dateIndex, accident):
    accident_fullDate = accident["Start_Time"]
    accident_date = datetime.datetime.strptime(accident_fullDate, '%Y-%m-%d %H:%M:%S')
    is_There = om.get(dateIndex, accident_date.date())
    if is_There is not None:
        type = me.getValue(is_There)
    else:
        type = newTypes(accident)
        om.put(dateIndex,accident_date.date(),type)
    updateIndex(type, accident)
    return dateIndex

def updateIndex(type,accident):
    lst = type["crashes"]
    lt.addLast(lst, accident)
    accident_type = type["accident_type"]
    is_there_type = m.get(accident_type, accident["Severity"])
    if is_there_type is None:
        index = newAccidentIndex(accident["Severity"])
        lt.addLast(index["accidents"],accident)
        m.put(accident_type, accident["Severity"], index)
    else:
        index = me.getValue(is_there_type)
        lt.addLast(index["accidents"],accident)
    return type

def newAccidentIndex(severity):
    index = {"type":None, "accidents":None}
    index["type"]=severity
    index["accidents"]=lt.newList("SINGLED_LINKED",compareTypes)
    return index
    

def newTypes(accident):
    type = {"accident_type":None, "crashes":None}
    type["accident_type"] = m.newMap(numelements=10,
                                     maptype="PROBING",
                                     comparefunction=compareTypes)
    type["crashes"]=lt.newList("SINGLED_LINKED",compareIds)
    return type
    
def addTime(timeIndex,accident):
    fulldate = accident["Start_Time"]
    time = ""
    for a in range(11,19):
        time += fulldate[a]
    oftime = timefix(time)
    is_There = om.get(timeIndex,oftime)
    if is_There is not None:
        type = me.getValue(is_There)
    else:
        type = newTypes(accident)
        om.put(timeIndex,time,type)
    updateIndex(type, accident)
    return timeIndex
    
def timefix(time):
    if int(time[3]+time[4])<15 and int(time[3]+time[4])>=0:
        time = time[0]+time[1]+":00:00"

    elif int(time[3]+time[4])>=15 and int(time[3]+time[4])<45:
        time = time[0]+time[1]+":30:00"

    elif int(time[3]+time[4])>=45 and int(time[3]+time[4])<59:
        hora = int(time[0]+time[1])+1
        if len(str(hora))<2:
            time ="0"+str(hora)+":00:00"
        else:
            time = str(hora)[0]+str(hora)[1]+":00:00"
    return time


# ==============================
# Funciones de consulta
# ==============================
def accidentsSize(analyzer):
    
    return lt.size(analyzer['crashes'])


def indexHeight(analyzer):
   
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    
    return om.maxKey(analyzer['dateIndex'])

def getAccidentsByDate(date, analyzer):
    try:
        cant1 = 0
        cant2 = 0
        cant3 = 0
        cant4 = 0
        events = om.get(analyzer["dateIndex"], date)
        accidents_date = me.getValue(events)
        total = lt.size(accidents_date["crashes"])
        sev1 = m.get(accidents_date["accident_type"],"1")
        if sev1 != None:
            v1 = me.getValue(sev1)
            cant1 = lt.size(v1["accidents"])
        sev2 = m.get(accidents_date["accident_type"],"2")
        if sev2 != None:
            v2 = me.getValue(sev2)
            cant2 = lt.size(v2["accidents"])
        sev3 = m.get(accidents_date["accident_type"],"3")
        if sev3 != None:
            v3 = me.getValue(sev3)
            cant3 = lt.size(v3["accidents"])
        sev4 = m.get(accidents_date["accident_type"],"4")
        if sev4 != None:
            v4 = me.getValue(sev4)
            cant4 = lt.size(v4["accidents"])
        res = (total, cant1, cant2, cant3, cant4)
    except: 
        res = None
    return res 


def getAccidentsByDateRange(date1, date2, analyzer):
    try:
        total = 0
        cant1 = 0
        cant2 = 0
        cant3 = 0
        cant4 = 0
        dates = om.values(analyzer["dateIndex"],date1,date2)
        iterator = it.newIterator(dates)
        while it.hasNext(iterator):
            element = it.next(iterator)
            total += int(lt.size(element["crashes"]))
            sev1 = m.get(element["accident_type"],"1")
            if sev1 != None:
                v1 = me.getValue(sev1)
                cant1 += int(lt.size(v1["accidents"]))
            sev2 = m.get(element["accident_type"],"2")
            if sev2 != None:
                v2 = me.getValue(sev2)
                cant2 += int(lt.size(v2["accidents"]))
            sev3 = m.get(element["accident_type"],"3")
            if sev3 != None:
                v3 = me.getValue(sev3)
                cant3 += int(lt.size(v3["accidents"]))
            sev4 = m.get(element["accident_type"],"4")
            if sev4 != None:
                v4 = me.getValue(sev4)
                cant4 += int(lt.size(v4["accidents"]))
        if cant1 > cant2 and cant1 > cant3 and cant1 > cant4:
            res = (total, cant1, "severidad 1") 
        elif cant2 > cant1 and cant2 > cant3 and cant2 > cant4:
            res = (total, cant2, "severidad 2") 
        elif cant3 > cant2 and cant3 > cant1 and cant1 > cant4:
            res = (total, cant3, "severidad 3") 
        elif cant4 > cant2 and cant4 > cant3 and cant4 > cant3:
            res = (total, cant4, "severidad 4") 
    except:
         res = None
    return res 

def accidentsByTimeRange(time1, time2, analyzer):
    try:
        total = 0
        cant1 = 0
        cant2 = 0
        cant3 = 0
        cant4 = 0
        times = om.values(analyzer["timeIndex"],time1,time2)
        iterator = it.newIterator(times)
        while it.hasNext(iterator):
            element = it.next(iterator)
            total += int(lt.size(element["crashes"]))
            sev1 = m.get(element["accident_type"],"1")
            if sev1 != None:
                v1 = me.getValue(sev1)
                cant1 += int(lt.size(v1["accidents"]))
            sev2 = m.get(element["accident_type"],"2")
            if sev2 != None:
                v2 = me.getValue(sev2)
                cant2 += int(lt.size(v2["accidents"]))
            sev3 = m.get(element["accident_type"],"3")
            if sev3 != None:
                v3 = me.getValue(sev3)
                cant3 += int(lt.size(v3["accidents"]))
            sev4 = m.get(element["accident_type"],"4")
            if sev4 != None:
                v4 = me.getValue(sev4)
                cant4 += int(lt.size(v4["accidents"]))
        per = round((total/int(accidentsSize(analyzer)))*100,2)
        res = (total, cant1, cant2, cant3, cant4, per) 
    except:
         res = None
    return res 

# ==============================
# Funciones de Comparacion
# ==============================
def compareIds(id1,id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareDates(date1, date2):

    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareTypes(type1,type2):
    type = me.getKey(type2)
    if (type1 == type):
        return 0
    elif type1 > type:
        return 1
    else:
        return -1

def compareTime(time1, time2):
    timea = int(time1[0]+time1[1]+time1[3])
    timeb = int(time2[0]+time2[1]+time2[3])
    if (timea == timeb):
        return 0
    elif (timea > timeb):
        return 1
    else:
        return -1
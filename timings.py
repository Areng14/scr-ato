sig_time = {
    "Stepford Victoria": {
        "002": 8.2
    },
    "Stepford Central" : {
        "049": 4,
        "029" : 4,
        "022": 5,
    },
    "St Helens Bridge" : {
        "139" : 9,
        "127" : 9,
        "134" : 9,
    },
    "Elsemere Junction" : {
        "024" : 7.5,
        "027" : 7.5,
        "030" : 7.5,
        "023" : 7.5,
    },
    "Berrily" : {
        "035" : 3.5
    },
    "Benton" : {
        "185" : 3.5,
        "027" : 8,
        "025" : 8,
        "026" : 8,
    },
    "Farleigh" : {
        "148" : 1,
        "146" : 1,
        #Since farleigh has distance wrong.
        #When distance is zero stop train or else
        #OVERSHOOT
    },
    "Newry" : {
        #Added later. too lazy lmao
    },
    "Leighton Stepford Road" : {
        "351" : 6.5,
        "353" : 6.5,
        "338" : 6.5,
        "340" : 6.5,
        "349" : 6.5,
    }, #Since term platforms dont have
    #signals (ofc) and you can continue,
    #Put other normal sigs here
    "Westwyvern" : {
        "377" : 5.75,
        "477" : 5.75, #SC
        "479" : 6.25, #EX
        "466" : 6.25, #EX
        "468" : 5, #SC
    },

}

def gettime(station, signal):
    # Process the station name to match the format used in sig_time dictionary
    processed_station = station.replace("  "," ").replace("\n", "").replace("_", "").strip().title()
    
    if processed_station in sig_time:
        time_value = sig_time[processed_station].get(signal, None)
        print(f"[ARRIVAL]\n\nStation '{processed_station}' found.\nSignal times available.")
        return time_value
    else:
        print(f"[ARRIVAL]\n\nStation '{processed_station}' not found.\nSignal times unavailable.")
        return None


#Even though signalstime replaces stations timings.
#It it not reliable enough. Put rounded time in next_time as fallback.

next_time = {
    "Willowfield": 3.3,
    "Hemdon Park" : 1.75,
    "Stepford Victoria" : 8.25,
    "City Hospital" : 2.7,
    "Stepford East" : 8,
    "Stepford Central" : 10.1,
    "St Helens Bridge" : 6,
    "Stepford High Street" : 3.75,
    "Whitefield Lido" : 3,
    "Stepford United Football..." : 3.75,
    "Woodhead Lane" : 2.5,
    "Houghton Rake" : 4.25,
    "Whitefield": 4.2,
    "New Harrow": 1.75,
    "Elsemere Pond": 1.6,
    "Elsemere Junction": 3.25,
    "Berrily" : 5,
    "East Berrily" : 1.75,
    "Beaulieu Park" : 3.25,
    "Morganstown" : 12,
    "Farleigh" : 6.75,
    "James Street" : 2.1,
    "Airport West" : 3,
    "Cambridge Street Parkway" : 1.5,
    "Benton" : 10,
    "West Benton" : 2.5,
    "Faraday Road" : 1.65,
    "Eden Quay" :  1.75,
    "Newry" : 1.75,
    "Bodin" : 4.5,
    "Coxly" : 4,
    "Upper Staploe" : 3.75,
    "Water Newton" : 3.75,
    "Rocket Parade" : 3.75,
    "Leighton Stepford Road" : 3.75,
    "Leighton City" : 4.5,
    "Edgemead" : 4.75,
    "Leighton West" : 4,
    "Faymere" : 4.25,
    "Westercoast" : 5,
    "Millcastle" : 3.5,
    "Westwyvern" : 3.75,
    "Starryloch" : 3,
    "Northshore" : 6,
    "Airport Central": 0.5,
    "Terminal 1" : 5.5
}

def gettimen(next_station):
    # Normalize the input to match the key format in the dictionary
    normalized_key = next_station.replace("  "," ").replace("_","").strip().title()
    return next_time.get(normalized_key, 3.5)

next_speed = {
    "Farleigh" : 30,
}

def getspeed(next_station):
    # Normalize the input to match the key format in the dictionary
    normalized_key = next_station.replace("_","").strip().title()
    return next_speed.get(normalized_key, 45)
import from_normals, from_dailies
import csv
from collections import OrderedDict


def final_report(chunked_report, dailydata, style = "str"):
  #print("Site ID: " + str(siteid))

  if "dict" in style:
    d = OrderedDict()
    d['Heat Wave'] = from_dailies.heatwaveD(dailydata)
    d['Cold Wave'] = from_dailies.coldwaveD(dailydata)
    d['Freeze-Thaw Temperatures'] = from_dailies.freezethawD(dailydata)
    d['Diurnal Temperature Deviation'] = from_dailies.diurnaldeviationD(dailydata)

    # TEMPERATURE TRY/EXCEPTS
    try: d['High Temperatures'] = from_normals.hightemperature(chunked_report)
    except: d['High Temperatures'] = from_dailies.hightemperatureD(dailydata)

    try: d['Low Temperatures'] = from_normals.lowtemperature(chunked_report)
    except: d['Low Temperatures'] = from_dailies.lowtemperatureD(dailydata)

    try: d['Very Hot Days'] = from_normals.veryhotdays(chunked_report)
    except: d['Very Hot Days'] = from_dailies.veryhotdaysD(dailydata)

    try: d['Very Cold Days'] = from_normals.verycolddays(chunked_report)
    except: d['Very Cold Days'] = from_dailies.verycolddaysD(dailydata)

    try: d['Cooling Degree Days'] = from_normals.coolingdegreedays(chunked_report)
    except: d['Cooling Degree Days'] = from_dailies.coolingdegreedaysD(dailydata)

    try: d['Heating Degree Days'] = from_normals.heatingdegreedays(chunked_report)
    except: d['Heating Degree Days'] = from_dailies.heatingdegreedaysD(dailydata)

    # PRECIPITATION TRY/EXCEPTS
    try: d['Annual Precipitation'] = from_normals.annualprecipitation(chunked_report)
    except: d['Annual Precipitation'] = from_dailies.annualprecipitationD(dailydata)

    try: d['Spring Precipitation'] = from_normals.springprecipitation(chunked_report)
    except: d['Spring Precipitation'] = from_dailies.seasonalprecipitationD(dailydata)[0]

    try: d['Summer Precipitation'] = from_normals.summerprecipitation(chunked_report)
    except: d['Summer Precipitation'] = from_dailies.seasonalprecipitationD(dailydata)[1]

    try: d['Autumn Precipitation'] = from_normals.fallprecipitation(chunked_report)
    except: d['Autumn Precipitation'] = from_dailies.seasonalprecipitationD(dailydata)[2]

    try: d['Winter Precipitation'] = from_normals.winterprecipitation(chunked_report)
    except: d['Winter Precipitation'] = from_dailies.seasonalprecipitationD(dailydata)[3]
    
    try: d['Annual Snowfall'] = from_normals.annualsnowfalltotal(chunked_report)
    except: d['Annual Snowfall'] = from_dailies.annualsnowfalltotalD(dailydata)

    try: d['Annual Average Snow Depth'] = from_normals.annualsnowdepth(chunked_report)
    except: d['Annual Average Snow Depth'] = from_dailies.annualsnowdepthD(dailydata)
    try: d['Winter Average Snow Depth'] = from_normals.averagewintersnowdepth(chunked_report)
    except: d['Winter Average Snow Depth'] = from_dailies.averagewintersnowdepthD(dailydata)
    
    try: d['Extreme Snowfall Days'] = from_normals.extremesnowfalldays(chunked_report)
    except: d['Extreme Snowfall Days'] = from_dailies.extremesnowfalldaysD(dailydata)

    # MISC TRY/EXCEPTS
    try: d['Dry Days'] = from_normals.drydays(chunked_report)
    except: d['Dry Days'] = from_dailies.drydaysD(dailydata)
    try: d['Strong Wind Days'] = from_normals.strongwinddays(chunked_report)
    except: d['Strong Wind Days'] = from_dailies.strongwinddaysD(dailydata)



    print(d)

  if "str" in style:
    for item in d:
      print(item, d[item])
    #print("Freeze-Thaw Cycles: N/A")

    #print("Extreme Temperatures: ")
    #print("- Heat Wave: ")
    #print("- High Temperatures: %.1f" % from_normals.hightemperature(chunked_report))
    #print("- Very Hot Days: %.1f" % from_normals.veryhotdays(chunked_report))
    #print("- Diurnal Temperature Deviation: ")
    #print("- Cold Wave: ")
    #print("- Low Temperatures: %.1f" % from_normals.lowtemperature(chunked_report))
    #print("- Very Cold Days: %.1f" % from_normals.verycolddays(chunked_report))

    #print("- Cooling Degree Days: %.1f" % from_normals.coolingdegreedays(chunked_report))
    #print("- Heating Degree Days: %.1f" % from_normals.heatingdegreedays(chunked_report))

    #print("Annual & Seasonal Precipitation")
    #print("- Total Precipitation (Annual): %.1f" % from_normals.annualprecipitation(chunked_report))
    #print("- Total Precipitation (Spring): %.1f" % from_normals.springprecipitation(chunked_report))
    #print("- Total Precipitation (Summer): %.1f" % from_normals.summerprecipitation(chunked_report))
    #print("- Total Precipitation (Fall): %.1f" % from_normals.fallprecipitation(chunked_report))
    #print("- Total Precipitation (Winter): %.1f" % from_normals.winterprecipitation(chunked_report))
    #print("- Annual Snow Depth: %.1f" % from_normals.annualsnowdepth(chunked_report))
    #print("- Average Winter Snow Depth: %.1f" % from_normals.averagewintersnowdepth(chunked_report))
    #print("- Extreme Snowfall Totals: %.1f" % from_normals.extremesnowfalldays(chunked_report))
    #print("- Annual Snowfall Total: %.1f" % from_normals.annualsnowfalltotal(chunked_report))

    #print("Design Event Precipitation")
    #print("- 1:5 yr/24 h: ")
    #print("- 1:50 yr/15 min: ")
    #print("- 1:50 yr/24 h: ")
    #print("- 1:100 yr/24 h: ")

    #print("Freezing Rain")
    #print("- Annual Freezing Precipitation Hours: ")
    #print("- Annual Freezing Rain Hours: ")

    #print("Wildfire")
    #print("- Climate Moisture Index: ")
    #print("- Dry Days: %.1f" % from_normals.drydays(chunked_report))
    #print("- Annual SPEI Values: ")
    #print("- Wildfire Events/Yr: ")

    #print("- Strong Winds: %.1f" % from_normals.strongwinddays(chunked_report))

    #print("Thunderstorms, lightning, tornadoes, hail")
    #print("Hail Frequency/severity: ")
    #print("Tornado Frequency/severity: ")
    #print("Thunderstorm Frequency/severity")

    #print("hurricanes and Tropical Storms")

    #print("Flooding")

    #print("Riparian erosion")

    #print("Sea Level Rise")

    #print("Coastal erosion")

    #print("Heavy Fog")


  if "csv" in style:
    d = [
      ["Climate Parameter", "Historical Climate (1981-2010)*"],
      ["Freeze-Thaw Cycles: ", ""], 
      ["Extreme Temperatures: ", ""], 
      ["Heat Wave: ", ""], 
      ["High Temperatures: ", str(from_normals.hightemperature(chunked_report))], 
      ["Very Hot Days:: ", str(from_normals.veryhotdays(chunked_report))], 
      ["Diurnal Temperature Deviation: ", ""], 
      ["Cold Wave: ", ""], 
      ["Low Temperatures: ", str(from_normals.lowtemperature(chunked_report))], 
      ["Very Cold Days", str(from_normals.verycolddays(chunked_report)) ], 
      ["Cooling Degree Days: ", str(from_normals.coolingdegreedays(chunked_report))], 
      ["Heating Degree Days: ", str(from_normals.heatingdegreedays(chunked_report))],
      ["Annual & Seasonal Precipitation: ", ], 
      ["Total Precipitation (Annual): ", str(from_normals.annualprecipitation(chunked_report)) ], 
      ["Total Precipitation (Spring): ", str(from_normals.springprecipitation(chunked_report))], 
      ["Total Precipitation (Summer): ", str(from_normals.summerprecipitation(chunked_report))], 
      ["Total Precipitation (Fall): ", str(from_normals.fallprecipitation(chunked_report)) ], 
      ["Total Precipitation (Winter): ", str(from_normals.winterprecipitation(chunked_report))], 
      ["Annual Snow Depth: ", str(from_normals.annualsnowdepth(chunked_report))], 
      ["Average Winter Snow Depth: ", str(from_normals.averagewintersnowdepth(chunked_report))], 
      ["Extreme Snowfall Totals: ", str(from_normals.extremesnowfalldays(chunked_report))], 
      ["Annual Snowfall Total: ", str(from_normals.annualsnowfalltotal(chunked_report))], 
      ["Design Event Precipitation: ", ], 
      ["1:5 yr/24 h: ", ], 
      ["1:50 yr/15 min: ", ], 
      ["1:50 yr/24 h: ", ], 
      ["1:100 yr/24 h: ", ], 
      ["Freezing Rain: ", ], 
      ["Annual Freezing Precipitation Hours: ", ], 
      ["Annual Freezing Rain Hours: ", ], 
      ["Wildfire: ", ], 
      ["Climate Moisture Index: ", ], 
      ["Dry Days: ", str(from_normals.drydays(chunked_report))], 
      ["Annual SPEI Values: ", ], 
      ["Wildfire Events/Yr: ", ], 
      ["Strong Winds: ", str(from_normals.strongwinddays(chunked_report)) ], 
      ["Thunderstorms, lightning, tornadoes, hail: ", ], 
      ["Hail Frequency/severity: ", ], 
      ["Tornado Frequency/severity: ", ], 
      ["Thunderstorm Frequency/severity: ", ], 
      ["hurricanes and Tropical Storms: ", ], 
      ["Flooding: ", ], 
      ["Riparian erosion: ", ], 
      ["Sea Level Rise: ", ], 
      ["Coastal erosion: ", ], 
      ["Heavy Fog: ", ], 
    ]
    with open("writtenreportoutput.csv", 'w') as f:
      csvwriter = csv.writer(f)
      for line in d:
        csvwriter.writerow(line)
    print("file written)")
    
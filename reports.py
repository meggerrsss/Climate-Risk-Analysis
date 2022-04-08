import from_normals, from_dailies
import csv
from collections import OrderedDict


def final_report(chunked_report, dailydata, verbose = True, sigs = 2, config = None):
  #print("Site ID: " + str(siteid))

  d = OrderedDict()
  #d['Heat Wave'] = from_dailies.heatwaveD(dailydata)
  #d['Cold Wave'] = from_dailies.coldwaveD(dailydata)
  #d['Freeze-Thaw Temperatures'] = from_dailies.freezethawD(dailydata)
  #d['Diurnal Temperature Deviation'] = from_dailies.diurnaldeviationD(dailydata)

  # loops over everything in the ["report"] chunk of the config file, attempting to gather the normals data, then trying the dailies afterwards if it doesn't exist. 
  # generalized version of the try/excepts below previously
  report = config["report"]
  for k in report:
    if report[k]["run"]:
      name = report[k]["name"]
      try: normal = getattr(from_normals, k)
      except: pass  ############create error here
      daily = getattr(from_dailies, k +"D")
      if config['forcedailies']:
        d[name] = daily(dailydata)
      else:
        try: d[name] = normal(chunked_report)
        except: d[name] = daily(dailydata)
        
  
  #try: d['High Temperatures'] = from_normals.hightemperature(chunked_report)
  #except: d['High Temperatures'] = from_dailies.hightemperatureD(dailydata)

  #try: d['Low Temperatures'] = from_normals.lowtemperature(chunked_report)
  #except: d['Low Temperatures'] = from_dailies.lowtemperatureD(dailydata)

  #try: d['Very Hot Days'] = from_normals.veryhotdays(chunked_report)
  #except: d['Very Hot Days'] = from_dailies.veryhotdaysD(dailydata)

  #try: d['Very Cold Days'] = from_normals.verycolddays(chunked_report)
  #except: d['Very Cold Days'] = from_dailies.verycolddaysD(dailydata)
  
  #try: d['Cooling Degree Days'] = from_normals.coolingdegreedays(chunked_report)
  #except: d['Cooling Degree Days'] = from_dailies.coolingdegreedaysD(dailydata)

  #try: d['Heating Degree Days'] = from_normals.heatingdegreedays(chunked_report)
  #except: d['Heating Degree Days'] = from_dailies.heatingdegreedaysD(dailydata)

    # PRECIPITATION TRY/EXCEPTS
  #try: d['Annual Precipitation'] = from_normals.annualprecipitation(chunked_report)
  #except: d['Annual Precipitation'] = from_dailies.annualprecipitationD(dailydata)

  #try: d['Spring Precipitation'] = from_normals.springprecipitation(chunked_report)
  #except: d['Spring Precipitation'] = from_dailies.seasonalprecipitationD(dailydata)[0]

  #try: d['Summer Precipitation'] = from_normals.summerprecipitation(chunked_report)
  #except: d['Summer Precipitation'] = from_dailies.seasonalprecipitationD(dailydata)[1]

  #try: d['Autumn Precipitation'] = from_normals.fallprecipitation(chunked_report)
  #except: d['Autumn Precipitation'] = from_dailies.seasonalprecipitationD(dailydata)[2]

  #try: d['Winter Precipitation'] = from_normals.winterprecipitation(chunked_report)
  #except: d['Winter Precipitation'] = from_dailies.seasonalprecipitationD(dailydata)[3]
    
  #try: d['Annual Snowfall'] = from_normals.annualsnowfalltotal(chunked_report)
  #except: d['Annual Snowfall'] = from_dailies.annualsnowfalltotalD(dailydata)

  #try: d['Annual Average Snow Depth'] = from_normals.annualsnowdepth(chunked_report)
  #except: d['Annual Average Snow Depth'] = from_dailies.annualsnowdepthD(dailydata)
  #try: d['Winter Average Snow Depth'] = from_normals.averagewintersnowdepth(chunked_report)
  #except: d['Winter Average Snow Depth'] = from_dailies.averagewintersnowdepthD(dailydata)
    
  #try: d['Extreme Snowfall Days'] = from_normals.extremesnowfalldays(chunked_report)
  #except: d['Extreme Snowfall Days'] = from_dailies.extremesnowfalldaysD(dailydata)

  # MISC TRY/EXCEPTS
  #try: d['Dry Days'] = from_normals.drydays(chunked_report)
  #except: d['Dry Days'] = from_dailies.drydaysD(dailydata)
  #try: d['Strong Wind Days'] = from_normals.strongwinddays(chunked_report)
  #except: d['Strong Wind Days'] = from_dailies.strongwinddaysD(dailydata)

  #print(d)

  if verbose:
    for item in d:
      print(item, d[item])#, round(d[item], sigs))

  with open("writtenreportoutput.csv", 'w') as f:
    csvwriter = csv.writer(f)
    for line in d:
      csvwriter.writerow([line, round(d[line], 2)])
  if verbose: print("(written report file written)")
    
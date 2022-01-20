import from_normals
import csv






def final_report(chunked_report, style = "str"):
  #print("Site ID: " + str(siteid))

  if "dict" in style:
    d = {}
    return d

  if "str" in style:
    print("Freeze-Thaw Cycles: N/A")

    print("Extreme Temperatures: ")
    print("- Heat Wave: ")
    print("- High Temperatures: %.1f" % from_normals.hightemperature(chunked_report))
    print("- Very Hot Days: %.1f" % from_normals.veryhotdays(chunked_report))
    print("- Diurnal Temperature Deviation: ")
    print("- Cold Wave: ")
    print("- Low Temperatures: %.1f" % from_normals.lowtemperature(chunked_report))
    print("- Very Cold Days: %.1f" % from_normals.verycolddays(chunked_report))

    print("- Cooling Degree Days: %.1f" % from_normals.coolingdegreedays(chunked_report))
    print("- Heating Degree Days: %.1f" % from_normals.heatingdegreedays(chunked_report))

    print("Annual & Seasonal Precipitation")
    print("- Total Precipitation (Annual): %.1f" % from_normals.annualprecipitation(chunked_report))
    print("- Total Precipitation (Spring): %.1f" % from_normals.springprecipitation(chunked_report))
    print("- Total Precipitation (Summer): %.1f" % from_normals.summerprecipitation(chunked_report))
    print("- Total Precipitation (Fall): %.1f" % from_normals.fallprecipitation(chunked_report))
    print("- Total Precipitation (Winter): %.1f" % from_normals.winterprecipitation(chunked_report))
    print("- Annual Snow Depth: %.1f" % from_normals.annualsnowdepth(chunked_report))
    print("- Average Winter Snow Depth: %.1f" % from_normals.averagewintersnowdepth(chunked_report))
    print("- Extreme Snowfall Totals: %.1f" % from_normals.extremesnowfalldays(chunked_report))
    print("- Annual Snowfall Total: %.1f" % from_normals.annualsnowfalltotal(chunked_report))

    print("Design Event Precipitation")
    print("- 1:5 yr/24 h: ")
    print("- 1:50 yr/15 min: ")
    print("- 1:50 yr/24 h: ")
    print("- 1:100 yr/24 h: ")

    print("Freezing Rain")
    print("- Annual Freezing Precipitation Hours: ")
    print("- Annual Freezing Rain Hours: ")

    print("Wildfire")
    print("- Climate Moisture Index: ")
    print("- Dry Days: %.1f" % from_normals.drydays(chunked_report))
    print("- Annual SPEI Values: ")
    print("- Wildfire Events/Yr: ")

    print("- Strong Winds: %.1f" % from_normals.strongwinddays(chunked_report))

    print("Thunderstorms, lightning, tornadoes, hail")
    print("Hail Frequency/severity: ")
    print("Tornado Frequency/severity: ")
    print("Thunderstorm Frequency/severity")

    print("hurricanes and Tropical Storms")

    print("Flooding")

    print("Riparian erosion")

    print("Sea Level Rise")

    print("Coastal erosion")

    print("Heavy Fog")


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
    
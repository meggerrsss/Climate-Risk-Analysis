import meghan

def final_report(chunked_report):
  #print("Site ID: " + str(siteid))

  print("Freeze-Thaw Cycles: N/A")

  print("Extreme Temperatures: ")
  print("- Heat Wave: ")
  print("- High Temperatures: %.1f" % meghan.hightemperature(chunked_report))
  print("- Very Hot Days: %.1f" % meghan.veryhotdays(chunked_report))
  print("- Diurnal Temperature Deviation: ")
  print("- Cold Wave: ")
  print("- Low Temperatures: %.1f" % meghan.lowtemperature(chunked_report))
  print("- Very Cold Days: %.1f" % meghan.verycolddays(chunked_report))

  print("- Cooling Degree Days: %.1f" % meghan.coolingdegreedays(chunked_report))
  print("- Heating Degree Days: %.1f" % meghan.heatingdegreedays(chunked_report))

  print("Annual & Seasonal Precipitation")
  print("- Total Precipitation (Annual): %.1f" % meghan.annualprecipitation(chunked_report))
  print("- Total Precipitation (Spring): %.1f" % meghan.springprecipitation(chunked_report))
  print("- Total Precipitation (Summer): %.1f" % meghan.summerprecipitation(chunked_report))
  print("- Total Precipitation (Fall): %.1f" % meghan.fallprecipitation(chunked_report))
  print("- Total Precipitation (Winter): %.1f" % meghan.winterprecipitation(chunked_report))
  print("- Annual Snow Depth: %.1f" % meghan.annualsnowdepth(chunked_report))
  print("- Average Winter Snow Depth: %.1f" % meghan.averagewintersnowdepth(chunked_report))
  print("- Extreme Snowfall Totals: %.1f" % meghan.extremesnowfalldays(chunked_report))
  print("- Annual Snowfall Total: %.1f" % meghan.annualsnowfalltotal(chunked_report))

  print("Design Event Precipitation")
  print("- 1:5 yr/24 h: ")
  print("- 1:59 yr/15 min: ")
  print("- 1:50 yr/24 h: ")
  print("- 1:100 yr/24 h: ")

  print("Freezing Rain")
  print("- Annual Freezing Precipitation Hours: ")
  print("- Annual Freezing Rain Hours: ")

  print("Wildfire")
  print("- Climate Moisture Index: ")
  print("- Dry Days: %.1f" % meghan.drydays(chunked_report))
  print("- Annual SPEI Values: ")
  print("- Wildfire Events/Yr: ")

  print("- Strong Winds: %.1f" % meghan.strongwinddays(chunked_report))

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
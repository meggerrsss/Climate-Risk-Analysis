print("Freeze-Thaw Cycles: N/A")

print("Extreme Temperatures: ")
print("- Heat Wave: ")
print("- High Temperatures: %.1f" % hightemperature(chunked_report))
print("- Very Hot Days: %.1f" % veryhotdays(chunked_report))
print("- Diurnal Temperature Deviation: ")
print("- Cold Wave: ")
print("- Low Temperatures: %.1f" % lowtemperature(chunked_report))
print("- Very Cold Days: %.1f" % verycolddays(chunked_report))

print("- Cooling Degree Days: %.1f" % coolingdegreedays(chunked_report))
print("- Heating Degree Days: %.1f" % heatingdegreedays(chunked_report))

print("Annual & Seasonal Precipitation")
print("- Total Precipitation (Annual): ")
print("- Total Precipitation (Spring): ")
print("- Total Precipitation (Summer): ")
print("- Total Precipitation (Fall): ")
print("- Total Precipitation (Winter): ")
print("- Annual Snow Depth: %.1f" % annualsnowdepth(chunked_report))
print("- Average Winter Snow Depth: %.1f" % averagewintersnowdepth(chunked_report))
print("- Extreme Snowfall Totals: ")
print("- Annual Snowfall Total: ")

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
print("- Dry Days: %.1f" % drydays(chunked_report))
print("- Annual SPEI Values: ")
print("- Wildfire Events/Yr: ")

print("Strong Winds: ")

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
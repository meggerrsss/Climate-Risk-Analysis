# unsure if this needs to be run in every file....

def openconfig():
  # importing from config file, call arguments like 
  with open("config.toml", "rb") as f:
    config = tomli.load(f)

  # converting each line in config.toml to its own variable name
  for sett in config.keys():
    #exec("{0} = {1}".format(sett,config[sett]))
    globals()[sett] = config[sett] 

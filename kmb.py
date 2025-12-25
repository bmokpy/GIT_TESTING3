import pandas as pd
import requests as req
import json
from termcolor import colored, cprint
from convert_chrs import convert_chrs as cc
from convert_chrs import spacing
import warnings

warnings.filterwarnings("ignore")
pd.options.display.max_rows = 80
nr_chr = 6

def eta(route="98", query_out="峻瀅", query_in="峻瀅", stop_list=False, service_type=1):

  url_base = f"https://data.etabus.gov.hk/v1/transport/kmb"
  
  url_routes = f"/route/"  # all routes origin and destination (basic info)
  url_routes_n_stops = f"/route-stop/" # all routes & all corr stops id (but no name)
  url_stops = f"/stop/" # all stops info (but no routes info) for stop name lookup
  url_eta_route_stops = f"/route-eta/{route}/{service_type}" # eta info of all stops of a route
  
  
  r1 = req.get(url_base + url_routes)
  routes = pd.DataFrame(json.loads(r1.text)["data"]).iloc[:,[0,1,2,4,7]]
  
  
  rt = routes.query('route == @route')
  
  print()
  print("=" * 40)
  cprint("KMB ROUTE INQUIRY", attrs={"bold":True})
  print("=" * 40)
  
  print(rt.T.to_string(header=False), "\n")
  
  
  # # All Stops info (stop_id) for a particular Route
  route_stops = pd.DataFrame()
  for d in ["in", "out"]:
    r2 = req.get(f"{url_base}{url_routes_n_stops}{route}/{d}bound/{service_type}")
    
    tmp = pd.DataFrame(json.loads(r2.text)["data"])
    route_stops=pd.concat([route_stops, tmp], axis=0)
    
  
  
  # # All Stop Names (for all routes)
  r3 = req.get(url_base + url_stops)
  stops_list = pd.DataFrame(json.loads(r3.text)["data"]).iloc[:,[0,2]]
  stops_list
  
  
  # # Get ETA data for Route_Stops
  r3 = req.get(url_base + f"/route-eta/{route}/{service_type}")
  route_stops_eta = pd.DataFrame(json.loads(r3.text)["data"]).iloc[:,[1,2,3,4,5,8,9,10]]
  route_stops_eta["uniq"] = route_stops_eta.apply(lambda x: f"{x.dir}{x.service_type}{x.seq}", axis=1) # To be looked up by route_stops_temp
  route_stops_eta.eta = pd.to_datetime(route_stops_eta.eta)
  route_stops_eta
  
  
  # # Lookup Stop Names to Route_stops DataFrame
  route_stops_temp = route_stops.merge(stops_list[["stop", "name_tc"]], on="stop", how="left") # Lookup Stop Name
  route_stops_temp["uniq"] = route_stops_temp.apply(lambda x: f"{x.bound}{x.service_type}{x.seq}", axis=1) # Create a unique id col to lookup ETA next
  route_stops_temp[["service_type", "seq"]] = route_stops_temp[["service_type", "seq"]].astype(int)
  
  
  route_stops_temp2 = route_stops_temp.merge(route_stops_eta[['uniq', 'eta_seq', 'eta']], on='uniq', how='left')
  route_stops_temp2.eta = route_stops_temp2.eta.dt.strftime("%H:%M")
  #route_stops_temp2
  
  
  route_stops_temp2.query('name_tc.str.contains("澳.*轉")')
  
  
  route_stops_temp3 = route_stops_temp2.pivot(index=["seq","route","name_tc", "bound"], columns="eta_seq", values="eta")
  #print(route_stops_temp3.head())
  
  final = route_stops_temp3.iloc[:,:3] if len(route_stops_temp3.columns) > 3 else route_stops_temp3  #tenary operator
  final = final.reset_index(level=["route","name_tc", "bound"]) #.reset_index(drop=False)
  # print(final)
  
  def eta_query(query=query_out,direction="Out"):
    q = final.query('name_tc.str.contains(@query) & bound == @direction[0].upper()')
    
    #q.name_tc = q.name_tc.str[-nr_chr:]
    q.name_tc = q.name_tc.apply(cc)
    q.name_tc = q.name_tc.apply(spacing, args=[nr_chr])
    # q = q.set_index(["route", "bound", "name_tc"])
    
    print(q.to_string(header=False, index=True, index_names=False, na_rep="-:-"))
    print()
  
  
  eta_query(query_out,"Out")
  eta_query(query_in,"In")
  
  
  if stop_list:
    print()
    cprint(f"路綫車站列表 - {cc(route)}\n", attrs=dict(bold=True, reverse=True))
    stops = final.iloc[:,[2,1]].reset_index()
    stops.name_tc = stops.name_tc.apply(cc)
    stops.name_tc = stops.name_tc.apply(spacing, args=[10])
    
    pvt_stops = stops.pivot(values="name_tc", index="seq", columns="bound")
    
    print(pvt_stops)
    



if __name__ == "__main__":
  
  eta(
  route = "290X",
  query_out = "峻瀅|康城",
  query_in = "荃灣|安達",
  stop_list=True,
  service_type = 1,
  )
  
  
  eta(
  route = "98",
  query_out = "峻瀅|康城|觀塘",
  query_in = "",
  stop_list=True,
  service_type = 1,
  )
  
  
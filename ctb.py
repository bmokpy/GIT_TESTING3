import pandas as pd
import httpx
import time
import asyncio
from termcolor import cprint
import logging
from tabulate import tabulate

pd.set_option("display.max_rows", 100)

# Configure the logger used by httpx
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)  # Set the logging level to WARNING or higher


base_url = "https://rt.data.gov.hk/v2/transport/citybus/"  # Base URL


# In[258]:


############# EXAMPLE ################
async def async_task(client, url):
    r = await client.get(url)
    return r.json()["data"]
######################################

async def get_route(client, route = 797):  # Route Details
    r = await client.get( base_url + f"route/CTB/{route}" ).json()['data']
    return {"route": r['route'], "from": r["orig_tc"], "to": r["dest_tc"]}

async def get_stop_name(client, stop_id = "001655"):  # Get Stop name by ID
    r = await client.get( base_url + f"stop/{stop_id}" )
    return r.json()['data']['name_tc']


async def get_eta(client, route = 797, stop_id = "001655", direction = "in", show=2):  # Stop ETA
    r = await client.get( base_url + f"eta/CTB/{stop_id}/{route}" )
    #return [dt.strptime(eta["eta"][:19], "%Y-%m-%dT%H:%M:%S") for eta in ETAs]
    schedules = []
    for x in (t:= r.json()["data"]):
        if x["dir"] == direction[0].upper():
            schedules.append(x["eta"][11:16])
    result = " ".join(schedules[:show]) if len(schedules) > 0 else "---"
    return result


async def async_get_route_all_stops(client, route = 797, direction = "in" ):  # All stop ids of a route
    r = await client.get( base_url + f"route-stop/CTB/{route}/{direction}bound" )
    return r.json()['data']

def time_it(fx):
    async def wrapper_fx(*args, **kwargs):
        start = time.time()
        x = await fx(*args, **kwargs)
        lapse = time.time() - start
        print(f"lapse Time: {lapse:.3f}s")
        return x
    #time.sleep(0.1)
    return wrapper_fx
     


# In[259]:


## MAIN FUNCTION ##
@time_it
async def main(route = 797, q = "", show=2):
    
    async with httpx.AsyncClient() as client:
        
        tasks = [async_get_route_all_stops(client, route, direction ) for direction in ["out", "in"] ]
        results = await asyncio.gather(*tasks)
        len_in = len(results[0])

        in_out = [pd.DataFrame(x).iloc[:,[2,3,4]] for x in results]
        combined = pd.concat(in_out, axis=0)

        tasks_get_names = []
        tasks_get_etas = []
        for stop, dir in zip(combined.stop, combined.dir):
            tasks_get_names.append(get_stop_name(client, stop))
            tasks_get_etas.append(get_eta(client, route, stop, dir, show=show))
        names_n_etas = await asyncio.gather(*tasks_get_names, *tasks_get_etas)

    combined["stop_name"] = names_n_etas[:len(names_n_etas)//2]
    combined["eta"] = names_n_etas[len(names_n_etas)//2:]

    query_result = combined.query('stop_name.str.contains(@q) or seq == 1').set_index('seq')

    #print("~" * 40 )
    
    #route_fw = "".join([chr(ord(c)+65248) for c in route])
    cprint(f"\nRoute: {route}", color="blue", attrs=["bold"])

    final = query_result.iloc[:,[0,3,2]]

    print(tabulate(final, 
    headers=["#", "d", "schedule", "station"]))


# In[261]:

if __name__ == "__main__":

    # asyncio.run(main('793', "峻瀅|首都|譽港灣|尖"))
    
    # asyncio.run(main('796x', ""))
    
    # asyncio.run(main(797,"峻瀅|首都|大有街|新蒲崗|爵祿街"))
    asyncio.run(main('795x',"荔枝角"))
    # asyncio.run(main("790"))

import schedule, time
import mtr
import ctb
import asyncio
import console
import weather
import os, sys
import kmb

def mtr_eta():
  console.clear()
  mtr.eta()

# schedule.every().second.do(mtr_run)


# WIP
routes = {
  '790': "首都|峻瀅|尖|漆咸道南",
  '797': "首都|大有|爵祿",
}



async def ctb_eta():
  
  results = await asyncio.gather(
  ctb.main(797, "首都|大有|爵祿"),
  ctb.main(790, "首都|峻瀅|尖|漆咸道南"),
  ctb.main('796x', "首都|尖|峻瀅|漆咸道南"),
  ctb.main('796p', "首都|尖|峻瀅"),
  ctb.main(793, "大埔道|寶血|太子站|旺角|首都|峻瀅"), ctb.main("A28"))

def ctb_single(route):
  return ctb.main


#def restart():
#  os.execl(sys.executable, (sys.executable, sys.argv))

def kmb_eta():
  
  kmb.eta(
    route = "290X",
    query_out = "峻瀅|康城",
    query_in = "荃灣|安達",
    stop_list=True,
    service_type = 1,
    )
    
  kmb.eta(
    route = "298X",
    query_out = "峻瀅|康城",
    query_in = "",
    stop_list=True,
    service_type = 1,
    ),
    
  kmb.eta(
    route = "98",
    query_out = "峻瀅|康城",
    query_in = "",
    stop_list=True,
    service_type = 1,
    )



if __name__ == "__main__":
  
  mtr_eta()
  weather.weather()
  
  input("\npress key to show bus schedule...")
  asyncio.run(ctb_eta())
  
  kmb_eta()

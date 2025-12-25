import requests as req
from datetime import datetime as dt
from termcolor import cprint, colored
from tabulate import tabulate

class Mtr:
  direction=["DOWN","UP"]
  fmt = "%Y-%m-%d %H:%M:%S"
  
  def __init__(self, line, station):
    self.line  = line.upper()
    self.station = station.upper()
    
  def getData(self, direction=direction):
    r = req.get(f"https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line={self.line}&sta={self.station}")
    data = r.json()["data"][f"{self.line}-{self.station}"]
    
    now = dt.now()

    all_data = []
    if type(direction) != list:
      direction = [str(direction).upper()]
      
    for way in direction:
      if dd:= data.get(way):
  
        for x in dd:
          sch_time = dt.strptime(x["time"], Mtr.fmt)
          is_valid = sch_time > now
          delta_time = str(sch_time - now)[-12:-7].replace(":","m")+"s"
          delta_time_fnl = delta_time if is_valid else " -- "

          all_data.append((
            colored("DN", "yellow") if way == "DOWN" else colored("UP", "blue" ),
            self.station,
            x["dest"] if x["dest"] != "LHP" else colored(x["dest"], "red"),
            sch_time.strftime("%H:%M"),
            delta_time_fnl
          ))
    return all_data
    
     
  def dataTable(self, direction=direction):
    line = colored(f" {self.line} ", "white", "on_green")
    header = [colored(x, attrs=["bold"]) for x in ["dir", "from", "dest", "time", "left"]]
    cprint("\nMTR Train Schedule - "+line, attrs=["bold"])
    print(tabulate(self.getData(direction), headers=header, tablefmt="fancy_grid"))
    # print("Current Time:", dt.now().strftime("%H:%M:%S"), "\n")

def eta():
  tik = Mtr("tkl", "tik").dataTable("up")
  lhp = Mtr("tkl", "lhp").dataTable("down")
  
  

if __name__ == "__main__":

  eta()
  
def convert_chrs(string, full_width=True):
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # function for single char    #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def convert_chr(x:str, full_width=True, show_type=False)-> str:
        import unicodedata as u
        
        if show_type:
            print(u.east_asian_width(x))
        
        if x == " ":
            if full_width:
                #return chr(65294)
                return chr(12288)
            else:
                return " "
        
        if u.east_asian_width(x) in ["F", "W", "A"]:
            if full_width:
                return x
            else:
                return chr(ord(x)-65248)
        else:
            if full_width:
                return chr(ord(x)+65248)
            else:
                return x
    
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # Codes for string conversion #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    string = string.replace(", ", ",").replace(" (", "(").replace(") ", ")")
    result = ""
    for x in str(string):
        result += convert_chr(x, full_width)
    return result
    
    

def spacing(string, nr_chr=10):
  #spc = chr(ord(".")+65248)
  spc = chr(12288)
  for i in range(1, nr_chr+1):
    if len(string) == i:
      return string + spc *(nr_chr-i)
  else:
    return string[:nr_chr]
    
    
    
    
    
if __name__ == "__main__":
  print(convert_chrs("apple orange"))
  print(spacing("apple"))
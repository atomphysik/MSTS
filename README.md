# Export Tournament Scores To SpreadSheet!


## Tutorial Step-By-Step

### Download This File!
* Self-explanatory

### Get your api-key from osu! web
* visit https://old.ppy.sh/p/api/ 
* fill application name and redirect url `ex)multiScores-to-spreadsheet, http://localhost:727/`
* apply and get your api key!

### Download Python And Libraries
* python : https://www.python.org/downloads/
* After downloading python, type these commands on powershell
  ```
   pip install requests
   pip install gspread
   pip install --upgrade oauth2client
  ```
### Make A SpreadSheet And Share It
* share with the email in service acc key json file

### Edit Config.py
* Open config.py with notepad, vscode, ... anything you want !!
* Fill out values with api-key, spreadsheet url, two sheet names
* MAKE SURE THAT SHEETS ARE CLEAN!!

### Open Main.py With Key.json
* Open powershell and type : `python main.py`
  




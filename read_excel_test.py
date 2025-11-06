import pandas as pd 
from pathlib import Path 
p = Path("data/raw")
file = list(p.glob("*.xlsx"))[0]
df=pd.read_excel(file)
print(df.head())
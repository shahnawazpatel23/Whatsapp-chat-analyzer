import pandas as pd
import re

def preprocess(data):

    pattern = r"(\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\u202f[AP]M) - ([^:]+): (.+)"

    matches = re.findall(pattern,data)

    df = pd.DataFrame(matches, columns=["Date", "User", "Message"])
    df["Date"] = pd.to_datetime(df["Date"])

    df['year'] = df['Date'].dt.year
    df["month"] = df["Date"].dt.month_name()
    df['dayname'] = df['Date'].dt.day_name()
    df['day'] = df['Date'].dt.day
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute
    df['monthnumber'] = df['Date'].dt.month
    return df
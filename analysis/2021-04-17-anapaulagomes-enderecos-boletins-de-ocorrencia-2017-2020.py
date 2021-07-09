#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from scripts.geolocation_info import get_geocode_info

df = pd.read_csv("2020-FEIRA - Sheet1.csv")
df.head()


# In[ ]:


addresses = df[["dbo_Logradouro_descricao", "dbo_Bairro_descricao"]]
addresses


# In[ ]:


addresses = addresses[addresses["dbo_Logradouro_descricao"] != "NAO INFORMADO"]
addresses


# In[ ]:


unique_address = {}
for _, row in addresses.iterrows():
    if not unique_address.get(row["dbo_Logradouro_descricao"]):
        unique_address[row["dbo_Logradouro_descricao"]] = {
            row["dbo_Bairro_descricao"]: True
        }
    elif not unique_address[row["dbo_Logradouro_descricao"]].get(
        row["dbo_Bairro_descricao"]
    ):
        unique_address[row["dbo_Logradouro_descricao"]] = {
            row["dbo_Bairro_descricao"]: True
        }
    else:
        unique_address[row["dbo_Logradouro_descricao"]][
            row["dbo_Bairro_descricao"]
        ] = True

print(len(unique_address))
unique_address


# In[ ]:


for street, neighborhoods in unique_address.items():
    for neighborhood in neighborhoods.keys():
        full_address = f"{street}, {neighborhood}, Feira de Santana, Bahia, Brazil"
        print(full_address)
        payload = get_geocode_info(full_address, raise_exception=True)
        if payload:
            for result in payload:
                if result["address"]["city"] == "Feira de Santana":
                    unique_address[street][neighborhood] = {
                        "api_address": result["title"],
                        "api_lat": result["position"]["lat"],
                        "api_long": result["position"]["lng"],
                    }
                    break
unique_address


# In[ ]:


unique_address["AVENIDA GOVERNADOR JOAO DURVAL CARNEIRO"]


# In[ ]:


def get_address(row):
    try:
        return unique_address[row.dbo_Logradouro_descricao][row.dbo_Bairro_descricao][
            "api_address"
        ]
    except:
        pass
    return


def get_lat(row):
    try:
        return unique_address[row.dbo_Logradouro_descricao][row.dbo_Bairro_descricao][
            "api_lat"
        ]
    except:
        pass
    return


def get_lng(row):
    try:
        return unique_address[row.dbo_Logradouro_descricao][row.dbo_Bairro_descricao][
            "api_long"
        ]
    except:
        pass
    return


addresses["api_address"] = addresses.apply(get_address, axis=1)
addresses["api_lat"] = addresses.apply(get_lat, axis=1)
addresses["api_lng"] = addresses.apply(get_lng, axis=1)


# In[ ]:


addresses


# In[ ]:


addresses.to_csv("api-unique-addresses-feira-2020.csv")


# In[ ]:

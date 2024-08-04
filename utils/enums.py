from enum import Enum
import sqlite3

class SqliteEnum(Enum):
    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return self.name


class States(SqliteEnum):
    Andaman_and_Nicobar_Islands = "Andaman and Nicobar Islands"
    Andhra_Pradesh = "Andhra Pradesh"
    Arunachal_Pradesh = "Arunachal Pradesh"
    Assam = "Assam"
    Bihar = "Bihar"
    Chandigarh = "Chandigarh" 
    Chhattisgarh = "Chhattisgarh"
    Dadra_and_Nagar_Haveli = "Dadra and Nagar Haveli"
    Daman_Diu = "Daman & Diu"
    Delhi = "Delhi"
    Goa = "Goa"
    Gujarat = "Gujarat"
    Haryana = "Haryana"
    Himachal_Pradesh = "Himachal Pradesh"
    Jammu_Kashmir = "Jammu & Kashmir"
    Jharkhand = "Jharkhand"
    Karnataka = "Karnataka"
    Kerala = "Kerala"
    Ladakh = "Ladakh"
    Lakshadweep = "Lakshadweep"
    Madhya_Pradesh = "Madhya Pradesh"
    Maharashtra = "Maharashtra" 
    Manipur = "Manipur"
    Meghalaya = "Meghalaya"
    Mizoram = "Mizoram"
    Nagaland = "Nagaland"
    Odisha = "Odisha"
    Puducherry = "Puducherry"
    Punjab = "Punjab"
    Rajasthan = "Rajasthan" 
    Sikkim = "Sikkim"
    Tamil_Nadu = "Tamil Nadu"
    Telangana = "Telangana"
    Tripura = "Tripura"
    Uttarakhand = "Uttarakhand"
    Uttar_Pradesh = "Uttar Pradesh"
    West_Bengal = "West Bengal"
    
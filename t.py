import os

import ds

os.environ["MY_INT_SETTING"] = "50"
os.environ["YESINT"] = "500"
os.environ["MY_STR_SETTING"] = "hehehe"
os.environ["MY_BOOL_SETTING"] = "FaLSe"

dir(ds)

print(ds.MY_INT_SETTING)
print(type(ds.MY_INT_SETTING))
print(ds.MY_STR_SETTING)
print(type(ds.MY_STR_SETTING))
print(ds.MY_BOOL_SETTING)
print(type(ds.MY_BOOL_SETTING))

if __name__ == "__main__":
    pass
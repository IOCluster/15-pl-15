import Register

wczytane_z_pliku = Register.CreateFromDocument( open('Register.xml').read() )

print(wczytane_z_pliku.Type)


import pyxb.utils.domutils

mess = Register

mess.Type = "TaskManager"
mess.Id = 123


print(mess.toxml("utf-8"))
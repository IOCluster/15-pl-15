import Register

wczytane_z_pliku = Register.CreateFromDocument( open('Register.xml').read() )

print(wczytane_z_pliku.Type)


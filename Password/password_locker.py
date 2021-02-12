#!/usr/bin/env python
# -*- coding: utf-8 -*-
from  cryptography.fernet import Fernet
from  tkinter import *
import sys
import os
import pyperclip
import mysql.connector
# from pynput import keyboard



def exito_guaradar():
    pantalla_exito=Toplevel()
    pantalla_exito.geometry("80x80")
    pantalla_exito.title("Hecho")
    palomita=PhotoImage(file='xd.png')
    x = Button(pantalla_exito,image = palomita,command =lambda:pantalla_exito.destroy())
    x.grid(row = 0, column = 0)
    pantalla_exito.mainloop()

def guardar_sin_db():
    palabraI=palabraC.get()
    usuariod=usuario.get()
    contrad=contra.get()
    palabraminiI=palabraI.lower()
    usuariodmini=usuariod.lower()
    clave=leer_clave()
    ferne=Fernet(clave)
    if(palabraI=="" and usuariod== "" and contrad == ""):
        Label(pantallados,text = "Falto o Faltaron campos por llenar").pack()
    else:
        entry1.delete(0,END)
        entry2.delete(0,END)
        entry3.delete(0,END)
        with open("passwords.key","ab") as archivo:
            archivo.write(palabraminiI.encode())
            archivo.write(b'\n')
            archivo.write(ferne.encrypt(usuariodmini.encode()))
            archivo.write(b'\n')
            archivo.write(ferne.encrypt(contrad.encode()))
            archivo.write(b'\n')
        print("operacion exitosa")
        exito_guaradar()



def guardar():
    if(os.stat('sqlcon.txt').st_size==0):
        guardar_sin_db()
    else:
        with open("sqlcon.txt","r") as archivo:
            llaves=[]
            llaves_chido=[]
            for linea in archivo:
                llaves.append(linea)
            for llave in llaves:
                llaves_chido.append(llave.replace("\n",""))
            for i in range(len(llaves_chido)):
                if(i==0):
                    host=llaves_chido[i]
                elif(i==1):
                    user=llaves_chido[i]
                else:
                    db=llaves_chido[i]
        print(host,user,db)
        try:
            con = mysql.connector.connect(host=host,user=user,database=db)

        except:
            print("algo anda mal ")
        cursor=con.cursor()


        palabraI=palabraC.get()
        usuariod=usuario.get()
        contrad=contra.get()

        palabraminiI=palabraI.lower()
        usuariodmini=usuariod.lower()
        contramini=contrad.lower()
        clave=leer_clave()
        ferne=Fernet(clave)
        info=("INSERT INTO password_locker(palabra_clave,usuario,contra) VALUES(%s,%s,%s)")

        este=(palabraminiI,usuariodmini,ferne.encrypt(contrad.encode()))
        cursor.execute(info,este)
        con.commit()
        if(palabraI=="" and usuariod== "" and contrad == ""):
            Label(pantallados,text = "Falto o Faltaron campos por llenar").pack()
        else:
            entry1.delete(0,END)
            entry2.delete(0,END)
            entry3.delete(0,END)
            with open("passwords.key","ab") as archivo:
                archivo.write(palabraminiI.encode())
                archivo.write(b'\n')
                archivo.write(ferne.encrypt(usuariodmini.encode()))
                archivo.write(b'\n')
                archivo.write(ferne.encrypt(contrad.encode()))
                archivo.write(b'\n')
            print("operacion exitosa")
            exito_guaradar()

        cursor.close()
        con.close()








def guardarInterfaz():
    global pantallados
    #Definimos los campos de espacio que ira En las entradas
    global palabraC
    global usuario
    global contra
    global entry1
    global entry2
    global entry3

    palabraC=StringVar()
    usuario=StringVar()
    contra = StringVar()
    #Creamos una nueva pantalla
    pantallados=Toplevel(pantalla1)
    pantallados.geometry("300x500")
    pantallados.title("Guardar")
    Label(pantallados,text="Palabra Clave",font=("Serif",24),bg='#000000',fg='#00C5FF').pack()
    entry1=Entry(pantallados,textvariable = palabraC,font=("Serif",19),bg='#000000',fg='#00C5FF')
    entry1.pack()
    Label(pantallados,text="Usuario",font=("Serif",24),bg='#000000',fg='#00C5FF').pack()
    entry2=Entry(pantallados,textvariable=usuario,font=("Serif",19),bg='#000000',fg='#00C5FF')
    entry2.pack()
    Label(pantallados,text="Contraseña",font=("Serif",24),bg='#000000',fg='#00C5FF').pack()
    entry3=Entry(pantallados,textvariable=contra,font=("Serif",19),bg='#000000',fg='#00C5FF')
    entry3.pack()
    Button(pantallados,text="Guardar",width="10",command=guardar,font=("Serif",22),bg='#000000',fg='#00C5FF').place(relx=0.5,y=300,anchor=CENTER)
    Button(pantallados,text="Regresar",width="10",font=("Serif",22),command = lambda: pantallados.destroy(),bg='#000000',fg='#00C5FF').place(relx=0.5,y=400,anchor=CENTER)
    pantallados.configure(bg='#000000')
    pantallados.mainloop()


def salir():
    pantalla1.destroy()
    sys.exit()

def buscarLacredencial():
    llaves=[]
    llaves_chido=[]
    c=nombreDeLacredencial.get()
    cual=c.lower()
    clave=leer_clave()
    ferne=Fernet(clave)
    with open("passwords.key","rb") as archivo:
        for linea in archivo:
            llaves.append(linea)
        for palabra in llaves:
            llaves_chido.append(palabra.replace(b'\n',b''))
        for i in range(len(llaves_chido)):
            if(llaves_chido[i]==cual.encode()):
                users=ferne.decrypt(llaves_chido[i+1])
                passsw=ferne.decrypt(llaves_chido[i+2])
                userLa=StringVar()
                passLa=StringVar()
                n1="Usuario: "+users.decode()
                n2="Contraseña: "+passsw.decode()
                userLa.set(n1)
                passLa.set(n2)
                Label(pantallaCredencial,textvariable =userLa,font=("Serif",24),bg='#000000',fg='#00C5FF').place(x=0,y=180)
                Button(pantallaCredencial,text="Copiar",font=("Serif",14),width="8",height="1",command=lambda:pyperclip.copy(users.decode()),bg='#000000',fg='#00C5FF').place(relx=0.5,y=230,anchor=CENTER)
                Label(pantallaCredencial,textvariable = passLa,font = ("Serif",24),bg='#000000',fg='#00C5FF').place(x=0,y=250)
                Button(pantallaCredencial,text="Copiar",font=("Serif",14),width="8",height="1",command=lambda:pyperclip.copy(passsw.decode()),bg='#000000',fg='#00C5FF').place(relx=0.5,y=300,anchor=CENTER)
                break
            elif(llaves_chido[i]==llaves_chido[-1] and llaves_chido[i]!=cual.encode()):
                Label(pantallaCredencial,text="Informacion no encontrada").pack()
            else:
                pass

def VerCredencial():
    global pantallaCredencial
    global nombreDeLacredencial
    nombreDeLacredencial = StringVar()
    pantallaCredencial = Toplevel(pantalla1)
    pantallaCredencial.geometry("300x500")
    pantallaCredencial.title("Buscar Credencial")
    Label(pantallaCredencial,text = "Introduce palabra clave ",font=("Sans",24),bg='#000000',fg='#00C5FF').pack()
    Entry(pantallaCredencial,textvariable = nombreDeLacredencial,font=("Serif",19),bg='#000000',fg='#00C5FF').pack()
    Button(pantallaCredencial,text = "Buscar",width="20",font=("Sans",24),command = buscarLacredencial,bg='#000000',fg='#00C5FF').place(relx=0.5,y=400,anchor=CENTER)
    Button(pantallaCredencial,text="Regresar",font=("Sans",24),width="20",command = lambda:pantallaCredencial.destroy(),bg='#000000',fg='#00C5FF').place(relx=0.5,y=450,anchor=CENTER)
    pantallaCredencial.configure(bg='#000000')
    pantallaCredencial.mainloop()

def Borrar_logica():
    res=Credencialborrada.get()
    k=res+'\n'
    crede=k.encode()
    TEMP=[]

    if(crede ==""):
        Label(pantallaBorrar,text="No se escribio nada",font=("Serif",20)).place(relx=0.5,y=270,anchor=CENTER)
    else:

        with open("passwords.key","rb") as archivo:
            for linea in archivo:
                TEMP.append(linea)
            f=open("temporal.key","ab")
            for i in range(len(TEMP)):
                if(TEMP[i]==crede ):
                    pass
                elif(TEMP[i-1]==crede):
                    pass
                elif(TEMP[i-2]==crede):
                    pass
                else:
                    f.write(TEMP[i])
            f.close()
            archivo.close()
        os.remove("passwords.key")
        os.rename("temporal.key","passwords.key")
        exito_guaradar()



def borrar_credencial():
    global Credencialborrada

    global pantallaBorrar
    Credencialborrada=StringVar()
    pantallaBorrar=Toplevel(pantalla1)
    pantallaBorrar.geometry("300x300")
    pantallaBorrar.title("Borrar Credencial")
    Label(pantallaBorrar,text="Escribe la credencial",font=("Serif",24),bg='#000000',fg='#00C5FF').pack()
    Entry(pantallaBorrar,textvariable=Credencialborrada,font=("Serif",20),bg='#000000',fg='#00C5FF').place(relx=0.5,y=70,anchor=CENTER)
    Button(pantallaBorrar,text="Borrar",width="20",height="2",command=Borrar_logica,bg='#000000',fg='#00C5FF').place(relx=0.5,y=150,anchor=CENTER)
    Button(pantallaBorrar,text="Regresar",width="20",height="2",command=lambda:pantallaBorrar.destroy(),bg='#000000',fg='#00C5FF').place(relx=0.5,y=220,anchor=CENTER)
    pantallaBorrar.configure(bg='#000000')
    pantallaBorrar.mainloop()

def ModificarLogica():
    nuevac=nuevacontra.get()
    cambiodeCrede=credencial.get()
    k=cambiodeCrede+'\n'
    crede=k.encode()
    TEMP=[]
    clave=leer_clave()
    ferne=Fernet(clave)
    if(crede =="" or nuevac ==""):
        Label(pantallaChance,text="No se escribio nada",font=("Serif",20),bg='#000000',fg='#00C5FF').place(relx=0.5,y=350,anchor=CENTER)
    else:

        with open("passwords.key","rb") as archivo:
            for linea in archivo:
                TEMP.append(linea)
            f=open("temporal.key","ab")
            for i in range(len(TEMP)):
                if(TEMP[i-2]==crede):
                    f.write(ferne.encrypt(nuevac.encode()))
                else:
                    f.write(TEMP[i])
            f.close()
            archivo.close()
        os.remove("passwords.key")
        os.rename("temporal.key","passwords.key")
        exito_guaradar()









def change():
    global pantallaChance
    global credencial
    global nuevacontra
    nuevacontra=StringVar()
    credencial=StringVar()

    pantallaChance = Toplevel(pantalla1)
    pantallaChance.title("Modificar")
    pantallaChance.geometry("300x400")
    Label(pantallaChance,text='Credencial',font=("Serif",24),bg='#000000',fg='#00C5FF').pack()
    Entry(pantallaChance,textvariable=credencial,font=("Serif",20),bg='#000000',fg='#00C5FF').pack()
    Label(pantallaChance,text="Nueva contrseña",font=("Serif",24),bg='#000000',fg='#00C5FF').pack()
    Entry(pantallaChance,textvariable=nuevacontra,font=("Serif",20),bg='#000000',fg='#00C5FF').pack()
    Button(pantallaChance,text="Modificar",width='20',height='2',command=ModificarLogica,bg='#000000',fg='#00C5FF').place(relx=0.5,y=200,anchor=CENTER)
    Button(pantallaChance,text="Regresar",width='20',height='2',command=lambda:pantallaChance.destroy(),bg='#000000',fg='#00C5FF').place(relx=0.5,y=290,anchor=CENTER)
    pantallaChance.configure(bg='#000000')
    pantallaChance.mainloop()


def conexion_db():
    pantalla_db.destroy()
    Server=Servidor.get()
    Us=user.get()
    Datab=db.get()

    con = mysql.connector.connect(host=Server,user=Us,database=Datab)

    clave=leer_clave()
    ferne= Fernet(clave)
    with open("sqlcon.txt","w")as archivo:
        archivo.write(Server)
        archivo.write('\n')
        archivo.write(Us)
        archivo.write('\n')
        archivo.write(Datab)
        archivo.write('\n')
    con.close()
    exito_guaradar()
    return
def base_de_datos():
    global Servidor
    global user
    global db
    global pantalla_db

    Servidor=StringVar()
    user = StringVar()
    db= StringVar()

    pantalla_db=Toplevel(pantalla1)
    pantalla_db.geometry("300x400")
    pantalla_db.title("base de datos")

    Label(pantalla_db,text="Servidor",font=("Serif",24),bg='#000000',fg='#00C5FF').pack()
    Entry(pantalla_db,textvariable=Servidor,font=("Serif",24),bg='#000000',fg='#00C5FF').pack()


    Label(pantalla_db,text="Usuario",font=("Serif",24),bg='#000000',fg='#00C5FF').pack()
    Entry(pantalla_db,textvariable=user,font=("Serif",24),bg='#000000',fg='#00C5FF').pack()

    Label(pantalla_db,text="Base de datos",font=("Serif",24),bg='#000000',fg='#00C5FF').pack()
    Entry(pantalla_db,textvariable=db,font=("Serif",24),bg='#000000',fg='#00C5FF').pack()
    Button(pantalla_db,text="conectar",font=("Serif",24),bg='#000000',fg='#00C5FF',command=conexion_db).place(relx=0.5,y=350,anchor=CENTER)

    pantalla_db.configure(bg='#000000')
    pantalla_db.mainloop()
def desconectar():
    with open('sqlcon.txt','w')as archivo:
        archivo.write=''
    print("exito")

def menu():
        global pantalla1
        # print("wow")
        pantalla.destroy()
        pantalla1=Tk()
        pantalla1.title("Menu")
        pantalla1.geometry("500x600")
        Button(pantalla1,text="Guardar nueva Credencial",width = "56",height="3",command = guardarInterfaz,bg='#000000',fg='#00C5FF').place(x=0,y=10)
        Button(pantalla1,text="Modificar Credencial",width = "56",height="3",bg='#000000',fg='#00C5FF',command=change).place(x=0,y=90)
        Button(pantalla1,text="Borrar Credencial",width = "56",height="3",command=borrar_credencial,bg='#000000',fg='#00C5FF').place(x=0,y=170)
        Button(pantalla1,text="Ver Credencial",width = "56",height="3",command=VerCredencial,bg='#000000',fg='#00C5FF').place(x=0,y=250)
        Button(pantalla1,text="Conectar base de datos",width = "56",height="3",command=base_de_datos,bg='#000000',fg='#00C5FF').place(x=0,y=330)
        Button(pantalla1,text="Desconectar base de datos",width = "56",height="3",command=desconectar,bg='#000000',fg='#00C5FF').place(x=0,y=410)
        Button(pantalla1,text="Salir",width = "56",height="3",command = salir,bg='#000000',fg='#00C5FF').place(x=0,y=490)
        pantalla1.configure(bg='#000000')
        pantalla1.update()




def Vaciar():
    entradaUsuario.delete(0,END)
    entradapass.delete(0,END)
    Label(pantalla,text="Usuario no valido o contraseña no valida ",font=("Serif",15),bg='#000000',fg='#00C5FF').place(x=0,y=260)


def comprobar():

    User = username.get()
    contra = password.get()
    clave=leer_clave()
    ferne= Fernet(clave)
    with open("passwords.key","rb") as archivo:
        llaves=[]
        llaves_chido=[]
        for linea in archivo:
            llaves.append(linea)
        for llave in llaves:
            llaves_chido.append(llave.replace(b'\n',b''))
        for i in range(len(llaves_chido)):
            if(ferne.decrypt(llaves_chido[i])==User.encode()):
                print("vientos")

                if(ferne.decrypt(llaves_chido[i+1])==contra.encode()):
                    menu()

                else:
                    Vaciar()

            elif(ferne.decrypt(llaves_chido[i])==llaves_chido[-1]):
                Vaciar()



def leer_clave():
    return open("clave.key","rb").read()




# def on_press(key):
#     if(key==keyboard.Key.enter):
#         pass
#
# def on_release(key):
#     intento=1
#     d=comprobar_teclado()
#     if(key==keyboard.Key.enter):
#         if(comprobar_teclado()==True):
#             Vaciar(intento)
#             menu()
#             return False
#         else:
#             pass




def main():
    global pantalla
    global username
    global password
    global entradaUsuario
    global entradapass
    #Si mal no me equivoco esto puede ser una clase

    pantalla = Tk()
    username = StringVar()
    password = StringVar()
    pantalla.geometry("300x300")
    pantalla.title("Password Locker")

    L1=Label(text = "Usuario",font=("Serif",24),bg='#000000',fg='#00C5FF').place(x=10,y=20)
    entradaUsuario=Entry(pantalla,textvariable =username,font=("Serif",19),width="22",bg='#000000',fg='#00C5FF')
    entradaUsuario.place(x=10,y=60)
    L2=Label(text = "Contraseña",font=("Serif",24),bg='#000000',fg='#00C5FF').place(x=10,y=100)
    entradapass=Entry(pantalla,textvariable = password,font=("Serif",19),width="22",show="*",bg='#000000',fg='#00C5FF')
    entradapass.place(x=10,y=140)
    B1=Button(pantalla,text = "Iniciar",bg='black',fg='#00C5FF',width = "10",height="2",command=lambda:comprobar()).place(x=100,y=200)
    pantalla.configure(bg='#000000')
    # listener = keyboard.Listener(on_press=on_press,on_release=on_release)
    # listener.start()
    pantalla.mainloop()





def generarclave():
    clave = Fernet.generate_key()
    with open('clave.key','wb') as archivo:
        archivo.write(clave)

def registro_Logica():
    Usur=Usuario_Registro.get()
    cont=contra_registro.get()
    generarclave()
    clave=leer_clave()
    ferne=Fernet(clave)
    with open('passwords.key','ab') as archivo:
        archivo.write(ferne.encrypt(Usur.encode()))
        archivo.write(b'\n')
        archivo.write(ferne.encrypt(cont.encode()))
        archivo.write(b'\n')
    print("bien")
    pantalla_Registrar.destroy()
    main()



def registrar():
    global Usuario_Registro
    global contra_registro
    global pantalla_Registrar
    pantalla_Registrar=Tk()
    Usuario_Registro=StringVar()
    contra_registro=StringVar()
    pantalla_Registrar.title("Registro")
    pantalla_Registrar.geometry("300x300")
    Label(pantalla_Registrar,text="Registro",font=("Serif",26),bg='#000000',fg='#00C5FF').pack()
    Label(pantalla_Registrar,text="Usuario",font=("Serif",24),bg='#000000',fg='#00C5FF').pack()
    Entry(pantalla_Registrar,textvariable=Usuario_Registro,font=("Serif",22),width="20",bg='#000000',fg='#00C5FF').pack()
    Label(pantalla_Registrar,text="Contraseña",font=("Serif",24),width="20",bg='#000000',fg='#00C5FF').pack()
    Entry(pantalla_Registrar,textvariable=contra_registro,font=("Serif",22),width="20",bg='#000000',fg='#00C5FF').pack()
    Button(pantalla_Registrar,text="registrar",font=("Serif",20),width="10",height="2",command=registro_Logica,bg='#000000',fg='#00C5FF').place(relx=0.5,y=250,anchor=CENTER)
    pantalla_Registrar.configure(bg='#000000')
    pantalla_Registrar.mainloop()


def verSiesNuevo():
    print("h")
    with open("passwords.key","rb") as archivo:
        s=archivo.read()
        if(os.stat('passwords.key').st_size == 0):
            return True
        else:
            return False


if __name__ == '__main__':
    valor=verSiesNuevo()
    if(valor == True):
        registrar()
    else:
        main()

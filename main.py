import os
import subprocess
from tkinter import messagebox
import customtkinter as ctk

ctk.set_appearance_mode("dark")

ativado=False

class Main(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("Maia Firewall")
        self.geometry("400x600")
        lbl_titulo_firewall = ctk.CTkLabel(master=self,text="MAIA FIREWALL",font=ctk.CTkFont(weight="bold",size=24))
        lbl_titulo_firewall.pack(ipady=50)
        lbl_tipo_de_protocolo = ctk.CTkLabel(master=self,text="Tipo de protocolo",font=ctk.CTkFont(weight="bold",size=14))
        lbl_tipo_de_protocolo.pack(side=ctk.TOP,anchor="center")
        cmb_tipo_de_protocolo = ctk.CTkComboBox(master=self,values=["TCP","UDP"],font=ctk.CTkFont(weight="bold",size=12),width=200,height=30)
        cmb_tipo_de_protocolo.pack(side=ctk.TOP,anchor="center")
        lbl_porta = ctk.CTkLabel(master=self,text="Porta",font=ctk.CTkFont(weight="bold",size=14))
        lbl_porta.pack(side=ctk.TOP,anchor="center", pady=(40,0))
        input_porta = ctk.CTkEntry(master=self,font=ctk.CTkFont(weight="bold",size=14))
        input_porta.pack(side=ctk.TOP,anchor="center",ipady=3)
        lbl_status_de_acesso = ctk.CTkLabel(master=self,text="Dar acesso ou bloquear",font=ctk.CTkFont(weight="bold",size=14))
        lbl_status_de_acesso.pack(side=ctk.TOP,anchor="center",pady=(50,0))
        cmb_status_de_acesso = ctk.CTkComboBox(master=self,values=["LIBERAR","BLOQUEAR"],width=200,height=30)
        cmb_status_de_acesso.pack(side=ctk.TOP,anchor="center")
        btn_aplicar = ctk.CTkButton(master=self,text="APLICAR",font=ctk.CTkFont(weight="bold",size=14),width=250,height=50,command=None)
        btn_aplicar.pack(side=ctk.TOP,anchor="center",pady=(60,0))  
      
        self.btnFirewallPadrao = ctk.CTkButton(master=self, text="ATIVAR FIREWALL PADRÃO",font=ctk.CTkFont(weight="bold",size=12),fg_color="#222222", text_color="#666666", hover_color="#333333", height=30, command=self.ativar_firewall)
        self.btnFirewallPadrao.pack(pady=20)
        
    def ativar_firewall(self):
        global ativado
        ativado = not ativado  # Inverte o valor booleano (True vira False, False vira True)
    
        if ativado:
            self.btnFirewallPadrao.configure(text="FIREWALL ATIVADO", fg_color="#006600", text_color="#e4e4e4", hover_color="#004600")
        else:
            self.btnFirewallPadrao.configure(text="FIREWALL DESATIVADO", fg_color="#D60000", text_color="#e4e4e4", hover_color="#B30000")
        
if __name__ == "__main__":
    main = Main()
    main.mainloop()
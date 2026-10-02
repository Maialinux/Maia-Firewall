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
        self.lbl_titulo_firewall = ctk.CTkLabel(master=self,text="MAIA FIREWALL",font=ctk.CTkFont(weight="bold",size=24))
        self.lbl_titulo_firewall.pack(ipady=50)
        self.lbl_tipo_de_protocolo = ctk.CTkLabel(master=self,text="Tipo de protocolo",font=ctk.CTkFont(weight="bold",size=14))
        self.lbl_tipo_de_protocolo.pack(side=ctk.TOP,anchor="center")
        self.cmb_tipo_de_protocolo = ctk.CTkComboBox(master=self,values=["TCP","UDP"],font=ctk.CTkFont(weight="bold",size=12),width=200,height=30)
        self.cmb_tipo_de_protocolo.pack(side=ctk.TOP,anchor="center")
        self.lbl_porta = ctk.CTkLabel(master=self,text="Porta",font=ctk.CTkFont(weight="bold",size=14))
        self.lbl_porta.pack(side=ctk.TOP,anchor="center", pady=(40,0))
        self.input_porta = ctk.CTkEntry(master=self,font=ctk.CTkFont(weight="bold",size=14))
        self.input_porta.pack(side=ctk.TOP,anchor="center",ipady=3)
        self.lbl_status_de_acesso = ctk.CTkLabel(master=self,text="Dar acesso ou bloquear",font=ctk.CTkFont(weight="bold",size=14))
        self.lbl_status_de_acesso.pack(side=ctk.TOP,anchor="center",pady=(50,0))
        self.cmb_status_de_acesso = ctk.CTkComboBox(master=self,values=["LIBERAR","BLOQUEAR"],width=200,height=30)
        self.cmb_status_de_acesso.pack(side=ctk.TOP,anchor="center")
        self.btn_aplicar = ctk.CTkButton(master=self,text="APLICAR",font=ctk.CTkFont(weight="bold",size=14),width=250,height=50,command=self.aplicar_regras)
        self.btn_aplicar.pack(side=ctk.TOP,anchor="center",pady=(60,0))  
        self.btnFirewallPadrao = ctk.CTkButton(master=self, text="ATIVAR FIREWALL PADRÃO",font=ctk.CTkFont(weight="bold",size=12),fg_color="#222222", text_color="#666666", hover_color="#333333", height=30, command=self.ativar_firewall)
        self.btnFirewallPadrao.pack(pady=20)

    def aplicar_regras(self):
        if self.cmb_tipo_de_protocolo.get():
            tipo_protocolo = self.cmb_tipo_de_protocolo.get()

        if self.input_porta.get() != "":
            input_porta = self.input_porta.get()    

        if self.cmb_status_de_acesso.get() == "LIBERAR":
            status_de_acesso = "ACCEPT"

        if self.cmb_status_de_acesso.get() == "BLOQUEAR":
            status_de_acesso = "DROP"         


        try:
            print(tipo_protocolo)
            print(input_porta)
            print(status_de_acesso)
            cmd_string1 = (      
                f"/usr/sbin/iptables -A INPUT -p {tipo_protocolo.lower()} -m {tipo_protocolo.lower()} --dport {input_porta} -j {status_de_acesso} "
                f"&& /usr/sbin/iptables-save > /etc/init.d/maiafirewall "
                f"&& chmod +x /etc/init.d/maiafirewall"
            )

            comando1 = [
                "pkexec",
                "bash",
                "-c",
                cmd_string1 
            ]

            subprocess.run(comando1, check=True)
           
            messagebox.showinfo(title="Sucesso", message="Nova regra adicionada e salva com sucesso!")
            continuar = messagebox.askyesno(title="Maia Firewall", message="Deseja continuar adicionando regras?")
            if not continuar:
                self.destroy()
            else:
                self.input_porta.delete(0, "end")
        except subprocess.CalledProcessError as e:
            messagebox.showerror(title="Erro", message=f"Falha ao executar o comando no iptables (código {e.returncode}).")
        except Exception as e:
            messagebox.showerror(title="Erro", message="Verifique os campos preenchidos.")
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
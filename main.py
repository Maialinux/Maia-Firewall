import os
import json
import subprocess
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
ctk.set_appearance_mode("dark")

ARQUIVO_ESTADO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "estado_firewall.json")

def carregar_estado():
    if os.path.exists(ARQUIVO_ESTADO):
        try:
            with open(ARQUIVO_ESTADO, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return bool(dados.get("ativado", False))
        except Exception:
            pass
    salvar_estado(False)
    return False

def salvar_estado(valor):
    with open(ARQUIVO_ESTADO, "w", encoding="utf-8") as f:
        json.dump({"ativado": valor}, f, indent=4)

ativado = carregar_estado()

class Main(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("Maia Firewall")
        self.geometry("400x600")
        # Ícone da janela (favicon)
        caminho_icone = os.path.join(os.path.dirname(__file__), "favicon.png")
        if os.path.exists(caminho_icone):
            self.icone = tk.PhotoImage(file=caminho_icone)
            self.iconphoto(False, self.icone)
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
        self.btnFirewallPadrao = ctk.CTkButton(master=self, text="FIREWALL DESATIVADO",font=ctk.CTkFont(weight="bold",size=12),fg_color="#D60000", text_color="#e4e4e4", hover_color="#B30000", height=30, command=self.ativar_firewall)
        self.btnFirewallPadrao.pack(pady=20)
        self.atualizar_visual_botao()

    def atualizar_visual_botao(self):
        if ativado:
            self.btnFirewallPadrao.configure(
                text="FIREWALL ATIVADO",
                fg_color="#006600",
                text_color="#e4e4e4",
                hover_color="#004600"
            )
        else:
            self.btnFirewallPadrao.configure(
                text="FIREWALL DESATIVADO",
                fg_color="#D60000",
                text_color="#e4e4e4",
                hover_color="#B30000"
            )

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

        servico_sistema = "/etc/systemd/system/maiawall.service"
        servico_local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maiawall.service")
        arquivo_regras = "/etc/init.d/maiafirewall"

        try:
            if ativado:
                comandos = []

                # Verifica se o arquivo maiawall.service existe em /etc/systemd/system/
                if os.path.exists(servico_sistema):
                    habilitado = subprocess.run(
                        ["systemctl", "is-enabled", "maiawall.service"],
                        capture_output=True, text=True
                    ).returncode == 0

                    ativo = subprocess.run(
                        ["systemctl", "is-active", "maiawall.service"],
                        capture_output=True, text=True
                    ).returncode == 0

                    if not habilitado:
                        comandos.append("systemctl enable maiawall.service")
                    if not ativo:
                        comandos.append("systemctl start maiawall.service")
                else:
                    # Copia o arquivo maiawall.service, recarrega o systemd, habilita e inicia
                    comandos.append(f'cp "{servico_local}" "{servico_sistema}"')
                    comandos.append("systemctl daemon-reload")
                    comandos.append("systemctl enable maiawall.service")
                    comandos.append("systemctl start maiawall.service")

                # Se o serviço estiver habilitado e iniciado e existir /etc/init.d/maiafirewall, restaura as regras
                if os.path.exists(arquivo_regras):
                    comandos.append(
                        f"systemctl is-enabled --quiet maiawall.service && "
                        f"systemctl is-active --quiet maiawall.service && "
                        f"/usr/sbin/iptables-restore < {arquivo_regras}"
                    )

                if comandos:
                    cmd_ativar = " && ".join(comandos)
                    subprocess.run(["pkexec", "bash", "-c", cmd_ativar], check=True)

                salvar_estado(ativado)
                self.atualizar_visual_botao()
                messagebox.showinfo(title="Maia Firewall", message="Firewall ativado com sucesso!")

            else:
                # Para e desabilita o serviço e reseta as regras do iptables
                cmd_desativar = (
                    "systemctl stop maiawall.service && "
                    "systemctl disable maiawall.service && "
                    "/usr/sbin/iptables -F && "
                    "/usr/sbin/iptables -X && "
                    "/usr/sbin/iptables -Z && "
                    "/usr/sbin/iptables -P INPUT ACCEPT && "
                    "/usr/sbin/iptables -P FORWARD ACCEPT && "
                    "/usr/sbin/iptables -P OUTPUT ACCEPT"
                )

                subprocess.run(["pkexec", "bash", "-c", cmd_desativar], check=True)

                salvar_estado(ativado)
                self.atualizar_visual_botao()
                messagebox.showinfo(title="Maia Firewall", message="Firewall desativado e regras resetadas!")

        except subprocess.CalledProcessError as e:
            ativado = not ativado  # Desfaz a troca de estado em caso de falha ou cancelamento
            messagebox.showerror(title="Erro", message=f"Falha ao alterar o estado do firewall (código {e.returncode}).")
        except Exception as e:
            ativado = not ativado
            messagebox.showerror(title="Erro", message=f"Ocorreu um erro: {e}")
        
if __name__ == "__main__":
    main = Main()
    main.mainloop()

# TALVEZ FIQUE NA CATEGORIA CONFIGURAÇÕES
class Persona:
    def __init__(self,nombres, apellidos , sexoLetra, cedulaPasaporte):
        self.nombresyApellidos = nombres + " " + apellidos
        self.cedula_o_pasaporte = cedulaPasaporte
        self.sexo = ""
        if(sexoLetra == 'M'):
            self.sexo = "masculino"
        elif(sexoLetra == 'F'):
            self.sexo = "femenino"

    
    def el_la_SR_SRA(self):
        if(self.sexo == "masculino"):
            return "el SR."
        elif(self.sexo == "femenino"):
            return "la SRA."

    def SR_SRA(self):
        if(self.sexo == "masculino"):
            return "SR."
        elif(self.sexo == "femenino"):
            return "SRA."

    def portador_a(self):
        if(self.sexo == "masculino"):
            return "portador"
        elif(self.sexo == "femenino"):
            return "portadora"

    def cedula_pasaporte(self):
        if(self.cedula_o_pasaporte.find('-') == -1):
            return f"del pasaporte No. {self.cedula_o_pasaporte}"
        else:
            return f"de la cedula de identidad y electoral No.{self.cedula_o_pasaporte}"
    
    def domiciliad_o_a(self):
        if(self.sexo == "masculino"):
            return "domiciliado"
        elif(self.sexo == "femenino"):
            return "domiciliada"

    def agrimensor_a(self):
        if(self.sexo == "masculino"):
            return "agrimensor"
        elif(self.sexo == "femenino"):
            return "agrimensora"

    def Propietario_a(self):
        if(self.sexo == "masculino"):
            return "Propietario"
        elif(self.sexo == "femenino"):
            return "Propietaria"

    def el_la(self):
        if(self.sexo == "masculino"):
            return "el"
        elif(self.sexo == "femenino"):
            return "la"

    def el_la_senior_seniora(self):
        if(self.sexo == "masculino"):
            return "el señor"
        elif(self.sexo == "femenino"):
            return "la señora"

    # NOTARIO

    def NOTARIO_A(self):
        if(self.sexo == "masculino"):
            return "NOTARIO"
        elif(self.sexo == "femenino"):
            return "NOTARIA"

    def Licdo_Licda(self):
        if(self.sexo == "masculino"):
            return "Licdo"
        elif(self.sexo == "femenino"):
            return "Licda"

    def Registrado_a(self):
        if(self.sexo == "masculino"):
            return "Registrado"
        elif(self.sexo == "femenino"):
            return "Registrada"


class Conjuncion:
    def __init__(self,cliente_01,cliente_02,uno):
        self.cliente_01 = cliente_01
        self.cliente_02 = cliente_02
        self.uno = uno

    def y_no(self):
        if(self.uno):
            return ""
        else:
            return " y "

    def domiciliado_s_residente_s(self):
        if(self.uno):
            return str(self.cliente_01.domiciliad_o_a() + " y residente")
        else:
            return "domiciliados y residentes"

    def residente_s(self):
        if(self.uno):
            return "residente"
        else:
            return "residentes"

    def el_la_los_SR_SRA_SRES(self):
        if(self.uno):
            return self.cliente_01.el_la_SR_SRA()
        else:
            return "los SRES."

    def el_la_los_senior_seniora_seniores(self):
        if(self.uno):
            return self.cliente_01.el_la_senior_seniora()
        else:
            return "los señores"

    def contrataron_contrato(self):
        if(self.uno):
            return "contrato"
        else:
            return "contrataron"

    def ambos_no(self):
        if(self.uno):
            return ""
        else:
            return 'ambos'
    
    def coma_no(self):
        if(self.uno):
            return ""
        else:
            return ','

    #-----------------------

    def el_SR_la_SRA_CLIENTE_01(self):
        return f"{self.cliente_01.el_la_SR_SRA()} {self.cliente_01.nombresyApellidos.upper()}"

    def SR_SRA_CLIENTE_01(self):
        return f"{self.cliente_01.SR_SRA()} {self.cliente_01.nombresyApellidos.upper()}"

    def portador_cliente_01(self):
        return self.cliente_01.portador_a()
    
    def del_pasaporte_de_la_cedula_cliente_01(self):
        return self.cliente_01.cedula_pasaporte()

    def el_SR_la_SRA_CLIENTE_02(self):
        if(self.uno):
            return ""
        else:
            return f" {self.cliente_02.el_la_SR_SRA()} {self.cliente_02.nombresyApellidos.upper()} "
    
    def SR_SRA_CLIENTE_02(self):
        return f"{self.cliente_02.SR_SRA()} {self.cliente_02.nombresyApellidos.upper()}"

    def portador_cliente_02(self):
        if(self.uno):
            return ""
        else:
            return f" {self.cliente_02.portador_a()} "

    def del_pasaporte_de_la_cedula_cliente_02(self):
        if(self.uno):
            return ""
        else:
            return f" {self.cliente_02.cedula_pasaporte()} "

    def cliente_01_r(self):
        return f" {self.cliente_01.nombresyApellidos} "

    def cliente_02_r(self):
        if(self.uno):
            return ""
        else:
            return f" {self.cliente_02.nombresyApellidos} "
    
    def Propietario02(self):
        if(self.uno):
            return ""
        else:
            return self.cliente_02.Propietario_a()

    def coma_espacio_client02(self):
        if(self.uno):
            return ""
        else:
            return ", "

    
    def mostrarTexto(self):
        print(f"{self.el_SR_la_SRA_cliente_01()} {self.portador_cliente_01()} {self.del_pasaporte_de_la_cedula_cliente_01()} {self.y_no()} {self.el_SR_la_SRA_cliente_02()} {self.portador_cliente_02()} {self.del_pasaporte_de_la_cedula_cliente_02()}, {self.ambos_no()} {self.domiciliado_s()} y {self.residente_s()} en el")
        

from crud import return_item_id_type
from math import inf

# VERIFICAR O QUE PRECISA!!!  Metade pode ser mandado direto para o DB!!!!!!!!!!!!!
class Item:

    def __init__(self, item_id, name, item_type, slots):
        self.id = item_id  # OK
        self.name = name  # OK
        self.i_type = item_type  # OK
        self.slots = slots  # OK
        self.v_d_low = inf  # OK
        self.v_d_low_quantity = 0  # OK
        self.v_d_avg = 0  # OK
        self.v_d_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.v_w_low = 0
        self.v_w_avg = 0  # Ok
        self.v_w_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.v_m_low = 0
        self.v_m_avg = 0  # OK
        self.v_m_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.v_h_avg = 0  # OK
        self.v_h_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.b_d_high = 0  # OK
        self.b_d_high_quantity = 0  # OK
        self.b_d_avg = 0  # OK
        self.b_d_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.b_w_high = 0
        self.b_w_avg = 0  # OK
        self.b_w_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.b_m_high = 0
        self.b_m_avg = 0  # OK
        self.b_m_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.b_h_avg = 0  # OK
        self.b_h_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.b_store_id = []  # OK
        self.b_store_date = []
        self.v_store_id = []  # OK
        self.v_store_date = []

    def better_b_price(self, price, quantity, store_id, store_date):
        self.b_d_high, self.b_d_high_quantity = price, quantity
        self.b_store_id = [store_id]
        self.b_store_date = [store_date]

    def better_v_price(self, price, quantity, store_id, store_date):
        self.v_d_low, self.v_d_low_quantity = price, quantity
        self.v_store_id = [store_id]
        self.v_store_date = [store_date]

    def price_b_quantity(self, quantity, store_id, store_date):
        self.b_d_high_quantity += quantity
        self.b_store_id.append(store_id)
        self.b_store_date.append(store_date)

    def price_v_quantity(self, quantity, store_id, store_date):
        self.v_d_low_quantity += quantity
        self.v_store_id.append(store_id)
        self.v_store_date.append(store_date)

    def set_v_d_avg(self, value):
        self.v_d_avg = value

    def set_v_w_avg(self, value):
        self.v_w_avg = value

    def set_v_m_avg(self, value):
        self.v_m_avg = value

    def set_v_h_avg(self, value):
        self.v_h_avg = value

    def set_b_d_avg(self, value):
        self.b_d_avg = value

    def set_b_w_avg(self, value):
        self.b_w_avg = value

    def set_b_m_avg(self, valeu):
        self.b_m_avg = valeu

    def set_b_h_avg(self, value):
        self.b_h_avg = value

    #\/ Testar
    def set_v_w_low(self, value):
        self.v_w_low = value

    def set_v_m_low(self, value):
        self.v_m_low = value

    def set_b_w_high(self, value):
        self.b_w_high = value

    def set_b_m_high(self, value):
        self.b_m_high = value


    def reset_day(self):
        """
        # Reseta os valores
        """
        self.v_d_low = inf  # Valor minimo atual
        self.v_d_low_quantity = 0  # Quantia
        self.v_d_avg = 0  # Media do Dia atnerior
        self.v_d_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.v_w_low = 0 # Valor minimo ultimos sete_dias
        self.v_w_avg = 0  # Valor Médio ultimos 7 dias
        self.v_w_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.v_m_low = 0 #Ok
        self.v_m_avg = 0  # OK
        self.v_m_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.v_h_avg = 0  # OK
        self.v_h_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.b_d_high = 0  # OK
        self.b_d_high_quantity = 0  # OK
        self.b_d_avg = 0  # OK
        self.b_d_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.b_w_high = 0 # OK
        self.b_w_avg = 0  # OK
        self.b_w_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.b_m_high = 0 # OK
        self.b_m_avg = 0  # OK
        self.b_m_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.b_h_avg = 0  # OK
        self.b_h_avg_x = 0 # FALTA IMPLEMENTAR!!
        self.b_store_id = []  # OK
        self.v_store_id = []  # OK




items = {item_id: Item(item_id, name, item_type, slots) for item_id, name, item_type, slots in return_item_id_type()}


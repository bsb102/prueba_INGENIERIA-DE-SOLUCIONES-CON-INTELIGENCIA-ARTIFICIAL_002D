import random
from typing import Literal


def retrieve_user_status(user_id: str) -> str:
    """
    Simula la consulta a la base de datos de clientes para obtener el estado de lealtad y reservas activas.
    Utilizada por el Router para priorización y adaptación (IE5, IE6).
    """
    if user_id == "VIP_LTM123":
        return "Usuario VIP con reserva activa (ID LTM456) para el 15/11/2025. Nivel Platinum. Prioridad alta."
    return "Usuario estándar, sin reservas activas recientes."

def update_flight_booking(id: str, new_date: str) -> str:
    """
    Simula una transacción de escritura en el sistema de reservas de LATAM.
    Utilizada por el Agente de Reservas (IE1).
    """
    if random.random() < 0.9:  
        return f"Éxito: La reserva {id} ha sido modificada correctamente para el {new_date}. Se envió confirmación por email."
    else:
        return f"Error de Sistema: No se pudo completar la transacción para la reserva {id}. Intente más tarde o solicite un Handoff humano."

def get_local_regulation(country_code: str) -> str:
    """
    Simula la consulta a la base de datos de regulaciones locales (RAG simulado).
    Utilizada por el Agente de Reclamos (IE4).
    """
    if country_code.upper() == "CHILE":
        return "Regulación Chilena: El plazo máximo para reclamos por demora de vuelo mayor a 3 horas es de 7 días hábiles. La compensación máxima es UF 10."
    elif country_code.upper() == "BRASIL":
        return "Regulación ANAC Brasil: Compensación inmediata por cancelaciones, incluyendo reacomodación o reembolso total, sin plazo de espera."
    else:
        return "Regulación estándar IATA aplicada. Especifique país para detalles locales."

def get_baggage_policy(type: Literal["mano", "documentada"]) -> str:
    """
    Simula una consulta de RAG a la documentación de políticas.
    Utilizada por el Agente Router (IE4 - RAG).
    """
    if type == "mano":
        return "Política de equipaje de mano: Máximo 8kg, dimensiones 55cm x 35cm x 25cm. Se aplica tarifa si excede."
    elif type == "documentada":
        return "Política de equipaje documentado: Depende de la tarifa y el destino. Para tarifas 'Light', el primer equipaje tiene costo adicional."
    return "Especifique si es equipaje de mano o documentada para obtener la política precisa."

def log_interaction_data(dialogue: str, resolution: str) -> str:
    """
    Simula la función del Agente de Análisis (Oculto) para recopilar insights (IE1, IE6).
    """
    sentiment = "Positivo" if "gracias" in dialogue.lower() and "éxito" in resolution.lower() else "Negativo"
    
    print(f"\n[ANÁLISIS]: Interacción registrada. Sentimiento detectado: {sentiment}. Resolución: {resolution[:30]}...")
    return f"Registro de datos completado. Sentimiento: {sentiment}"

def escalate_to_human_agent(case_data: str) -> str:
    """
    Simula la decisión de Handoff (traspaso) a un agente humano cuando la IA no puede resolver (IE6).
    """
    print(f"\n[DECISIÓN CRÍTICA]: ¡ESCALADA NECESARIA!")
    return f"Traspaso a Agente Humano iniciado. Hemos creado el caso #CRT{random.randint(1000, 9999)}. Un humano se comunicará contigo en los próximos 5 minutos para resolver: {case_data[:50]}..."


if __name__ == '__main__':
    print("Prueba de herramientas:")
    print(get_local_regulation("CHILE"))
    print(update_flight_booking("LTM999", "30/11/2025"))
    log_interaction_data("Cliente molesto por el retraso.", "Se compensó con un voucher.")

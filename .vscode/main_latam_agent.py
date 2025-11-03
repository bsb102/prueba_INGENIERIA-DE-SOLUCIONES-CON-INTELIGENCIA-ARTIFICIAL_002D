import autogen
import os

from tools import update_flight_booking, get_local_regulation, get_baggage_policy, log_interaction_data, retrieve_user_status, escalate_to_human_agent

if "GEMINI_API_KEY" not in os.environ:
    print("ERROR: La variable de entorno GEMINI_API_KEY no está configurada.")
    print("Por favor, configúrala antes de ejecutar el script.")
    exit()


config_list_gemini = [
    {
        "model": "gemini-2.5-pro",
        "api_key": os.environ["GEMINI_API_KEY"],
        "base_url": "https://api.gemini.ai/v1", 
    }
]

llm_config = {
    "timeout": 120,
    "config_list": config_list_gemini,
    "temperature": 0.1,
    "cache_seed": 42
}

router_agent = autogen.UserProxyAgent(
    name="Agente_Router_LATAM",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    human_input_mode="NEVER",  
    max_consecutive_auto_reply=15,
    system_message=(
        "Eres el Agente Principal de Atención al Cliente de LATAM. Tu rol es clasificar la intención del usuario "
        "y derivar la tarea al Agente Especializado correspondiente. Si la consulta es de 'reservas' o 'reclamos', "
        "debes invocar al agente adecuado para que use la herramienta. Después de la resolución, "
        "debes usar la herramienta 'log_interaction_data' antes de responder al usuario. "
        "Si detectas un problema grave, una consulta muy técnica o si la herramienta devuelve un 'Error de Sistema', "
        "debes usar inmediatamente la función 'escalate_to_human_agent'. Usa 'retrieve_user_status' al inicio de cada conversación para contexto."
    ),
    code_execution_config=False,
    llm_config=llm_config
)

router_agent.register_function(
    function_map={
        "get_baggage_policy": get_baggage_policy, 
        "retrieve_user_status": retrieve_user_status,
        "escalate_to_human_agent": escalate_to_human_agent,
        "log_interaction_data": log_interaction_data
    }
)


reservas_agent = autogen.AssistantAgent(
    name="Reservas_Agent",
    system_message=(
        "Eres el Agente de Reservas de LATAM. Eres experto en gestión de itinerarios. "
        "Tu única función es ejecutar transacciones (ej. cambio de vuelo) usando la herramienta 'update_flight_booking'. "
        "Debes reportar el resultado al Agente_Router_LATAM y finalizar tu tarea, incluyendo el mensaje TERMINATE."
    ),
    llm_config=llm_config,
)
reservas_agent.register_function(
    function_map={"update_flight_booking": update_flight_booking}
)

reclamos_agent = autogen.AssistantAgent(
    name="Reclamos_Agent",
    system_message=(
        "Eres el Agente de Reclamos de LATAM. Eres experto en regulaciones aéreas. "
        "Utiliza la herramienta 'get_local_regulation' para dar una respuesta fundamentada al Agente_Router_LATAM. "
        "Debes reportar el resultado al Agente_Router_LATAM y finalizar tu tarea, incluyendo el mensaje TERMINATE."
    ),
    llm_config=llm_config,
)
reclamos_agent.register_function(
    function_map={"get_local_regulation": get_local_regulation}
)


analisis_agent = autogen.AssistantAgent(
    name="Analisis_Agent",
    system_message="Eres un agente de BI. Tu única función es registrar datos usando 'log_interaction_data'. Finaliza con TERMINATE.",
    llm_config=llm_config
)
analisis_agent.register_function(
    function_map={"log_interaction_data": log_interaction_data}
)


groupchat = autogen.GroupChat(
    agents=[router_agent, reservas_agent, reclamos_agent, analisis_agent],
    messages=[],
    max_round=20,
    speaker_selection_method="auto"  
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)


print("\n" + "="*50)
print("  Simulador de Agente Funcional LATAM (AutoGen + Gemini)")
print("="*50)
print("Instrucciones: El Agente_Router_LATAM gestionará la conversación.")
print("  - Prueba de RAG/Consulta: '¿Cuál es la política de equipaje de mano?'")
print("  - Prueba de Escritura/Transacción: 'Necesito cambiar mi vuelo con ID LTM456 al 25 de diciembre.'")
print("  - Prueba de Decisión Adaptativa (Handoff): 'El sistema me devolvió un error 404, ayuda'")
print("  - Escribe 'salir' para terminar.")
print("="*50)


while True:
    user_query = input("\n[Usuario]: ")
    if user_query.lower() == 'salir':
        break
    
    router_agent.initiate_chat(
        manager,
        message=user_query,
        clear_history=True 
    )

print("\nSimulación de agente finalizada. ¡Éxito en la orquestación! TERMINATE")

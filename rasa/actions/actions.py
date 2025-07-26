version: "3.1"

intents:
  - agendar_consulta
  - negar
  - affirm
  - greet
  - goodbye
  - expressar_sintoma

entities:
  - motivo_consulta_tipo
  - motivo_consulta
  - especialidade
  - nome_medico
  - data_consulta
  - hora_consulta

slots:
  motivo_consulta_tipo:
    type: text
    mappings:
      - type: from_text
  motivo_consulta:
    type: text
    mappings:
      - type: from_text
  especialidade:
    type: text
    mappings:
      - type: from_text
  nome_medico:
    type: text
    mappings:
      - type: from_text
  data_consulta:
    type: text
    mappings:
      - type: from_text
  hora_consulta:
    type: text
    mappings:
      - type: from_text

responses:
  utter_greet:
    - text: "Olá! Em que posso ajudar hoje?"

  utter_goodbye:
    - text: "Tchau! Até breve."

  utter_agendamento_cancelado:
    - text: "Agendamento cancelado. Se quiser tentar de novo, é só me avisar!"

  utter_submit_agendamento_consulta_form:
    - text: "Sua consulta foi agendada com sucesso. Obrigado!"

forms:
  agendamento_consulta_form:
    required_slots:
      - motivo_consulta_tipo
      - motivo_consulta
      - especialidade
      - nome_medico
      - data_consulta
      - hora_consulta

actions:
  - action_perguntar_llm
  - action_submit_agendamento
  - validate_agendamento_consulta_form
  - action_confirmar_agendamento
  - action_reset_slots

session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true

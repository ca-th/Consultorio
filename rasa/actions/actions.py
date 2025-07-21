from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import os
import mysql.connector

DB_HOST = os.environ.get("localhost", "localhost")
DB_USER = os.environ.get("root",, "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "cat1234")
DB_NAME = os.environ.get("DB_NAME", "consultorio")
DB_PORT = os.environ.get("DB_PORT", "3306")

class ActionCheckExistingUser(Action):
    def name(self) -> Text:
        return "action_check_existing_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Obtendo o valor do slot 'cadastro_pessoa_f' (assumindo que é onde o CPF será armazenado)
        user_cpf = tracker.get_slot("cadastro_pessoa_f")

        user_exists = False
        message_to_user = ""

        if not user_cpf:
            message_to_user = "Não consegui identificar o CPF. Poderia informar seu CPF, por favor?"
            dispatcher.utter_message(text=message_to_user)
            return [SlotSet("user_exists", None)]

        # remover pontos, traços, etc. para comparar apenas os dígitos
        cleaned_cpf = ''.join(filter(str.isdigit, user_cpf))

        
        if len(cleaned_cpf) != 11:
            message_to_user = "O CPF informado não parece ter 11 dígitos. Por favor, digite seu CPF novamente sem pontos ou traços."
            dispatcher.utter_message(text=message_to_user)
            return [SlotSet("user_exists", False)] # CPF inválido

        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                port=DB_PORT
            )
            cursor = conn.cursor()

            #Consulta ao Banco de Dados MySQL usando a coluna 'cpf' ---
            #Confirme que 'cpf' é o nome exato da sua nova coluna na tabela 'usuarios'.
            query = "SELECT COUNT(*) FROM usuarios WHERE cpf = %s"
            cursor.execute(query, (cleaned_cpf,)) # Use %s como placeholder para MySQL
            result = cursor.fetchone()[0]

            if result > 0:
                user_exists = True
                message_to_user = "CPF encontrado em nosso cadastro. Bem-vindo(a)!"
            else:
                user_exists = False
                message_to_user = "CPF não encontrado em nosso cadastro. Por favor, faça seu cadastro."

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            user_exists = False
            message_to_user = "Desculpe, tive um problema técnico ao verificar seu cadastro. Por favor, tente novamente mais tarde."
            print(f"Erro no MySQL: {err}")
        except Exception as e:
            user_exists = False
            message_to_user = "Desculpe, ocorreu um erro inesperado ao verificar seu cadastro. Por favor, tente novamente mais tarde."
            print(f"Erro inesperado: {e}")

        dispatcher.utter_message(text=message_to_user)
        return [SlotSet("user_exists", user_exists)]
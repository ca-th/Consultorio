from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionCheckExistingUser(Action):
    def name(self) -> Text:
        return "action_check_existing_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_cpf = tracker.get_slot("cadastro_pessoa_f")
        user_exists = user_cpf == '04536206124'
        return [SlotSet("user_exists", user_exists)]
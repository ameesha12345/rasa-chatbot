# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

class ActionRecommendPlaces(Action):
    def name(self) -> Text:
        return "action_recommend_places"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        # Load the dataset
        data_path = 'Top Indian Places to Visit.csv'
        places_df = pd.read_csv(data_path)
        
        # Get the city from slot
        city = tracker.get_slot("city")
        
        if not city:
            dispatcher.utter_message(text="Please specify the city you're interested in.")
            return []
        
        # Filter places based on the city
        filtered_places = places_df[places_df['City'].str.lower() == city.lower()]
        
        # Check if there are any places for the specified city
        if filtered_places.empty:
            dispatcher.utter_message(text=f"Sorry, I couldn't find any places to visit in {city}.")
            return []
        
        # Generate a response with recommended places
        recommendations = []
        for index, row in filtered_places.iterrows():
            recommendations.append(f"{row['Name']} - {row['Type']} (Rating: {row['Google review rating']})")
        
        # Send the list of places to the user
        response_message = f"Top places to visit in {city}:\n" + "\n".join(recommendations[:5])
        dispatcher.utter_message(text=response_message)

        return []

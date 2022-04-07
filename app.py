from flask import Flask, request
from flask_cors import CORS, cross_origin
from google.cloud import dialogflow

project_id = 'newagent-hvgx'
session_id = '123456789'  # generate random
language_code = 'en-US'

app = Flask(__name__)
CORS(app)


# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
# processing the request from dialogflow
def processRequest():
    global button
    event_data = request.get_json(force=True,silent=True)

    if event_data['type'] == 'CARD_CLICKED':
        action_name = event_data['action']['actionMethodName']
        resp, button = detect_intent_texts(text=action_name)

    # if (req.body.type == "CARD_CLICKED"):
    #   action_name = req.body.action.actionMethodName

    return resp, button


def detect_intent_texts(text, project_id='newagent-hvgx', session_id='123456789', language_code='en-US'):
    """Returns the result of detect intent with texts as inputs.

        Using the same `session_id` between requests allows continuation
        of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    # output_text = response.query_result.fulfillmentText
    output = response.query_result.fulfillmentMessages
    output_text, payload = output[0], output[1]["payload"]
    payload = response.query_result.fulfillmentMessages.payload

    return output_text, payload


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 

"""{
  "responseId": "838f1d78-4298-444c-a4ad-6901e35f7001-96b8a746",
  "queryResult": {
    "queryText": "hi",
    "parameters": {
      "query": ""
    },
    "allRequiredParamsPresent": True,
    "fulfillmentText": "Hi! How are you doing?",
    "fulfillmentMessages": [
      {
        "text": {
          "text": [
            "Hi! How are you doing?"
          ]
        },
        "platform": "GOOGLE_HANGOUTS"
      },
      {
        "payload": {
          "hangouts": {
            "header": {
              "title": "TOPICS"
            },
            "sections": [
              {
                "widgets": [
                  {
                    "buttons": [
                      {
                        "textButton": {
                          "onClick": {
                            "action": {
                              "actionMethodName": "Methodologies_Agile"
                            }
                          },
                          "text": "project management"
                        }
                      },
                      {
                        "textButton": {
                          "text": "project methodologies",
                          "onClick": {
                            "action": {
                              "actionMethodName": "agile"
                            }
                          }
                        }
                      },
                      {
                        "textButton": {
                          "onClick": {
                            "action": {
                              "actionMethodName": "kanban"
                            }
                          },
                          "text": "project life cycle"
                        }
                      }
                    ]
                  }
                ]
              }
            ]
          }
        },
        "platform": "GOOGLE_HANGOUTS"
      },
      {
        "text": {
          "text": [
            "Hi! How are you doing?"
          ]
        }
      },
      {
        "payload": {
          "richContent": [
            [
              {
                "type": "list",
                "subtitle": "Introduction to project management",
                "title": "Project Management",
                "event": {
                  "languageCode": "en-US",
                  "parameters": {},
                  "name": "initial"
                }
              },
              {
                "type": "divider"
              },
              {
                "title": "Project Management Methodologies",
                "type": "list",
                "event": {
                  "name": "methodologies",
                  "parameters": {},
                  "languageCode": "en"
                }
              },
              {
                "type": "divider"
              },
              {
                "subtitle": "Phases of a project",
                "type": "list",
                "event": {
                  "parameters": {},
                  "name": "phases_project_life_cycle",
                  "languageCode": "en-US"
                },
                "title": "Project Life Cycle"
              }
            ]
          ]
        }
      }
    ],
    "outputContexts": [
      {
        "name": "projects/newagent-hvgx/locations/global/agent/sessions/903e39a2-80f7-a5ac-e664-697cef7ccac0/contexts/await_choice",
        "lifespanCount": 1,
        "parameters": {
          "query": "",
          "query.original": ""
        }
      }
    ],
    "intent": {
      "name": "projects/newagent-hvgx/locations/global/agent/intents/cc51e086-51a6-419d-b3b0-3f028261e22b",
      "displayName": "Default Welcome Intent"
    }"""
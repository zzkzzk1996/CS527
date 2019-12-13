# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import requests
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Alexa My Cart! What can I do for you?"
        reprompt_txt = "You can try select order from orders."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_txt)
                .response
        )


class ProductInfoIntentHandler(AbstractRequestHandler):
    """Handler for finding the information of a particular product."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ProductInfoIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        information = slots["information"].value
        id_ = slots["id"].value
        # different information cases
        if information == 'name':
            sql = f'SELECT product_id, product_name FROM products WHERE product_id = {id_}'
        elif information == 'location':
            sql = f'SELECT p.product_id, a.aisle FROM products p INNER JOIN aisles a ON a.aisle_id = p.aisle_id WHERE product_id = {id_}'
        elif information == 'department':
            sql = f'SELECT p.product_id, d.department FROM products p INNER JOIN departments d ON d.department_id = p.department_id WHERE product_id = {id_}'

        rsp = requests.get('http://cs527.zekunzhang.net./alexa', params={'query':sql})
        if rsp.status_code == requests.codes.ok:
            speak_output = 'Sure. Here are the results.'
        else:
            speak_output = 'Sorry. I got a problem with status code: {}.'.format(str(rsp.status_code))
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class FindProductIntentHandler(AbstractRequestHandler):
    """Handler for finding the most/least popular products."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("FindProductIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        order = slots["order"].value
        number = slots["number"].value

        sql = 'SELECT product_name, COUNT(*) ' + \
                'FROM order_products op ' + \
                'INNER JOIN products p ' + \
                'ON p.product_id = op.product_id ' + \
                'GROUP BY p.product_id ' + \
                'ORDER BY count(*) '
        if order == 'most': sql += 'DESC '
        if number: 
            sql += f'LIMIT {number}'
        else:
            sql += 'LIMIT 1'

        rsp = requests.get('http://cs527.zekunzhang.net./alexa', params={'query':sql})
        if rsp.status_code == requests.codes.ok:
            speak_output = 'Sure. Here are the results.'
        else:
            speak_output = 'Sorry. I got a problem with status code: {}.'.format(str(rsp.status_code))
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


def Helper(attributes, flag):
    attri_res = ""
    # flag is true, deal with attribute, else, deal with table
    aggregate = ['max', 'min', 'count', 'average']
    if flag:
        attri = attributes.strip().split(' ')
        i = 0
        dic = {'aisle': {'id': ['aisle_id', 1]}, 
                'department': {'id': ['department_id', 1]},
                'product': {'id': ['product_id', 1],
                            'name': ['product_name', 1]},
                'user': {'id': ['user_id', 1]},
                'order': {'id': ['order_id', 1],
                            'day': ['order_dow', 3],
                            'hour': ['order_hour_of_day', 3]},
                'add': {'to': ['add_to_cart_order', 3]},
                'days': {'since': ['days_since_prior_order', 3]}}
        while i < len(attri):
            # transform "star" to "*"
            if attri[i] == 'star': attri[i] = '*'
            curr = ''
            pre = i-1
            if dic.get(attri[i]):
                if i+1 < len(attri) and dic[attri[i]].get(attri[i+1]):
                    l = dic[attri[i]][attri[i+1]]
                    curr = l[0]
                    i += l[1]
            if pre > -1 and attri[pre] in aggregate:
                if not curr == '':
                    attri_res += attri[pre] + '(' + curr + ')'
                else:
                    attri_res += attri[pre] + '(' + attri[i] + ')'
            else:
                if not curr == '':
                    attri_res += curr
                elif not attri[i] in aggregate:
                    attri_res += attri[i]
                else:
                    i += 1
                    continue                    
            attri_res += ','
            i += 1
    else:
        for item in attributes.strip().split(','):
            attri_res += item.strip().replace(' ', '_') + ','
    return attri_res[:-1]


class QueryIntentHandler(AbstractRequestHandler):
    """Handler for the general SQL queries."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("QueryIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        function = slots["function"].value
        attribute = Helper(slots["attribute"].value, True)
        table = Helper(slots["table"].value, False)
        
        sql = ''
        # different query funtions
        if function == "select":
            sql += f'{function} {attribute} from {table} '
        '''
        elif function == "update":
            speak_output = '{function} {table} set {attribute} = '.format(attribute=attribute,
                                                                        function=function,
                                                                      table=table)
        elif function == "delete":
            speak_output = '{function} from {table} where {attribute} = '.format(attribute=attribute,
                                                                                function=function,
                                                                                table=table)
        elif function == "insert into":
            speak_output = '{function} {table} values {attribute} '.format(attribute=attribute,
                                                                            function=function,
                                                                            table=table)
        '''
        # "where" implementation
        if slots["where"].value:
            operator = slots["operator"].value
            if operator in ["larger than","greater than","is greater than","is larger than"]:
                operator = '>'
            elif operator in ["smaller than","less than","is smaller than","is less than"]:
                operator = '<'
            elif operator in ["equal to","is","equals to"]:
                operator = '='
            elif operator in ["not equal to","doesn't equal to","does not equal to"]:
                operator = '!='
            value = slots["value"].value
            target_attr = slots["target_attr"].value
            sql += f'where {target_attr} {operator} {value} '

        rsp = requests.get('http://cs527.zekunzhang.net./alexa', params={'query':sql})
        if rsp.status_code == requests.codes.ok:
            speak_output = 'OK. Your request is successfully sent!'
        else:
            speak_output = f'Sorry. I got a problem with error code {rsp.status_code}.'
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(QueryIntentHandler())
sb.add_request_handler(ProductInfoIntentHandler())
sb.add_request_handler(FindProductIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()


#!/usr/bin/env python3
from dialogs.dialogs import *
from nl import *
from nl import nlp
import random


#################### LIST OF INTENTS ############################


def intent_has_verb_and_player(context):
    return context.has_verb and context.has_player_name


def intent_no_verb(context):
    return context.has_verb == False


def intent_not_has_budget(context):
    return context.has_budget == False


def intent_has_only_verb(context):
    return context.has_verb \
           and not context.has_attribute \
           and not context.has_player_role \
           and not context.has_quantifier \
           and not context.has_budget \
           and not context.has_player_name


def intent_is_ready_for_seach(context):
    return context.has_verb \
           and context.has_attribute \
           and context.has_player_role \
           and context.has_quantifier \
           and context.has_budget \
           and context.category_verb == "find"


def intent_is_quit(context):
    return context.category_verb == "quit"


def intent_is_invalid(context):
    return not context.request_did_success


def intent_is_missing_role(context):
    return context.has_player_role is False


def intent_is_missing_attribute(context):
    return context.has_attribute is False


def intent_is_missing_quantifier(context):
    return context.has_quantifier is False


##############################################################


def process_logic(context):
    process_intents(context)
    return context


def process_intents(context):
    context.trace()

    dialog = DialogManager()

    if intent_is_quit(context):
        context.request_is_still_active = False
        dialog.processDialog(ID_GOODBYE)
        return context

    if intent_is_invalid(context):
        dialog.processDialog(ID_INTENT_NOT_CLEAR)

    if intent_no_verb(context):
        dialog.processDialog(ID_NO_VERB)
        return context

    if intent_has_only_verb(context):
        dialog.processDialog(ID_WELCOME)

    if intent_has_verb_and_player(context):
        dialog.processDialog(ID_FIND_HAS_PLAYER_NAME, [context.player_name])
        return context

    if intent_not_has_budget(context):
        while intent_not_has_budget(context):
            dialog.processDialog(ID_ASK_FOR_BUDGET)
            budget = input()
            if budget.isdigit():
                dialog.processDialog(ID_THANKS)
                context.budget_amount = budget
                context.has_budget = True
            else:
                dialog.processDialog(ID_BUDGET_NOT_VALID)

    if intent_is_missing_role(context):
        dialog.processDialog(ID_ASK_PLAYER_ROLE)
        return context

    if intent_is_missing_attribute(context):
        dialog.processDialog(ID_ASK_ATTRIBUTE, [context.category_player_role])
        return context

    if intent_is_missing_quantifier(context):
        dialog.processDialog(ID_ASK_QUANTIFIER, [context.category_attribute, context.category_player_role])
        return context

    if intent_is_ready_for_seach(context):
        dialog.processDialog(ID_FIND_REQUEST_IS_READY, [context.category_player_role, context.quantifier_attribute,
                                                        context.category_attribute])
        context.request_is_still_active = False

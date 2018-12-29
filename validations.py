#!/usr/bin/env python
import tkMessageBox


def validateNumerics(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    if (action == '1'):
        if text in '0123456789':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
    else:
        return True


def validateEntries(algoValue, reqPreSec, servers):
    if algoValue == 'None':
        tkMessageBox.showerror('Algorithm NOT selected', 'Please select an algorithm to proceed')
        return False
    elif reqPreSec == 0 | servers == 0:
        tkMessageBox.showerror('Invalid Parameters', 'Please select no of servers and requests per sec to proceed')
        return False
    else:
        return True

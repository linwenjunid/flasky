from flask import current_app

def myfilter(arg):
    for i,item in enumerate(arg):
        arg[i]=arg[i].replace('\r\n','').replace('\t','')
    return arg

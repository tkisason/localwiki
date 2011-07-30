#!/usr/bin/python

from bottle import route,run,get,post,request
import shelve, string,re

db = shelve.open("database",writeback=True)

style = "" # this element will be added in every view. Add your custom javascript/css here

def wikify(data):
    out = ""
    keys = dict(zip(map(lambda x: string.lower(x),db.keys()),db.keys()))
    for elem in data.split(" "):
        le = string.lower(elem)
        if le in keys.keys():
            out += '<a href="/'+keys[le]+'">'+elem+'</a>'+" "
        else:
            out += elem+" "
    return out 
    

def markup(data):
    r = re.compile(r"(http://[^ ]+)")
    data = style+wikify(data)
    data = r.sub(r'<a href="\1">\1</a>', data) 
    return str(data.replace("\n","<br>"))

@route("/")
def print_pages():
    html =""
    for elem in db:
#        html += "<a href="+markup(elem)+">"+markup(elem)+"</a><br>"
        html += markup(elem) + "<br>"
    return html

@get("/:name")
def get_page(name):
    if db.has_key(name):
        return markup(db[name])
    else:
        return ""

@get("/:name/:command")
def node(name,command):
    if db.has_key(name):
        cont = db[name]
    else:
        cont = ""
    if command == "edit":
        return str('<form method="POST"><textarea name="content" type="text" rows="40" cols="120">'+cont+'</textarea><br><input type="submit" value="submit" /></form>')
    elif command == "del":
        db.pop(name)
        return str("Deleted: "+name)
    else:
        return "Unknown command: ", command

@post('/:name/:command')
def node_submit(name,command):
    cont  = request.forms.get('content')
    db[name] = cont
    return markup(cont)


run(host='localhost', port=8080)
print "[+] Flushing data to db..."
db.close()
print "[+] Done, bye"


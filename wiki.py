#!/usr/bin/python

from bottle import route, run, get, post, request, redirect
import shelve
import re


def wikify(data):
    out = ""
    keys = dict(zip([x.lower() for x in db.keys()], db.keys()))
    for elem in data.split(" "):
        le = elem.lower()
        if le in keys.keys():
            out += '<a href="/'+keys[le]+'">'+elem+'</a>'+" "
        else:
            out += r.sub(r'<a href="\1">\1</a>', elem)+" "
    return out


def markup(data):
    data = style+wikify(data)
    return str(data.replace("\n", "<br>"))


@route("/")
def print_pages():
    html = ""
    for elem in db:
        html += markup(elem) + "<br>"
    return html


@get("/:name")
def get_page(name):
    if name in db:
        return markup(db[name])
    else:
        return redirect("/%s/edit" % name)


@get("/:name/:command")
def node(name, command):
    if name in db:
        cont = db[name]
    else:
        cont = ""
    if command == "edit":
        return str('<form method="POST"><textarea name="content" type="text"'
                   'rows="40" cols="120">'+cont+'</textarea><br><input '
                   'type="submit" value="submit" /></form>')
    elif command == "del":
        db.pop(name)
        return str("Deleted: "+name)
    else:
        return "Unknown command: ", command


@post('/:name/:command')
def node_submit(name, command):
    cont = request.forms.get('content')
    db[name] = cont
    return markup(cont)


if __name__ == "__main__":
    db = shelve.open("database", writeback=True)
    style = ""  # this element will be added in every view. Add your custom
                # javascript/css here
    r = re.compile(r"(http://[^ \n]+)")

    run(host='127.0.0.1', port=8000)
    print "[+] Flushing data to db..."
    db.close()
    print "[+] Done, bye"

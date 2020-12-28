"""
##########################################################################
*
*   Copyright © 2019-2020 Akashdeep Dhar <t0xic0der@fedoraproject.org>
*
*   This program is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
##########################################################################
"""

from hashlib import sha256
import json
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
import os


servchat = Flask(__name__, template_folder="../templates", static_folder="../static")
storedir = "storage"


@servchat.route("/")
def asciidoc():
    return render_template("asciidoc.html", sockport=sockp0rt, servport=servp0rt)


@servchat.route("/<themcolr>/")
def themable(themcolr):
    return render_template("themable.html", sockport=sockp0rt, servport=servp0rt, themcolr=themcolr)


@servchat.route("/storage/<path:filename>")
def getsaved(filename):
    return send_from_directory(servchat.config["CUSTOM_STATIC_PATH"], filename, conditional=True)


@servchat.route("/savedocs/")
def savedocs():
    try:
        timehash = sha256(str(time.time()).encode("UTF-8")).hexdigest()
        filename = request.args.get("filename", "0", type=str) + "_" + timehash + ".swd"
        document = request.args.get("document", "0", type=str)
        docsdict = json.loads(document)
        with open(storedir + "/" + filename, "w") as jsonfile:
            json.dump(docsdict, jsonfile)
        return jsonify(result=filename)
    except:
        return jsonify(result="savefail")


def colabnow(netpdata, servport):
    servchat.config["TEMPLATES_AUTO_RELOAD"] = True
    servchat.config["CUSTOM_STATIC_PATH"] = "../storage"
    servchat.run(host=netpdata, port=servport)


def mainfunc(servport, sockport, netprotc):
    global sockp0rt
    sockp0rt = sockport
    global servp0rt
    servp0rt = servport
    print(" * Starting Syngrafias...")
    if servport == sockport:
        print(" * [FAILMESG] The port values for Syngrafias server and WebSocket server cannot be the same!")
    else:
        print(" * Collaborator server started on port " + str(servport) + ".")
        print(" * WebSocket server started on port " + str(sockport) + ".")
        netpdata = ""
        if netprotc == "ipprotv6":
            print(" * IP version  : 6")
            netpdata = "::"
        elif netprotc == "ipprotv4":
            print(" * IP version  : 4")
            netpdata = "0.0.0.0"
        colabnow(netpdata, servport)

if __name__ == "__main__":
    mainfunc(os.getenv("PORT"), "35.231.107.163:6969", "ipprotv4")

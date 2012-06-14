from flask import Flask,url_for,render_template,request,abort,make_response,send_file,redirect
import generate_cute_qr
app = Flask(__name__) 
app.config["SERVER_NAME"] = "localhost:8080"

# in-memory database
db = { "box" : [], "project": []}
@app.route("/")
def hello():
  return render_template("index.html")


@app.route("/publish",methods=["POST"])
def publish():
  """
  """
  try:
    owner = request.form["owner-name"]
    email= request.form["owner-email"]
    twitter = request.form["owner-twitter"]
    t = request.form["item-type"]
    url = request.form["wiki-url"]
    text = request.form["freetext"]
  except:
    abort(500)
  if t == "item-type-project":
    t = "project"
  elif t == "item-type-box":
    t = "box"
  else:
    return "WTF?"
  ident = len(db[t])
  db[t].append({"owner": owner, "email": email,"ident": ident,"url":url,"text":text, "twitter" : twitter})
  return redirect("/%s/details/%d" % (t,ident))



@app.route("/<typ>/qr/<int:ident>")
def gen_qr(typ=None,ident=None):
  if ident is None: abort (500)
  if typ not in ["box","project"]: abort(404)
  data = {}
  try: data = db[typ][ident]
  except : abort(404)

  import qrcode
  import os.path
  qrpath= "qr/%s_%s"%(typ,ident)
  if not os.path.isfile(qrpath):  #skip if qrcode has already been written
    qr = qrcode.QRCode(version=5,error_correction=qrcode.constants.ERROR_CORRECT_Q,box_size=15,border=0)
    qr.add_data("%s/%s/details/%s"%(app.config["SERVER_NAME"],typ,ident))
    qr.make(fit=True)
    img = qr.make_image()
    img.save(qrpath)
    generate_cute_qr(qrpath,data)

  assert (os.path.isfile(qrpath))
  f = open(qrpath)
  #response = make_response(f.read())
  #f.close()
  #response.headers["Content-Type"] = "image/png"
  return send_file(f,mimetype="image/png")

@app.route("/<typ>/details/<int:ident>")
def details_for(typ,ident=None):
  """
  returns details for box or project
  """
  if typ not in ["box","project"]: abort(404)
  if ident is None: abort (500)

  data = {}
  try: data = db[typ][ident]
  except : print "%s %d not found" % (typ,ident)
  return render_template("%s.html" %typ,app=app,ident=ident,data=data)

@app.route("/<typ>/details/<int:ident>/json")
def json_for(typ,ident=None):
  import json
  if typ not in ["box","project"]: abort(404)
  if ident is None: abort (500)

  data = {}
  try: data = db[typ][ident]
  except : abort(404)
  return json.dumps(data)


if __name__ == "__main__":
  from os import system
  #url_for('static', filename='index.js')
  #url_for('static', filename='jquery-1.7.2.min.js')
  app.debug = True
  system("rm qr/*")
  app.run(host= "0.0.0.0",port=8080)

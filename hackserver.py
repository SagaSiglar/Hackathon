# -*- coding: iso-8859-15 -*-
from flask import Flask, request, send_from_directory
from datetime import datetime,timedelta
from dateutil import parser
from dateutil.relativedelta import *
import requests
import json
import re
app = Flask(__name__, static_url_path='')

@app.route('/img/<path:path>')
def send_img(path):
    print("serving image",path)
    return send_from_directory('img', path)

@app.route('/', methods=['GET'])
def handle_verification():
    return request.args['hub.challenge']
 
#app = Flask(__name__)
ACCESS_TOKEN = "EAAErQSJANfwBAOCZCqoiVG5BY6ZBMjWv4ByX9BX8gA3m7vnMOHK5ZCq9d0U0hK5GUEZBycfmuaxxN7c2SGWQZC3eWeKujKXMpHYTsRMg3ZCTYtiQ1A3S5jhasXxWWxOL1TUDFrdtHfMYdV7ZBqutt7x2YecbW7uopx9FZCzx7AxN4AZDZD"
company_categories = {
"Get AS":"cable","Steen & Strøm ASA":"fashion","UPS":"transportation",
"DHL AS":"transportation","Norwegian Air Shuttle ASA":"travel","Tollpost Globe AS":"transportation",
"DnB NOR Insurance":"insurance","Fred Olsen Energy ASA":"offshore","Netcom ASA":"mobile",
"Elixia Colosseum":"fitness","TV 2 Gruppen AS":"tv",
"Schibsted ASA":"media","Telenor Norge ASA":"mobile","Metronet AS":"tv",
"Sats Bislett":"fitness","Canal Digital":"cable","NRK":"tv",
"Volvo Personbiler Norge AS":"cars","Hafslund ASA":"power","PostNord AS":"transportation",
"Haralds Gym":"fitness","Telia Norge AS":"mobile","Elkjøp Norge AS":"electronics","Broadnet AS":"cable",
"Sats Bislett":"fitness"
}
confirm_yes = ['yes','yup','ok', 'confirm','i confirm','sure','do it','go ahead','y']
confirm_no = ['no','nope','never', 'cancel']
regex = re.compile('[^a-zA-Z]')
img_server="https://a8d668fd.ngrok.io/img/"

user_context={}


def initialize_user_context(user_id):
 user_context[user_id] = { 
 "customerId": "19089446109",
 "accountnumber":"12083015417",
 "accounts": {},
 "account_details": {}, # accountnumber -> name
 "account_names": {}, # account name -> accountnumber
 "counterparties": {},
 "fullnames": {},
 "context": None,
 "current_payment": {},
 "username": None
 }

def get_chunks(a, k):
  r = []
  p = len(a)//k
 
  for i in range(0,p+1):
    r.append(a[i*k:i*k+k])
    #print(i, a[i*k:i*k+k])
 
  return r

def sort_listdict(the_list): 
    tlist={}
    kl= []
    result = []
    
    for l in the_list:
      dt = l['date']
      ndt = dt[6:10]+dt[3:5]+dt[0:2]
      tid = l['transactionID']
      k = ndt+' '+str(tid)
      tlist[k] = l
      kl.append(k)
    
    kl.sort()
    for m in reversed(kl):
       #print(tlist[m])
       result.append(tlist[m])
    
    return result

def letters_only(t):
  global regex
  if t:
    return regex.sub('',t).lower()
  else:
    return None
 
def reply(user_id, msg):
    print("Sending")
 
    c = get_chunks(msg, 640)
    for line in c:
      data = {
        "recipient": {"id": user_id},
        "message": {"text": line}
      }
      resp = requests.post("https://graph.facebook.com/v2.10/me/messages?access_token=" + ACCESS_TOKEN, json=data)
      #print(resp.content)

def quickreply_confirm(user_id, msg):
    print("Quick reply")
 
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg,
        "quick_replies":[
          {
            "content_type":"text",
            "title":"Confirm",
            "payload":"Confirm"
          },
          {
            "content_type":"text",
            "title":"Cancel",
            "payload":"Cancel"
          }
    	]}
    }
    resp = requests.post("https://graph.facebook.com/v2.10/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)

def show_bills(user_id):
    data = {
        "recipient": {"id": user_id},
        "message": {
            "attachment":{"type":"template",
              "payload":{"template_type":"generic",
              "elements":[{
                    "title":"Hafslund",
                    "image_url":'https://a8d668fd.ngrok.io/img/hafslund-nett-logo.png',
                    "subtitle":"Electricity August 2018, kr 1.208,50"
					,
                    "buttons":[
                      {
                       "type":"postback",
                       "title":"Pay this bill",
                       "payload":"Pay"
                      }             
                    ]     
                  },
				  {
                    "title":"Sats Elexia",
                    "image_url":'https://a8d668fd.ngrok.io/img/jpg.jpg',
                    "subtitle":"Monthly subscription August 2018, kr 950,00"
					,
                    "buttons":[
                      {
                       "type":"postback",
                       "title":"Pay this bill",
                       "payload":"Pay"
                      }             
                    ]     
                  }                  
                ]
              }
            }
        }
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)
    return None

def show_bills2(user_id):
    data = {
        "recipient": {"id": user_id},
        "message": {
            "attachment":{"type":"template",
              "payload":{"template_type":"list",
              "top_element_style": "compact",
              "elements":[{
                    "title":"Hafslund, kr 1.208,50",
                    #"image_url":'https://a8d668fd.ngrok.io/img/hafslund-nett-logo.png',
                    "subtitle":"Electricity August 2017, Due date: 10.09.2017"
					,
                    "buttons":[
                      {
                       "type":"postback",
                       "title":"Pay this bill",
                       "payload":"Pay"
                      }             
                    ]     
                  },
				  {
                    "title":"Sats Elixia, kr 950,00",
                    #"image_url":'https://a8d668fd.ngrok.io/img/satselixia.PNG',
                    "subtitle":"Monthly subscription August 2017, Due date: 25.09.2017"
					,
                    "buttons":[
                      {
                       "type":"postback",
                       "title":"Pay this bill",
                       "payload":"Pay"
                      }             
                    ]     
                  }      ,
                  {
                    "title":"DNB Skadeforsikring, kr 5350,00",
                    #"image_url":'https://a8d668fd.ngrok.io/img/satselixia.PNG',
                    "subtitle":"Quarterly installment Oct-Dec 2017, Due date: 10.10.2017"
					,
                    "buttons":[
                      {
                       "type":"postback",
                       "title":"Pay this bill",
                       "payload":"Pay"
                      }                                  
                    ]     
                  }            
                ]
              }
            }
        }
    }
    resp = requests.post("https://graph.facebook.com/v2.10/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)
    return None


def handle_nlp_message(user_id, message):
  nlp = message["nlp"]
  print("User"+user_id+ ", received nlp "+str(nlp))
  fromdate=None
  todate=None
  if 'datetime' in nlp['entities']:
    dts = nlp['entities']['datetime']
    for dt in dts:
      dttype = dt['type']
    
      if (dttype == 'value'):
          dtgrain = dt['grain']
          fromdt=parser.parse(dt['value'])
          if (fromdt > datetime.now(fromdt.tzinfo)):
             fromdt = fromdt-relativedelta(years=+1)
          if (dtgrain == 'month'):
             todt=fromdt+relativedelta(months=+1)
             todt = todt-relativedelta(days=1)
          elif (dtgrain == 'year'):
             todt=fromdt+relativedelta(years=+1)
          else:
             todt=fromdt
          fromdate=fromdt.strftime('%d%m%Y')
          todate=todt.strftime('%d%m%Y')
      elif (dttype == 'interval'):
          fromdate='01012015'
          todate='01012018'
          if 'from' in dt:
             fromdt=parser.parse(dt['from']['value'])
             if (fromdt > datetime.now(fromdt.tzinfo)):
               fromdt = fromdt-relativedelta(years=+1)
             fromdate=fromdt.strftime('%d%m%Y')
          if 'to' in dt:
            todt=parser.parse(dt['to']['value'])
            if (todt > datetime.now(todt.tzinfo)):
               todt = todt-relativedelta(years=+1)
            todt = todt-relativedelta(days=1)
            todate=todt.strftime('%d%m%Y')
      else:
         print('Unknown datetime type '+dttype)
    if fromdate and todate:
      print('fromdate='+fromdate+' todate='+todate)
   
  if 'intent' in nlp['entities']:
     intent = nlp['entities']['intent'][0]['value']
     if  intent == 'payment_query':
       if (len(user_context[user_id]["accounts"]) < 1):
          get_accounts(user_id)
     
       counterparty_filter = None
       if 'payment_recipient' in nlp['entities']:
          counterparty_filter = nlp['entities']['payment_recipient'][0]['value']
       
       category_filter = None
       if 'payment_category' in nlp['entities']:
          category_filter = nlp['entities']['payment_category'][0]['value']
      
       #accno = next(iter(accounts)) # get first one
       #global accountnumber
       #accountnumber = accno # set default accountnumber
       if user_context[user_id]["accountnumber"]:
          #return handle_intent_payment_query(accounts[accno]['accountNumber'], fromdate, todate, counterparty_filter, category_filter)
          return handle_intent_payment_query(user_id,fromdate, todate, counterparty_filter, category_filter)
     elif intent == "payment_received":
       if (len(user_context[user_id]["accounts"]) < 1):
          get_accounts(user_id)
     
       counterparty_filter = None
       if 'payment_recipient' in nlp['entities']:
          counterparty_filter = nlp['entities']['payment_recipient'][0]['value']
       if user_context[user_id]["accountnumber"]:
          return handle_intent_payment_received(user_id,fromdate, todate, counterparty_filter)               
     elif intent == 'account_balance':
       #get_accounts()
       return handle_intent_get_account(user_id)
     elif intent == 'payment_transaction':
       return handle_intent_payment(user_id,nlp)
     elif intent == 'show_bills':
       return show_bills2(user_id)
     elif intent == 'get_statement':
       counterparty_filter = None
       if 'payment_recipient' in nlp['entities']:
          counterparty_filter = nlp['entities']['payment_recipient'][0]['value']
       return handle_intent_get_statement(user_id, fromdate, todate, counterparty_filter)
     else:
       return 'I don\'t know what you mean...'
  elif 'greetings' in nlp["entities"]:
    return "Hi there, "+user_context[user_id]["username"]+"!"
  elif user_context[user_id]["context"] == "WAIT_FOR_AMOUNT" and "number" in nlp["entities"]:
    current_payment = user_context[user_id]["current_payment"]
    amount = nlp["entities"]["number"][0]["value"]
    current_payment["amount"] = amount
    user_context[user_id]["context"]='WAIT_FOR_PAYMENT_CONFIRMATION'
    recipient = current_payment["recipientName"]
    accno = current_payment['creditAccountNumber']
    #return 'Please confirm that I transfer '+str(amount)+' to '+recipient+' ('+str(accno)+')'
    quickreply_confirm(user_id, 'Please confirm that I transfer '+str(amount)+' to '+recipient+' ('+str(accno)+')')
    return None
  elif "thanks" in nlp["entities"]:
    return "Glad to be of help, "+user_context[user_id]["username"]+"!"
  else:
    return "I'm not sure what you mean."
    
    
def handle_intent_payment(user_id,nlp):
  counterparties = user_context[user_id]["counterparties"]
  fullnames = user_context[user_id]["fullnames"]
  context = user_context[user_id]["context"]
  current_payment = user_context[user_id]["current_payment"]
  
  if (len(user_context[user_id]["accounts"]) < 1):
     get_accounts(user_id)
  
  accountnumber = user_context[user_id]["accountnumber"]
  
  if len(counterparties) < 1 and accountnumber:
    t = get_account_transactions(user_id,'01012015','01012018')
    for trans in t:
        accname = trans['transactionAccountName']
        user_context[user_id]["fullnames"][accname.lower()] = accname
        counterparties[accname.lower()] = trans['transactionAccountNumber']
        xl = accname.split(' ')
        for n in xl:
          counterparties[n.lower()] = trans['transactionAccountNumber']
          fullnames[n.lower()] = accname
        
  
  recipient = None
  amount = None
  #get payment recipient
  if 'payment_recipient' in nlp['entities']:
    recipient = nlp['entities']['payment_recipient'][0]['value']
  #get amount
  if 'number' in nlp['entities']:
    amount = nlp['entities']['number'][0]['value']
  if 'datetime' in nlp['entities']:
    dt = nlp['entities']['datetime'][0]['value']
    amount=dt[0:4]
  #get all transactions to build counterparty database
  #search recipient in database
  #send confirmation message
  resptxt = ''
  if not recipient:
     return 'To whom ?'
  elif not amount:
     if recipient.lower() in counterparties.keys():
        accno = counterparties[recipient.lower()] 
        current_payment=user_context[user_id]["current_payment"]
        current_payment['debitAccountNumber'] = accountnumber
        current_payment['creditAccountNumber'] = accno
        current_payment['message'] = 'Test transfer'
        current_payment['paymentDate'] = '2017-09-07'
        current_payment["recipientName"] = fullnames[recipient.lower()]
        user_context[user_id]["context"] = "WAIT_FOR_AMOUNT"
        return 'What amount?'
     else:
        return 'Sorry, I could not find the account number for '+recipient
  else:
     if recipient.lower() in counterparties.keys():
        accno = counterparties[recipient.lower()] 
        current_payment=user_context[user_id]["current_payment"]
        current_payment['debitAccountNumber'] = accountnumber
        current_payment['creditAccountNumber'] = accno
        current_payment['amount'] = amount
        current_payment['message'] = 'Test transfer'
        current_payment['paymentDate'] = '2017-09-07'
        current_payment["recipientName"] = fullnames[recipient.lower()]
        user_context[user_id]["context"]='WAIT_FOR_PAYMENT_CONFIRMATION'
        #return 'Please confirm that I transfer '+str(amount)+' to '+fullnames[recipient.lower()]+' ('+str(accno)+')'
        quickreply_confirm(user_id, 'Please confirm that I transfer '+str(amount)+' to '+fullnames[recipient.lower()]+' ('+str(accno)+')')
        return None
     else:
        return 'Sorry, I could not find the account number for '+recipient

def handle_intent_get_accounts(user_id):
    resptext = ''
    accounts = user_context[user_id]
    print(accounts)
    for accno in accounts.keys():       
          resptext += account_details[accno]['accountName']+': '+str(accounts[accno]['availableBalance'])+'\n'
    return resptext

def handle_intent_get_account(user_id):
    resptext = ''
    accountnumber = user_context[user_id]["accountnumber"]
    customerId = user_context[user_id]["customerId"]
    if accountnumber:
       j = get_account_details(accountnumber, customerId)
       if j:
          #resptext = "Your balance is "+str(j['availableBalance'])+" ("+j["accountName"]+")\n"
          resptext = "Your balance is "+str(j['availableBalance'])+".\n"
       else:
          resptext = "I cannot find any information for that account"
    else:
       resptext = "Hmm, I don't have an account number to look up"
    return resptext


def get_accounts(user_id):
  accounts = user_context[user_id]["accounts"]
  account_details = user_context[user_id]["account_details"]
  customerId = user_context[user_id]["customerId"]
  url ="https://dnbapistore.com/hackathon/accounts/1.0/account/customer/"+customerId
  r = requests.get(url, headers = headers)
  if r.ok:
    #print(r.text)
    j = json.loads(r.text)
    if 'accounts' in j:
       for acc in j['accounts']:
          accounts[acc['accountNumber']] = acc
          details = get_account_details(acc['accountNumber'],customerId)
          if details:
            account_details[acc['accountNumber']] = details
    return True
  else:
    print("Problems getting account data for "+user_context[user_id]["customerId"]+ " "+r.text)
    return False

def get_account_transactions(user_id, fromdate, todate, trans_type = 0):
  transactions = []
  if not (fromdate and todate):
    return None
  print("--> get_account_transactions:"+fromdate+" "+todate)
  customerId = user_context[user_id]["customerId"]
  accountnumber = user_context[user_id]["accountnumber"]
  url = 'https://dnbapistore.com/hackathon/accounts/1.0/account?accountNumber='+str(accountnumber)+'&customerID='+ customerId+'&dateFrom='+fromdate+'&dateTo='+todate
  r = requests.get(url, headers = headers)
  if r.ok:
    j = json.loads(r.text)
    if 'transactions' in j:
      for trans in j['transactions']:
        #print(trans)
        if trans_type == 0:   
           transactions.append(trans)
        elif trans_type < 0 and float(trans["amount"]) < 0.0:
           transactions.append(trans)
        elif trans_type > 0 and float(trans["amount"]) > 0.0:
           transactions.append(trans)
                      
    return sort_listdict(transactions)
  else:
    return None

def is_similar_to(a, b):
  return b.lower().find(a.lower())>-1
  
def format_date_expression(fromdate,todate):
  if fromdate == todate:
    return "for "+fromdate[0:2]+"/"+fromdate[2:4]+"/"+fromdate[4:8]
  else:
    return "for the period "+fromdate[0:2]+"/"+fromdate[2:4]+"/"+fromdate[4:8]+" to "+todate[0:2]+"/"+todate[2:4]+"/"+todate[4:8]
 
def handle_intent_payment_query(user_id, fromdate, todate, counterparty_filter=None, category_filter = None):
  #print("category_filter="+category_filter)
  if not fromdate:
     fromdate='01062017'
  if not todate:
     todate = '01012018'
  
  accountnumber = user_context[user_id]["accountnumber"]
  
  t = get_account_transactions(user_id, fromdate, todate,-1)
  if t:
    resptext=''
    total = 0.0
    for trans in t:
        #print ("handling "+trans['transactionAccountName'])
        if counterparty_filter:
          if is_similar_to(counterparty_filter,trans['transactionAccountName']):
            resptext += trans['date']+' '+trans['transactionAccountName']+' '+str(trans['amount'])+'\n'
            total = total + float(trans['amount'])
        elif category_filter:
          #print("here "+category_filter+" '"+trans['transactionAccountName']+"'")
          if trans['transactionAccountName'] in company_categories and category_filter == company_categories[trans['transactionAccountName']]:
             resptext += trans['date']+' '+trans['transactionAccountName']+' '+str(trans['amount'])+'\n'
             total = total + float(trans['amount'])
        else:
          resptext += trans['date']+' '+trans['transactionAccountName']+' '+str(trans['amount'])+'\n'
          total = total + float(trans['amount'])
                
    if (len(resptext) < 1):
        resptext='I could not find any payments '+format_date_expression(fromdate,todate)
    elif category_filter and abs(total) > 0.0:
        resptext = 'You have spent a total of '+str(abs(total))+' '+format_date_expression(fromdate,todate)+'.\n'+resptext
    else:
        resptext = "Here is what I found "+format_date_expression(fromdate,todate)+".\nThe total amount is "+str(abs(total))+"\n"+resptext
    return resptext
  
  else:
    return "Could not find any outgoing transactions "+ format_date_expression(fromdate,todate) #for "+user_context[user_id]["customerId"]

def handle_intent_payment_received(user_id, fromdate, todate, counterparty_filter=None):
  #print("category_filter="+category_filter)
  if not fromdate:
     fromdate='01062017'
  if not todate:
     todate = '01012018'
  
  accountnumber = user_context[user_id]["accountnumber"]
  
  t = get_account_transactions(user_id, fromdate, todate, 1)
  if t:
    resptext=''
    total = 0.0
    for trans in t:
        #print ("handling "+trans['transactionAccountName'])
        if counterparty_filter:
          if is_similar_to(counterparty_filter,trans['transactionAccountName']):
            resptext += trans['date']+' '+trans['transactionAccountName']+' '+str(trans['amount'])+' ('+trans["message/KID"]+')\n'
            total = total + float(trans['amount'])
        else:
          resptext += trans['date']+' '+trans['transactionAccountName']+' '+str(trans['amount'])+' ('+trans["message/KID"]+')\n'
          total = total + float(trans['amount'])
       
    if (len(resptext) < 1):
        resptext='I could not find anything '+format_date_expression(fromdate,todate)
    else:
        resptext = "Here is what I found "+format_date_expression(fromdate,todate)+".\nThe total amount is "+str(abs(total))+"\n"+resptext
    return resptext
  else:
    return "I could not find any credit transactions for "+user_context[user_id]["customerId"]

def handle_intent_get_statement(user_id, fromdate=None, todate=None, counterparty_filter=None):
  if not fromdate:
     fromdate='01062017'
  if not todate:
     todate = '01012018'
  print("--> handle_intent_get_statement:"+fromdate+" "+todate)
  accountnumber = user_context[user_id]["accountnumber"]
  
  t = get_account_transactions(user_id, fromdate, todate)
  if t:
    resptext=''
    for trans in t:
        if counterparty_filter:
          if is_similar_to(counterparty_filter,trans['transactionAccountName']):
            resptext += trans['date']+' '+trans['transactionAccountName']+' '+str(trans['amount'])+' ('+trans["message/KID"]+')\n'
        else:
          resptext += trans['date']+' '+trans['transactionAccountName']+' '+str(trans['amount'])+'\n'
    
       
    if (len(resptext) < 1):
        resptext='I could not find anything '+format_date_expression(fromdate,todate)
    else:
        resptext = "Here is what I found "+format_date_expression(fromdate,todate)+".\n"+resptext
    return resptext
  else:
    return "I could not find any transactions for "+user_context[user_id]["customerId"]



def get_account_details(accountnumber,customerId):
    url = 'https://dnbapistore.com/hackathon/accounts/1.0/account/details?accountNumber='+str(accountnumber)+'&customerID='+customerId
    print('-->'+url)
    r = requests.get(url, headers = headers)
    print(r.text)
    if r.ok:
        j = json.loads(r.text)
        return j
    else:
        return None
 
def send_payment(payload):
  #payload = {
  #"debitAccountNumber": fromAccount,
  #"creditAccountNumber": toAccount,
  #"message": message,
  #"amount": amount,
  #"paymentDate": "2017-08-31"
  #}
 
  print("Payload="+str(payload))
 
  url='https://dnbapistore.com/hackathon/payments/1.0/payment' 
  r = requests.put(url,headers=headers, json=payload)
  if r.ok:
    j = json.loads(r.text)
    print(r.text)
    return j['paymentIDNumber']
  else:
    print(r.text)
    return None
    
def get_user_profile(psid):
    print("psid="+psid)
    resp = requests.get("https://graph.facebook.com/v2.6/"+psid+"?fields=first_name,last_name&access_token=" + ACCESS_TOKEN)
    if resp.ok and resp.text:
      j = json.loads(resp.text)
      user_context[psid]["username"] = j["first_name"]
    else:
      print(resp.text)
     
@app.route('/', methods=['POST'])
def handle_incoming_messages():
   
    global user_context
    
    data = request.json
    #print("---->Incoming", data)
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):                    
                    the_message = messaging_event["message"]                 
                    if (not the_message.get("is_echo")) and 'text' in the_message:
                      print("Incoming", data)
                      message = the_message["text"]     
                      sender = messaging_event["sender"]["id"]
                      
                      if not sender in user_context:
                         initialize_user_context(sender)
                      user_id=sender
                      context = user_context[user_id]["context"]
                      current_payment = user_context[user_id]["current_payment"]
                      username = user_context[user_id]["username"]
                      
                      if not username:
                        get_user_profile(sender)
                        #reply(sender, "Hi, "+user_context[user_id]["username"]+"!")
                      
                      if context:                    
                         if context == 'WAIT_FOR_PAYMENT_CONFIRMATION':
                            message = the_message["text"]     
                            if letters_only(message) in confirm_yes:
                               payid= send_payment(current_payment)
                               if payid:
                                  reply(sender, "OK, payment confirmed (payment number "+str(payid)+")")
                               else:
                                  reply(sender, "Hmmm, seems I cannot transfer the money.")
                               context = None
                               return "ok"
                            elif letters_only(message) in confirm_no:
                               reply(sender, "OK, payment cancelled")
                               context = None
                               return "ok"                          
                               
                               #reply(sender, "Payment cancelled.")
                            context = None
                      
                      if message[0] == '@':
                        user_context[user_id]["accounts"] = {}
                        (user_context[user_id]["customerId"],user_context[user_id]["accountnumber"]) = message[1:].split('/')
                        reply(sender, "Current customerID="+user_context[user_id]["customerId"]+", current accountnumber="+user_context[user_id]["accountnumber"])
                      elif 'nlp' in the_message and len(the_message['nlp']['entities']) > 0:
                        response = handle_nlp_message(sender,the_message)
                        if response:
                           reply(sender, response)                                                        
                      else:
                        reply(sender, "Sorry, I'm not sure what you mean." )
                      #quick_reply(sender, "choose one:")                                                     
                      
    
    return "ok"
if __name__ == '__main__':
 
    headers = {'Authorization':'Bearer 881d5fef-ecde-3ab2-8e01-223c5560ec6f'}
    app.run(debug=True)
 
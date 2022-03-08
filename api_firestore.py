import csv 
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from utils import CURRENT_COLLECTION, HOLDER_COLLECTION, now
import random
from datetime import timedelta

db = firestore.Client()

def generate_tx(user_id):
    rand_nums = random.randint(100,999)
    last_num = random.randint(1,9)
    amount = float(f"4.{rand_nums}{last_num}")
    print(f"generated amount {amount}")
    if (not add_tx(user_id, amount)):
        return (0)
    return (amount)

def add_tx(user_id, tx_amount):
    time = now()
    time = time + timedelta(hours=1)
    user_id = str(user_id)
    tx_amount = float(tx_amount)
    try:
        db = firestore.Client()
        doc_ref = db.collection(CURRENT_COLLECTION).document(user_id)
        doc_ref.set({
            "user_id" : user_id,
            "tx_amount": tx_amount,
            "time": str(time)
        })
    except:
        return (0)
    return (1)

def add_holder(user_id, addr):
    user_id = str(user_id)
    try:
        db = firestore.Client()
        doc_ref = db.collection(HOLDER_COLLECTION).document(user_id)
        doc_ref.set({
            "user_id" : user_id,
            "addr": addr
        })
    except:
        return (0)
    return (1)

def get_all_holders():
    docs = db.collection(HOLDER_COLLECTION).stream()
    return (docs)

def get_all_tx():
    docs = db.collection(CURRENT_COLLECTION).stream()
    return (docs)

def get_tx(user_id):
    user_id = str(user_id)
    doc_ref = db.collection(CURRENT_COLLECTION).document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return(doc.to_dict())
    else:
        return (0)

def delete_tx(user_id):
    db.collection(CURRENT_COLLECTION).document(str(user_id)).delete()
    return (1)


def delete_holder(user_id):
    db.collection(HOLDER_COLLECTION).document(str(user_id)).delete()
    return (1)


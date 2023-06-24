from __future__ import annotations
from enum import Enum
from math import sqrt
from typing import Iterable
import store.models as models
import re
import django.contrib.auth.hashers as hashers
from django.db.models.manager import BaseManager
from django.db.models import Q

class Status(Enum):
    FAILURE = 0
    SUCCESS = 1


def rangeStatus(val, min, max, name, regex=r"[\s\S]*", regexFailMessage=""): # [min, max]
    if len(val) < min:
        return (Status.FAILURE, name + " must be more than " + (min-1) + " characters")
    if len(val) > max:
        return (Status.FAILURE, name + " must be less than " + (max+1) + " characters")
    if re.fullmatch(regex, val) == None:
        if regexFailMessage == "":
            return (Status.FAILURE, "invalid character(s)")
        else:
            return (Status.FAILURE, name + " " + regexFailMessage)
    return (Status.SUCCESS, "")


# check fields and add new customer to database if passes
def signUp(username: str, name: str, email: str, phoneNumber: str, password: str) -> tuple[Status, any]:
    username = username.strip()
    statusMessage = rangeStatus(username, 2, 32, "username", r"\w*", "must contain only Latin alphanumeric characters or underscore") # a-zA-Z0-9_
    if (statusMessage[0] == Status.FAILURE):
        return statusMessage

    if username == password:
        return (Status.FAILURE, "username and password can't be the same")

    name = name.strip()
    statusMessage = rangeStatus(name, 1, 64, "name", r"[a-zA-Z ]*", "must contain only Latin characters or space") # a-zA-Z or space
    if (statusMessage[0] == Status.FAILURE):
        return statusMessage

    email = email.strip()
    statusMessage = rangeStatus(email, -1, 254, "email", r"\S+@\S+\.\S+", "is not valid") # x@x.x
    if (statusMessage[0] == Status.FAILURE):
        return statusMessage
    if (models.Customer.objects.filter(email=email).count() >= 1):
        return (Status.FAILURE, "email is already in use")

    phoneNumber = phoneNumber.strip()
    statusMessage = rangeStatus(phoneNumber, -1, 254, "phone number", r"(\+?\d{1,3}[-.\s]?)?(\d{3}|\(\d{3}\))[-.\s]?\d{3}[-.\s]?\d{4}", "is in an invalid format")
    if (statusMessage[0] == Status.FAILURE):
        return statusMessage
    for char in "()+-. \t\n\r\v\f": # "+1(444)-666 - 7777" => 14446667777
        phoneNumber.replace(char, "")
    if (models.Customer.objects.filter(phoneNumber=phoneNumber).count() >= 1):
        return (Status.FAILURE, "phone number is already in use")

    # vulnerable on HTTP
    ### no strip ###
    statusMessage = rangeStatus(password, 8, 16, "password",
        r"[\w#$%&'()*+,-./:;<=>?@^_{|}~]*", "must contain only Latin alphanumeric characters or punctuation") # a-zA-Z0-9_...
    if (statusMessage[0] == Status.FAILURE):
        return statusMessage
    password = hashers.make_password(password)

    customer = models.Customer.objects.create(username=username, name=name, email=email, phoneNumber=phoneNumber, password=password)

    return (Status.SUCCESS, customer)


def getCustomerByUserName(username: str) -> models.Customer | None:
    return models.Customer.objects.filter(username=username).first()


# check if user's password is correct
def loginVerify(wildInput: str, password: str) -> tuple[Status, any]:
    if wildInput.count("@") == 1: # email
        user = models.Customer.objects.filter(email=wildInput).first()
        if user == None:
            return (Status.FAILURE, "email not found")
    else: # username
        user = getCustomerByUserName(wildInput)
        if user == None:
            return (Status.FAILURE, "username not found")
    # phone number possible to be indistinguishable from username

    if not hashers.check_password(password, user.password):
        return (Status.FAILURE, "incorrect password or username")

    return (Status.SUCCESS, user)


# verify and add an address to the database
def createAddress(address: str, city: str, state: str, zipcode: str) -> tuple[Status, any]:
    address = address.strip()
    statusMessage = rangeStatus(address, 1, 50, "address", r"[\w\s]*", "must contain only letters or numbers or space") # a-zA-Z0-9
    if (statusMessage[0] == Status.FAILURE):
        return statusMessage

    city = city.strip()
    statusMessage = rangeStatus(city, 1, 50, "city", r"[\w\s]*", "must contain only letters or numbers or space") # a-zA-Z0-9
    if (statusMessage[0] == Status.FAILURE):
        return statusMessage

    state = state.strip()
    statusMessage = rangeStatus(state, 1, 50, "state", r"[\w\s]*", "must contain only letters or numbers or space") # a-zA-Z0-9
    if (statusMessage[0] == Status.FAILURE):
        return statusMessage

    zipcode = zipcode.strip()
    statusMessage = rangeStatus(state, 1, 50, "zipcode", r"[\w\s]*", "must contain only letters or numbers or space") # a-zA-Z0-9
    if (statusMessage[0] == Status.FAILURE):
        return statusMessage

    address = models.ShippingAddress.objects.create(address=address, city=city, state=state, zipcode=zipcode)

    return (Status.SUCCESS, address)


# create a new perfume item type available for items to identify as
def addItemType(name: str, categoryName, brandName: str,
    priceCents, salePrice, sizeOz, gender, description, image,
    qualities: list[tuple[str, float]]) -> tuple[Status, str]:

    brand = models.Brand.objects.filter(name__iexact=brandName).first()
    if (brand == None):
        brand = models.Brand.objects.create(name=brandName)
    category = models.ItemType.objects.filter(name__iexact=categoryName).first()
    if (category == None):
        category = models.ItemCategory.objects.create(name=categoryName)

    itemType = models.ItemType.objects.create(
        name=name, category=category, brand=brand,
        priceCents=priceCents, salePrice=salePrice, sizeOz=sizeOz,
        gender=gender, description=description, image=image
    )

    # IF FAILURE, DELETE THE NEW ITEMCATEGORY?
    addQualitiesItemType(qualities, itemType)

    return (Status.SUCCESS, itemType)


def addQualitiesItemType(qualities: list[tuple[str, float]], itemType: models.ItemType):
    for qualityPair in qualities:
        qualityType = models.QualityType.objects.filter(name__iexact=qualityPair[0]).first()
        if (qualityType == None):
            qualityType = models.QualityType.objects.create(name=qualityPair[0])
        quality = models.Quality.objects.create(type=qualityType, value=qualityPair[1])
        models.QualityItemTypeJoin.objects.create(
            quality=quality,
            itemType=itemType
        )


def addQualitiesCustomer(qualities: list[tuple[str, float]], customer: models.Customer):
    for qualityPair in qualities:
        qualityType = models.QualityType.objects.filter(name__iexact=qualityPair[0]).first()
        if (qualityType == None):
            qualityType = models.QualityType.objects.create(name=qualityPair[0])
        quality = models.Quality.objects.create(type=qualityType, value=qualityPair[1])
        models.QualityCustomerJoin.objects.create(
            quality=quality,
            customer=customer
        )


# quality type length: Q, q1 length: A, q2 length: B; A<Q, B<Q.
# Algorithm choices: O(A * B) or O(Q + intoDict(A) + intoDict(B)) (or O(Q) if we autosort Quality)
# return score between [-1.0, 1.0]
def correlateQualitiesDict(qualities1: dict[models.QualityType, float], qualities2: dict[models.QualityType, float],
        discardNoRelatedQualities,
        averageError=0, # to compensate for unspecified qualities
        ) -> float | None:
    amountQualityTypes = models.QualityType.objects.count()
    amountMatched = 0
    totalScore = 0
    dict(qualities1)
    # for q1Type, q1Val in qualities1:
    #     for q2Type, q2Val in qualities2:
    for qualityType in models.QualityType.objects.all():
        q1Val = qualities1.get(qualityType)
        q2Val = qualities2.get(qualityType)
        if q1Val != None and q2Val != None:
            amountMatched += 1
            difference = abs(q1Val - q2Val)
            totalScore += 1 - difference # https://www.desmos.com/calculator/w57bhkvkv1

    if discardNoRelatedQualities and amountMatched == 0:
        return None

    amountMissed = amountQualityTypes - amountMatched
    totalScore += (amountMissed * averageError)
    totalScore /= amountQualityTypes
    return totalScore


def dbQualitiesToDict(objs):
    return dict(list(map(lambda q: (q.quality.type, q.quality.value), objs)))

def correlateQualitiesItemType(qualities1: dict[models.QualityType, float], itemType: models.ItemType, discardNoRelatedQualities) -> float | None:
    return correlateQualitiesDict(
        qualities1,
        dbQualitiesToDict(models.QualityItemTypeJoin.objects.filter(itemType=itemType).all()),
        discardNoRelatedQualities
    )

def getCorrelations(primaryQualities: dict[models.QualityType, float], discardNoRelatedQualities):
    scores = dict(list(map(lambda it: (it, correlateQualitiesItemType(primaryQualities, it, discardNoRelatedQualities)), models.ItemType.objects.all())))
    if discardNoRelatedQualities:
        scores = {k:v for (k,v) in scores.items() if v != None}
    return sorted(scores, key=lambda s: scores[s], reverse=True)

# main method for finding the best perfumes for a customer
# discardNoRelatedQualities - if no perfums have defined any qualities that the customer defines, then leave them empty
def getCorrelations(customer: models.Customer, discardNoRelatedQualities=True):
    return getCorrelations(dbQualitiesToDict(models.QualityCustomerJoin.objects.filter(customer=customer).all()), discardNoRelatedQualities)

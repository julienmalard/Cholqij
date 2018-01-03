from pkg_resources import resource_filename
import json

a = resource_filename('cholqij', "ch'ab'äl.json")

with open(a, encoding='UTF8') as d:
    ruqaxik_tzij = json.load(d)


def taqaxaj_tzij(cholqij, wachinaq, chabäl):

    try:
        rqxk = ruqaxik_tzij[cholqij][wachinaq]
    except KeyError:
        raise ValueError('')

    nabey_chabäl = ruqaxik_tzij[cholqij]["Ch'ab'äl"]
    try:
        return rqxk[chabäl]
    except KeyError:
        return rqxk[nabey_chabäl]


def taqaxaj_ajilanïk(ajlnk, ruwäch):
    return ajlnk

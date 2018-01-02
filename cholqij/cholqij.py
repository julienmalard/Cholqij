from datetime import date as qj
from datetime import timedelta


class Cholqij(object):

    nubi = NotImplemented

    def __init__(ri, qij, **kwargs):

        if all(x != None for x in kwargs.values()):
            ajlnk = ri.taban_rikïn_qij(qij, **kwargs)
            ri.qij_python = qj.fromordinal(ajlnk)
        else:
            if isinstance(qij, qj):
                ajlnk = qij.toordinal()
                qij_python = qij
            elif isinstance(qij, int):
                ajlnk = qij
                qij_python = qj.fromordinal(ajlnk)
            elif isinstance(qij, Cholqij):
                ajlnk = qij.qij_python.toordinal()
                qij_python = qj.fromordinal(ajlnk)
            else:
                raise ValueError('')
            
            ri.taban_rikïn_ajilanïk(ajlnk)
            ri.qij_python = qj(year=qij_python.year, month=qij_python.month, day=qij_python.day)

    def taban_rikïn_ajilanïk(ri, ajlnk):
        raise NotImplementedError

    def taban_rikïn_qij(ri, qij, **kwargs):
        raise NotImplementedError

    def tatzibaj(ri, rubanom, chabäl):
        raise NotImplementedError

    def tajala(ri, cholqij):
        for sbc in Cholqij.__subclasses__():
            if cholqij.lower == sbc.nubi.lower():
                return sbc(ri)

    def __add__(ri, chïk):

        if isinstance(chïk, int):
            chïk = timedelta(days=chïk)

        qij_python = ri.qij_python + chïk

        return ri.__class__(qij_python)

    __radd__ = __add__

    def __sub__(ri, chïk):

        if isinstance(chïk, int):
            chïk = timedelta(days=chïk)

        kaka_qij = ri.qij_python - chïk

        if isinstance(kaka_qij, timedelta):
            return kaka_qij
        else:
            return ri.__class__(kaka_qij)


class Gregoriano(Cholqij):

    nubi = 'Gregoriano'

    def __init__(ri, qij, ik=None, junab=None):

        ri.ik = None
        ri.qij = None
        ri.junab = None
        ri.rubi_qij = None

        super().__init__(qij=qij, ik=ik, junab=junab)

    def taban_rikïn_ajilanïk(ri, ajlnk):
        qij_python = qj.fromordinal(ajlnk)

        ri.qij = qij_python.day
        ri.ik = qij_python.month
        ri.junab = qij_python.year
        ri.rubi_qij = qij_python.isoweekday()

    def taban_rikïn_qij(ri, qij, **kwargs):

        ik = kwargs['ik']
        junab = kwargs['junab']

        if ik is None and junab is not None:
            raise ValueError('')
        elif ik is not None and junab is None:
            raise ValueError('')

        ri.qij = qij  # type: int
        ri.ik = ik  # type: int
        ri.junab = junab  # type: int

        qij_python = qj(year=ri.junab, month=ri.ik, day=ri.qij)
        ri.rubi_qij = qij_python.isoweekday()

        return qij_python.toordinal()

    def tatzibaj(ri, rubanom, chabäl):
        pass


class Maya(Cholqij):

    nubi = 'Maya'

    def __init__(ri, qij=None, baktun=None, katun=None, tun=None, winal=None, kin=None):

        ri.baktun = ri.katun = ri.tun = ri.winal = ri.kin = None

        super().__init__(qij=qij, baktun=baktun, katun=katun, tun=tun, winal=winal, kin=kin)


    def taban_rikïn_ajilanïk(ri, ajlnk):
        ri.baktun = NotImplemented
        ri.katun = NotImplemented
        ri.tun = NotImplemented
        ri.winal = NotImplemented
        ri.kin = NotImplemented

    def taban_rikïn_qij(ri, qij, **kwargs):
        ri.baktun = kwargs['baktun']
        ri.katun = kwargs['katun']
        ri.tun = kwargs['tun']
        ri.winal = kwargs['winal']
        ri.kin = kwargs['kin']

        ajlnk = NotImplemented

        return ajlnk

    def tatzibaj(ri, rubanom, chabäl):
        pass



class Tamil(Cholqij):

    def __init__(ri, qij, ik, junab):

        super().__init__(qij=qij, ik=ik, junab=junab)

    def taban_rikïn_ajilanïk(ri, ajlnk):
        pass

    def taban_rikïn_qij(ri, qij, **kwargs):
        pass

    def tatzibaj(ri, rubanom, chabäl):
        pass


class Farsi(Cholqij):
    def taban_rikïn_ajilanïk(ri, ajlnk):
        pass

    def taban_rikïn_qij(ri, qij, **kwargs):
        pass

    def tatzibaj(ri, rubanom, chabäl):
        pass

from datetime import date as qj
from datetime import timedelta

from cholqij.chabäl import taqaxaj_tzij


class Cholqij(object):
    nubi = NotImplemented

    def __init__(ri, qij, **kwargs):

        ri.chabäl = 'Kaqchikel'
        ri.ruwäch_ajilanïk = 'latino'

        if all(x is not None for x in kwargs.values()):
            ajlnk = ri._taban_rikïn_qij(qij, **kwargs)
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

            ri._taban_rikïn_ajilanïk(ajlnk)
            ri.qij_python = qj(year=qij_python.year, month=qij_python.month, day=qij_python.day)

    def _taban_rikïn_ajilanïk(ri, ajlnk):
        raise NotImplementedError

    def _taban_rikïn_qij(ri, qij, **kwargs):
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

        ri.chabäl = 'Español'

    def _taban_rikïn_ajilanïk(ri, ajlnk):
        qij_python = qj.fromordinal(ajlnk)

        ri.qij = qij_python.day
        ri.ik = qij_python.month
        ri.junab = qij_python.year
        ri.rubi_qij = qij_python.isoweekday()

    def _taban_rikïn_qij(ri, qij, **kwargs):

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


class Mayab(Cholqij):
    nubi = 'Mayab\''

    _ajilanïk_qij0_py = int(((20 + 30 + 31 + 30 + 31 + 365) + 365.25 * 3112 - 31 + 7) + 1)

    def __init__(ri, qij=None, baktun=None, katun=None, tun=None, winal=None, kin=None):

        ri.baktun = ri.katun = ri.tun = ri.winal = ri.kin = None

        ri.tzolkin = ri.aj_tzolkin = None
        ri.haab = ri.qij_haab = None

        super().__init__(qij=qij, baktun=baktun, katun=katun, tun=tun, winal=winal, kin=kin)

    def _taban_rikïn_ajilanïk(ri, ajlnk):

        ajlnk = ajlnk + ri._ajilanïk_qij0_py

        ri._tajilaj_tzolkin(ajlnk)
        ri._tajilaj_haab(ajlnk)

        ri.baktun = ajlnk // 144000
        ajlnk %= 144000
        ri.katun = ajlnk // 7200
        ajlnk %= 7200
        ri.tun = ajlnk // 360
        ajlnk %= 360
        ri.winal = ajlnk // 20
        ri.kin = ajlnk % 20

    def _taban_rikïn_qij(ri, qij, **kwargs):
        ri.baktun = baktun = kwargs['baktun']
        ri.katun = katun = kwargs['katun']
        ri.tun = tun = kwargs['tun']
        ri.winal = winal = kwargs['winal']
        ri.kin = kin = kwargs['kin']

        ajlnk_mayab = baktun * 144000 + katun * 7200 + tun * 360 + winal * 20 + kin

        ri._tajilaj_tzolkin(ajlnk_mayab)
        ri._tajilaj_haab(ajlnk_mayab)

        ajlnk_py = ajlnk_mayab - ri._ajilanïk_qij0_py

        return ajlnk_py

    def _tajilaj_haab(ri, ajlnk):
        ri.haab = ((ajlnk + 17 * 20 + 7) % 365) // 20 + 1
        ri.qij_haab = ((ajlnk + 17 * 20 + 7) % 365) % 20 + 1

    def _tajilaj_tzolkin(ri, ajlnk):
        ri.tzolkin = (ajlnk + 19) % 20 + 1
        ri.aj_tzolkin = (ajlnk + 3) % 13 + 1

    def tatzibaj(ri, rubanom='konojel', chabäl=None, ruwäch_ajilanïk=None):
        if chabäl is None:
            chabäl = ri.chabäl
        if ruwäch_ajilanïk is None:
            ruwäch_ajilanïk = ri.ruwäch_ajilanïk

        if rubanom.lower() == 'konojel':
            haab = taqaxaj_tzij(cholqij="Mayab'", wachinaq="Haab'", chabäl=chabäl)
            tzolkin = taqaxaj_tzij(cholqij="Mayab'", wachinaq="Tz'olk'in", chabäl=chabäl)

            return '{}.{}.{}.{}.{} {} {}, {} {}'.format(
                ri.baktun, ri.katun, ri.tun, ri.winal, ri.kin,
                ri.aj_tzolkin, tzolkin[ri.tzolkin], ri.qij_haab, haab[ri.qij_haab])

        if rubanom.lower() == 'ajilanïk_qij':
            return '{}.{}.{}.{}.{}'.format(ri.baktun, ri.katun, ri.tun, ri.winal, ri.kin)

        if rubanom.lower() == "haab'":
            haab = taqaxaj_tzij(cholqij="Mayab'", wachinaq="Haab'", chabäl=chabäl)
            return '{} {}'.format(ri.qij_haab, haab[ri.haab - 1])

        if rubanom.lower() == "tzolk'in":
            tzolkin = taqaxaj_tzij(cholqij="Mayab'", wachinaq="Tz'olk'in", chabäl=chabäl)
            return '{} {}'.format(ri.aj_tzolkin, tzolkin[ri.tzolkin - 1])


class Tamil(Cholqij):

    def __init__(ri, qij, ik, junab):
        super().__init__(qij=qij, ik=ik, junab=junab)

        ri.chabäl = 'தமிழ்'
        ri.ruwäch_ajilanïk = 'தமிழ்'

    def _taban_rikïn_ajilanïk(ri, ajlnk):
        pass

    def _taban_rikïn_qij(ri, qij, **kwargs):
        pass

    def tatzibaj(ri, rubanom, chabäl):
        pass


class Farsi(Cholqij):
    def _taban_rikïn_ajilanïk(ri, ajlnk):
        pass

    def _taban_rikïn_qij(ri, qij, **kwargs):
        pass

    def tatzibaj(ri, rubanom, chabäl):
        pass

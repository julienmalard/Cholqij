from datetime import date as qj
from datetime import timedelta

from cholqij.chabäl import taqaxaj_tzij, taqaxaj_ajilanïk as tqxj_ajlnk


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

    def tatzibaj(ri, rubanom='konojel', chabäl=None, ruwäch_ajilanïk=None):
        raise NotImplementedError

    def taya_qij_wuqqij(ri, chabäl=None):
        if chabäl is None:
            chabäl = ri.chabäl

        aj_qij = ri.qij_python.isoweekday()

        return taqaxaj_tzij(cholqij="Wuqq'ij", wachinaq="Kib'i' q'ij", chabäl=chabäl)[aj_qij]

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

    def tatzibaj(ri, rubanom='konojel', chabäl=None, ruwäch_ajilanïk=None):
        if chabäl is None:
            chabäl = ri.chabäl
        if ruwäch_ajilanïk is None:
            ruwäch_ajilanïk = ri.ruwäch_ajilanïk

        if rubanom == 'konojel':
            qij = tqxj_ajlnk(ri.qij, ruwäch=ruwäch_ajilanïk)
            ik = taqaxaj_tzij(cholqij=ri.nubi, wachinaq="Kib'i' ik'", chabäl=chabäl)[ri.ik]
            return '{} {} {}'.format(qij, ik, ri.junab)

        else:
            raise ValueError('')


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

    def tatzibaj(ri, rubanom='konojel', chabäl=None, rwch_ajlnk=None):
        if chabäl is None:
            chabäl = ri.chabäl
        if rwch_ajlnk is None:
            rwch_ajlnk = ri.ruwäch_ajilanïk

        haab = taqaxaj_tzij(cholqij="Mayab'", wachinaq="Haab'", chabäl=chabäl)[ri.haab - 1]
        tzolkin = taqaxaj_tzij(cholqij="Mayab'", wachinaq="Tz'olk'in", chabäl=chabäl)[ri.tzolkin - 1]
        aj_tzolkin = tqxj_ajlnk(ri.aj_tzolkin, ruwäch=rwch_ajlnk)
        qij_haab = tqxj_ajlnk(ri.qij_haab, ruwäch=rwch_ajlnk)
        baktun, katun, tun, winal, kin = [tqxj_ajlnk(x, ruwäch=rwch_ajlnk) for x in [
            ri.baktun, ri.katun, ri.tun, ri.winal, ri.kin]]

        if rubanom.lower() == 'konojel':
            return '{}.{}.{}.{}.{} {} {}, {} {}'.format(
                baktun, katun, tun, winal, kin, aj_tzolkin, tzolkin, qij_haab, haab
            )

        if rubanom.lower() == 'ajilanïk_qij':
            return '{}.{}.{}.{}.{}'.format(baktun, katun, tun, winal, kin)

        if rubanom.lower() == "haab'":
            return '{} {}'.format(qij_haab, haab)

        if rubanom.lower() == "tzolk'in":
            return '{} {}'.format(aj_tzolkin, tzolkin)


class Tamil(Cholqij):

    def __init__(ri, qij, ik, junab):
        super().__init__(qij=qij, ik=ik, junab=junab)

        ri.chabäl = 'தமிழ்'
        ri.ruwäch_ajilanïk = 'தமிழ்'

    def _taban_rikïn_ajilanïk(ri, ajlnk):
        pass

    def _taban_rikïn_qij(ri, qij, **kwargs):
        pass

    def tatzibaj(ri, rubanom='konojel', chabäl=None, ruwäch_ajilanïk=None):
        pass


class Japón(Cholqij):
    nubi = 'Japón'

    ketamabal_ajaw = {'大宝': 701,
                      '慶雲': 704,
                      '和銅': 708,
                      '霊亀': 715,
                      '養老': 717,
                      '神亀': 724,
                      '天平': 729,
                      '天平感宝': 749,
                      '天平勝宝': 749,
                      '天平宝字': 757,
                      '天平神護': 765,
                      '神護景雲': 767,
                      '宝亀': 770,
                      '天応': 781,
                      '延暦': 782,
                      '大同': 806,
                      '弘仁': 810,
                      '天長': 824,
                      '承和': 834,
                      '嘉祥': 848,
                      '仁寿': 851,
                      '斉衡': 854,
                      '天安': 857,
                      '貞観': 859,
                      '元慶': 877,
                      '仁和': 885,
                      '寛平': 889,
                      '昌泰': 898,
                      '延喜': 901,
                      '延長': 923,
                      '承平': 931,
                      '天慶': 938,
                      '天暦': 947,
                      '天徳': 957,
                      '応和': 961,
                      '康保': 964,
                      '安和': 968,
                      '天禄': 970,
                      '天延': 973,
                      '貞元': 976,
                      '天元': 978,
                      '永観': 983,
                      '寛和': 985,
                      '永延': 987,
                      '永祚': 988,
                      '正暦': 990,
                      '長徳': 995,
                      '長保': 999,
                      '寛弘': 1004,
                      '長和': 1012,
                      '寛仁': 1017,
                      '治安': 1021,
                      '万寿': 1024,
                      '長元': 1028,
                      '長暦': 1037,
                      '長久': 1040,
                      '寛徳': 1044,
                      '永承': 1046,
                      '天喜': 1053,
                      '康平': 1058,
                      '治暦': 1065,
                      '延久': 1069,
                      '承保': 1074,
                      '承暦': 1077,
                      '永保': 1081,
                      '応徳': 1084,
                      '寛治': 1087,
                      '嘉保': 1094,
                      '永長': 1096,
                      '承徳': 1097,
                      '康和': 1099,
                      '長治': 1104,
                      '嘉承': 1106,
                      '天仁': 1108,
                      '天永': 1110,
                      '永久': 1113,
                      '元永': 1118,
                      '保安': 1120,
                      '天治': 1124,
                      '大治': 1126,
                      '天承': 1131,
                      '長承': 1132,
                      '保延': 1135,
                      '永治': 1141,
                      '康治': 1142,
                      '天養': 1144,
                      '久安': 1145,
                      '仁平': 1151,
                      '久寿': 1154,
                      '保元': 1156,
                      '平治': 1159,
                      '永暦': 1160,
                      '応保': 1161,
                      '長寛': 1163,
                      '永万': 1165,
                      '仁安': 1166,
                      '嘉応': 1169,
                      '承安': 1171,
                      '安元': 1175,
                      '治承': 1177,
                      '養和': 1181,
                      '寿永': 1182,
                      '元暦': 1184,
                      '文治': 1185,
                      '建久': 1190,
                      '正治': 1199,
                      '建仁': 1201,
                      '元久': 1204,
                      '建永': 1206,
                      '承元': 1207,
                      '建暦': 1211,
                      '建保': 1213,
                      '承久': 1219,
                      '貞応': 1222,
                      '元仁': 1224,
                      '嘉禄': 1225,
                      '安貞': 1227,
                      '寛喜': 1229,
                      '貞永': 1232,
                      '天福': 1233,
                      '文暦': 1234,
                      '嘉禎': 1235,
                      '暦仁': 1238,
                      '延応': 1239,
                      '仁治': 1240,
                      '寛元': 1243,
                      '宝治': 1247,
                      '建長': 1249,
                      '康元': 1256,
                      '正嘉': 1257,
                      '正元': 1259,
                      '文応': 1260,
                      '弘長': 1261,
                      '文永': 1264,
                      '建治': 1275,
                      '弘安': 1278,
                      '正応': 1288,
                      '永仁': 1293,
                      '正安': 1299,
                      '乾元': 1302,
                      '嘉元': 1303,
                      '徳治': 1306,
                      '延慶': 1308,
                      '応長': 1311,
                      '正和': 1312,
                      '文保': 1317,
                      '元応': 1319,
                      '元亨': 1321,
                      '正中': 1324,
                      '嘉暦': 1326,
                      '元徳': 1329,
                      '元弘': 1331,
                      '建武': 1334,
                      '正慶': 1332,
                      '(Cour': 1333,
                      '暦応': 1338,
                      '康永': 1342,
                      '貞和': 1345,
                      '観応': 1350,
                      '文和': 1352,
                      '延文': 1356,
                      '康安': 1361,
                      '貞治': 1362,
                      '応安': 1368,
                      '永和': 1375,
                      '康暦': 1379,
                      '永徳': 1381,
                      '至徳': 1384,
                      '嘉慶': 1387,
                      '康応': 1389,
                      '明徳': 1390,
                      '延元': 1336,
                      '興国': 1340,
                      '正平': 1346,
                      '建徳': 1370,
                      '文中': 1372,
                      '天授': 1375,
                      '弘和': 1381,
                      '元中': 1384,
                      '応永': 1394,
                      '正長': 1428,
                      '永享': 1429,
                      '嘉吉': 1441,
                      '文安': 1444,
                      '宝徳': 1449,
                      '享徳': 1452,
                      '康正': 1455,
                      '長禄': 1457,
                      '寛正': 1460,
                      '文正': 1466,
                      '応仁': 1467,
                      '文明': 1469,
                      '長享': 1487,
                      '延徳': 1489,
                      '明応': 1492,
                      '文亀': 1501,
                      '永正': 1504,
                      '大永': 1521,
                      '享禄': 1528,
                      '天文': 1532,
                      '弘治': 1555,
                      '永禄': 1558,
                      '元亀': 1570,
                      '天正': 1573,
                      '文禄': 1592,
                      '慶長': 1596,
                      '元和': 1615,
                      '寛永': 1624,
                      '正保': 1644,
                      '慶安': 1648,
                      '承応': 1652,
                      '明暦': 1655,
                      '万治': 1658,
                      '寛文': 1661,
                      '延宝': 1673,
                      '天和': 1681,
                      '貞享': 1684,
                      '元禄': 1688,
                      '宝永': 1704,
                      '正徳': 1711,
                      '享保': 1716,
                      '元文': 1736,
                      '寛保': 1741,
                      '延享': 1744,
                      '寛延': 1748,
                      '宝暦': 1751,
                      '明和': 1764,
                      '安永': 1772,
                      '天明': 1781,
                      '寛政': 1789,
                      '享和': 1801,
                      '文化': 1804,
                      '文政': 1818,
                      '天保': 1830,
                      '弘化': 1844,
                      '嘉永': 1848,
                      '安政': 1854,
                      '万延': 1860,
                      '文久': 1861,
                      '元治': 1864,
                      '慶応': 1865,
                      '明治': 1868,
                      '大正': 1912,
                      '昭和': 1926,
                      '平成': 1989

                      }

    def __init__(ri, qij, ik=None, junab=None, ajaw=None):
        ri.qij = qij
        ri.ik = ik
        ri.junab = junab
        ri.ajaw = ajaw

        super().__init__(qij=qij, ik=ik, junab=junab, ajaw=ajaw)

        ri.chabäl = '日本語'
        ri.ruwäch_ajilanïk = '日本語'

    def _taban_rikïn_ajilanïk(ri, ajlnk):

        qij_python = qj.fromordinal(ajlnk)
        ri.qij = qij_python.day
        ri.ik = qij_python.month
        junab_py = qij_python.year

        l_ajaw = sorted(ri.ketamabal_ajaw, key=lambda x: ri.ketamabal_ajaw[x])
        jnb_ajaw = [ri.ketamabal_ajaw[x] for x in l_ajaw]

        aj_ajaw = next(len(jnb_ajaw) - i - 1 for i, x in enumerate(jnb_ajaw[::-1]) if junab_py >= x)
        ri.ajaw = l_ajaw[aj_ajaw]
        ri.junab = junab_py - jnb_ajaw[aj_ajaw] + 1

    def _taban_rikïn_qij(ri, qij, **kwargs):
        ri.qij = qij
        ri.ik = kwargs['ik']
        ri.ajaw = kwargs['ajaw']
        ri.junab = kwargs['junab']

        junab_py = ri.ketamabal_ajaw[ri.ajaw] + ri.junab - 1
        qij_python = qj(year=junab_py, month=ri.ik, day=ri.qij)

        return qij_python.toordinal()

    def tatzibaj(ri, rubanom='konojel', chabäl=None, ruwäch_ajilanïk=None):
        if chabäl is None:
            chabäl = ri.chabäl
        if ruwäch_ajilanïk is None:
            ruwäch_ajilanïk = ri.ruwäch_ajilanïk

        ajaw = ri.ajaw
        junab = tqxj_ajlnk(ri.junab, ruwäch=ruwäch_ajilanïk)
        ik = tqxj_ajlnk(ri.ik, ruwäch=ruwäch_ajilanïk)
        qij = tqxj_ajlnk(ri.qij, ruwäch=ruwäch_ajilanïk)

        if rubanom.lower() == 'konojel':
            return '{}{}年{}月{}日'.format(ajaw, junab, ik, qij)


class Farsi(Cholqij):
    def _taban_rikïn_ajilanïk(ri, ajlnk):
        pass

    def _taban_rikïn_qij(ri, qij, **kwargs):
        pass

    def tatzibaj(ri, rubanom='konojel', chabäl=None, ruwäch_ajilanïk=None):
        pass

from cholqij import Gregoriano, Mayab, Japón

greg = Gregoriano(qij=1, ik=1, junab=2018)

print((greg + 1).qij_python)
greg += 1

print(greg.qij_python, greg.qij)
greg -= 1

print(greg.qij_python, greg.qij)

mayab = Mayab(greg)
print(mayab.tatzibaj())
print(mayab.tatzibaj(chabäl="K'iche'"))

japón = Japón(greg)
print(japón.tatzibaj(chabäl="K'iche'"))

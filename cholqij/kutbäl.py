from cholqij import Gregoriano

greg = Gregoriano(qij=1, ik=1, junab=2018)

print((greg + 1).qij_python)

greg += 1

print(greg.qij_python, greg.qij)

greg -= 1

print(greg.qij_python, greg.qij)

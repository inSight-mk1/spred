from daniel_tactics import DanielTactics
from uplimit_tactics import UplimitTactics
from xxnb_tactics import XXNBTactics

print("DanielTactics")
dt = DanielTactics(t_before=0)
dt.select()

print("\nXXNBTactics")
dt = XXNBTactics(t_before=0)
dt.select()

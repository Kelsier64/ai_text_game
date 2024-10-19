l = ["aa","bb","cc"]

re = " ".join(f"{i+1}.{item}" for i,item in enumerate(l))

print(re)
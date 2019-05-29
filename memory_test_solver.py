import re
from pysmt.shortcuts import Symbol, And, GE, LT, Plus, Equals, Int, get_model, Or, Times
from pysmt.typing import INT

mem_power_list= {}
mem_test_time_list={}
mem_list=[]

def read_file():
	f = open ("test_case.txt","r")
	count = 1
	for line in f:
		# print (line)
		if count==1:
			reobj = re.match('chip power: (\d+)',line)
			chip_power = int(reobj.group(1))
		elif count>2:
			reobj = re.match('(.+): (\d+), (\d+)',line)
			key = reobj.group(1)
			mem_list.append(key)
			mem_power = reobj.group(2)
			mem_test_time = reobj.group(3)
			mem_power_list[key] = int(mem_power)
			mem_test_time_list[key] = int(mem_test_time)
		count = count +1
	# print (chip_power)
	# print(mem_power_list)
	# print(mem_test_time_list)
	# print(mem_list)
	f.close
	return chip_power

def scheduler(chip_power):
	total_power = 0
	mem = [Symbol(M,INT) for M in mem_list]
	# print(mem_power_list.get(str(mem[0])))
	domain = And([And(GE(l, Int(0)),LT(l,Int(2))) for l in mem])
	# print(domain)
	sum_power = Plus([l*mem_power_list.get(str(l)) for l in mem])
	# print(sum_power)
	problem = Equals(sum_power,Int(chip_power))
	formula = And(domain,problem)
	# print(formula)
	model = get_model(formula)
	# print(model)
	if model!=None:
		for l in mem:
			mem_test_time_list[str(l)] =  mem_test_time_list[str(l)] - int(model.get_value(l).constant_value())
			if int(model.get_value(l).constant_value())== 1:
				print (str(l))
				total_power = total_power + mem_power_list[str(l)]
		print("total power:",total_power)
		return True
	else:
		return False


def delete_list():
	for memory, time in mem_test_time_list.items():
		if time == 0:
			try:
				mem_list.remove(memory)
			except:
				continue
			# del mem_test_time_list[memory]

def recursive(chip_power):
	total_test_time = 0
	while(mem_list!=[]):
		step = 0
		print("time ",total_test_time,":")
		while (scheduler(chip_power-step)!=True):
			step = step +1
		delete_list()
		# print(mem_list)
		total_test_time +=1
	return total_test_time


if __name__ == "__main__":
	chip_power = read_file()
	print("total test time:",recursive(chip_power))


















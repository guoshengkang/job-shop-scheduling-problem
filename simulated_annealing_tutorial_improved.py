import numpy as np
import pandas as pd
import random
from copy import deepcopy

url = 'http://www.sohu.com/a/210894022_291099'

# 行：产品，列：机器，值：时间
# time_cost = [[3, 10, 9, 5, 3, 10],
# 	          [6, 8, 1, 5, 3, 3],
# 	          [1, 5, 5, 5, 9, 1],
# 	          [7, 4, 4, 3, 1, 3],
# 	          [6, 10, 7, 8, 5, 4],
# 	          [3, 10, 8, 9, 4, 9]]

# 行：产品，列：机器，值：顺序
# sequence = [[3, 1, 2, 4, 6, 5],
# 	         [2, 3, 5, 6, 1, 4],
# 	         [3, 4, 6, 1, 2, 5],
# 	         [2, 1, 3, 4, 5, 6],
# 	         [3, 2, 5, 6, 1, 4],
# 	         [2, 4, 6, 1, 5, 3]]

# 产品：顺序：（机器，时间）
context = {1:{1:(2,10),2:(3,9),3:(1,3),4:(4,5),5:(6,10),6:(5,3)},
		   2:{1:(5,3),2:(1,6),3:(2,8),4:(6,3),5:(3,1),6:(4,5)},
		   3:{1:(4,5),2:(5,9),3:(1,1),4:(2,5),5:(6,1),6:(3,5)},
		   4:{1:(2,4),2:(1,7),3:(3,4),4:(4,3),5:(5,1),6:(6,3)},
		   5:{1:(5,5),2:(2,10),3:(1,6),4:(6,4),5:(3,7),6:(4,8)},
		   6:{1:(4,9),2:(1,3),3:(6,9),4:(2,10),5:(5,4),6:(3,8)}}

# (产品，顺序)
init_solution = [(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),
       			 (2,1),(2,2),(2,3),(2,4),(2,5),(2,6),
       			 (3,1),(3,2),(3,3),(3,4),(3,5),(3,6),
       			 (4,1),(4,2),(4,3),(4,4),(4,5),(4,6),
       			 (5,1),(5,2),(5,3),(5,4),(5,5),(5,6),
       			 (6,1),(6,2),(6,3),(6,4),(6,5),(6,6)]

init_solution_1 = [(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),
				   (1,2),(2,2),(3,2),(4,2),(5,2),(6,2),
				   (1,3),(2,3),(3,3),(4,3),(5,3),(6,3),
				   (1,4),(2,4),(3,4),(4,4),(5,4),(6,4),
				   (1,5),(2,5),(3,5),(4,5),(5,5),(6,5),
				   (1,6),(2,6),(3,6),(4,6),(5,6),(6,6)]

# 判断一个解是否为有效解
def determination(solution):
	# 键为产品, 值为机器
	_dict = {1:[],2:[],3:[],4:[],5:[],6:[]}
	for operation in solution:
		_dict[operation[0]].append(operation[1])
		if len(_dict[operation[0]]) > 1:
			if _dict[operation[0]][-1] < _dict[operation[0]][-2]:
				return 'Infeasible solution'
	return 'feasible solution'


# 计算一个解的排程时间
def calculate_total_time(solution, context):
	if determination(solution) == 'Infeasible solution':
		return 'Infeasible solution'

	# 键为机器，值为产品
	_dict = {1:[],2:[],3:[],4:[],5:[],6:[]}
	# 创建机器进度指针和产品进度指针
	machine_pointer = {1:0,2:0,3:0,4:0,5:0,6:0}
	product_poniter = {1:0,2:0,3:0,4:0,5:0,6:0}
	for operation in solution:
		_dict[ context[operation[0]][operation[1]][0] ].append(operation[0])
		# operation[0]:产品编号 operation[1]：工序编号
		# context[operation[0]][operation[1]][0]:机器编号
		start = max(machine_pointer[context[operation[0]][operation[1]][0]], product_poniter[operation[0]])
		end = start + context[operation[0]][operation[1]][1]
		machine_pointer[context[operation[0]][operation[1]][0]] = end
		product_poniter[operation[0]] = end
	return max([machine_pointer[i] for i in machine_pointer]), _dict

# 实施退火算法
def simulated_annealing_algorithm(solution, T, alpha, Tend):
	'''
	solution:初始解
	T:初始温度
	alpha:温度衰减系数
	Tend:温度衰减的最低值
	'''
	# 出现过的最优解
	best_solution = {'objective': calculate_total_time(solution, context)[0],
					 'machine-schedule': calculate_total_time(solution, context)[1],
					 'solution': deepcopy(solution)}
	# 生成一组可行解
	solutions=[]
	for _ in range(20):
		# 生成新的10个可行解
		new_performance = 'Infeasible solution'
		while new_performance == 'Infeasible solution':
			int_1 = random.randint(0, 35)
			int_2 = random.randint(0, 35)
			tmp_solution = deepcopy(solution)
			tmp_solution[int_1], tmp_solution[int_2] = tmp_solution[int_2], tmp_solution[int_1]
			new_performance = calculate_total_time(tmp_solution, context)
		solutions.append(tmp_solution)

	# 总迭代次数
	iteration = 0
	# 在同一目标值时的重复次数
	iteration_at_optimal = 0

	# 终止条件为温度降到Tend或者连续无法出现最优解的次数达到1000次
	while (T >= Tend and iteration_at_optimal <= 1000):
		iteration += 1 # 自增迭代次数
		for index,one_solution in enumerate(solutions):
			old_solution = deepcopy(one_solution)
			old_performance = calculate_total_time(old_solution, context)
			# 生成新的可行解
			new_performance = 'Infeasible solution'
			while new_performance == 'Infeasible solution':
				int_1 = random.randint(0, 35)
				int_2 = random.randint(0, 35)
				solution = deepcopy(old_solution)
				solution[int_1], solution[int_2] = solution[int_2], solution[int_1]
				new_performance = calculate_total_time(solution, context)
			# 如果新解的目标值优于已知最优解，则取代已知最优解
			if new_performance[0] <= best_solution['objective']:
				best_solution = {'objective': new_performance[0],
								 'machine-schedule': new_performance[1],
								 'solution': deepcopy(solution)}
			# 计算新解和其上一个解的目标值差值（新解为其上一个解的邻解）
			delta = new_performance[0] - old_performance[0]
			# 如果有优化，则在新目标值得重复次数重设为0
			if delta < 0:
				iteration_at_optimal = 0
			# 如果没有优化，则一定概率退回上一个解，或以新解作为下一次迭代的起点
			elif delta == 0:
				iteration_at_optimal += 1
			else: # delta > 0
				iteration_at_optimal += 1
				rand = random.uniform(0, 1)
				keep_probability = np.exp(-delta/T)
				if keep_probability > rand:
					pass # 保留当前的解
				else: # 保留上一次的解
					solution = old_solution
			solutions[index]=solution
		T = alpha * T # 温度的衰减使得保留当前劣解的概率降低

		if iteration%200==0:
			print('[INFO]:{:-^30}'.format('迭代次数:{:4d},当前最优解的排程时间:{}'.format(iteration,best_solution['objective'])))
	
	print('退出迭代时的参数状态：',T,'>=',Tend,',',iteration_at_optimal,'<=',1000)	
	return best_solution, iteration

if __name__ == '__main__':
	print('[INFO]:{:-^30}'.format('输出算法求解过程'))
	best_solution,iteration=simulated_annealing_algorithm(init_solution_1, 10, 0.999, 0.001)
	print()
	print('[INFO]:{:-^30}'.format('输出算法求解的结果'))
	print('算法的迭代次数:{}'.format(iteration))
	print('最终最优解:{}'.format(best_solution['solution']))
	print('最终最优解的排程时间:{}'.format(best_solution['objective']))
	print('最终最优解的生产排程:{}'.format(best_solution['machine-schedule']))

	print()
	print('[INFO]:{:-^30}'.format('输出真正最优解'))
	# 真正最优解
	optimal_solution = [(1, 1), (5, 1), (6, 1), (2, 1), (3, 1), (4, 1), 
						(6, 2), (1, 2), (6, 3), (4, 2), (3, 2), (5, 2), 
						(1, 3), (4, 3), (5, 3), (6, 4), (4, 4), (1, 4), 
						(2, 2), (5, 4), (6, 5), (1, 5), (5, 5), (3, 3), 
						(2, 3), (4, 5), (5, 6), (3, 4), (6, 6), (1, 6), 
						(2, 4), (3, 5), (2, 5), (4, 6), (2, 6), (3, 6)]
	total_time,machine_schedule=calculate_total_time(optimal_solution, context)
	print('真正最优解的排程时间:{}'.format(total_time))
	print('真正最优解的生产排程:{}'.format(machine_schedule))

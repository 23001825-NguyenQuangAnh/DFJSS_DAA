import os
import matplotlib.pyplot as plt
import numpy as np

# Nhớ thay đổi đường dẫn import này cho khớp với thư mục thực tế của bạn
from GP_Engine import generate_random_tree, crossover, mutate
from GP_Simulator import GPSimulator, Draw_Gantt_GP
from DataSet.Instance import *


def evaluate_fitness(tree):
    sim = GPSimulator(J, Processing_time, M_num, Arrival_Time, Due_Dates, Breakdowns, gp_tree=tree)
    cmax, tardiness = sim.run()

    alpha = 0.7
    beta = 0.3
    fitness = (alpha * cmax) + (beta * tardiness)
    return fitness, cmax, tardiness


if __name__ == '__main__':
    # THIẾT LẬP THAM SỐ
    POP_SIZE = 200  # Số lượng công thức toán học cạnh tranh
    GENERATIONS = 200  # Số thế hệ tiến hóa
    MAX_DEPTH = 5  # Cây công thức sâu nhất

    os.makedirs(os.path.join(os.path.dirname(__file__), ''), exist_ok=True)

    print("--- BẮT ĐẦU HUẤN LUYỆN LUẬT PHÂN PHỐI BẰNG GP ---")
    population = [generate_random_tree(MAX_DEPTH) for _ in range(POP_SIZE)]

    best_overall_tree = None
    best_overall_fitness = float('inf')
    best_cmax, best_tardiness = 0, 0
    history_fitness = []

    for gen in range(GENERATIONS):
        fitness_scores = []
        cmax_list = []
        tard_list = []

        for tree in population:
            try:
                fit, c, t = evaluate_fitness(tree)
            except (OverflowError, ZeroDivisionError, ValueError):
                # Loại bỏ cá thể sinh ra phép tính lỗi hoặc quá tải (infinity)
                fit, c, t = float('inf'), 0, 0

            fitness_scores.append(fit)
            cmax_list.append(c)
            tard_list.append(t)

        gen_best_idx = np.argmin(fitness_scores)
        gen_best_fit = fitness_scores[gen_best_idx]

        if gen_best_fit < best_overall_fitness:
            best_overall_fitness = gen_best_fit
            best_overall_tree = population[gen_best_idx]
            best_cmax = cmax_list[gen_best_idx]
            best_tardiness = tard_list[gen_best_idx]
            print(
                f"[*] Kỷ lục mới tại Gen {gen}! Fitness: {best_overall_fitness:.2f} | Cmax: {best_cmax} | T: {best_tardiness}")
            print(f"    Công thức: {best_overall_tree}")

        history_fitness.append(best_overall_fitness)
        print(f"Thế hệ {gen:02d} hoàn tất. Best Gen Fit: {gen_best_fit:.2f}")

        # Chọn lọc & Lai tạo (Tournament)
        new_population = [best_overall_tree]  # Elitism (Giữ lại công thức vô địch)

        while len(new_population) < POP_SIZE:
            tournament_size = min(3, POP_SIZE)
            p1_idx = min(random.sample(range(POP_SIZE), tournament_size), key=lambda x: fitness_scores[x])
            p2_idx = min(random.sample(range(POP_SIZE), tournament_size), key=lambda x: fitness_scores[x])

            p1 = population[p1_idx]
            p2 = population[p2_idx]

            if random.random() < 0.8:
                c1, c2 = crossover(p1, p2)
                new_population.extend([c1, c2])
            else:
                new_population.append(mutate(p1, MAX_DEPTH))
                new_population.append(mutate(p2, MAX_DEPTH))

        population = new_population[:POP_SIZE]

    print("\n=========================================")
    print("QUÁ TRÌNH HUẤN LUYỆN GP HOÀN TẤT!")
    print(f"Luật lập lịch tốt nhất: {best_overall_tree}")
    print(f"Fitness: {best_overall_fitness:.2f} (Cmax: {best_cmax}, Tardiness: {best_tardiness})")

    # Vẽ biểu đồ
    plt.figure(figsize=(10, 5))
    plt.plot(range(GENERATIONS), history_fitness, '-g', linewidth=2, label='GP Best Fitness')
    plt.title('Quá trình tiến hóa tìm kiếm Luật phân phối (GP)')
    plt.ylabel('Giá trị hàm thích nghi')
    plt.xlabel('Thế hệ')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.savefig(os.path.join(os.path.dirname(__file__), '', 'Result_GP.png'), dpi=300)
    plt.show()

    # Chạy lần cuối để lấy biểu đồ Gantt
    final_sim = GPSimulator(J, Processing_time, M_num, Arrival_Time, Due_Dates, Breakdowns, gp_tree=best_overall_tree)
    final_sim.run()
    Draw_Gantt_GP(final_sim.machines, best_cmax, best_tardiness, title="GP Evolved Rule Gantt")
import matplotlib.pyplot as plt

class GPSimulator:
    def __init__(self, J, Processing_time, M_num, Arrival_Time, Due_Dates, Breakdowns=None, gp_tree=None):
        """
        Simulator thiết kế riêng cho việc đánh giá cá thể GP.
        Bắt buộc phải truyền gp_tree vào.
        """
        self.J = J
        self.Processing_time = Processing_time
        self.M_num = M_num
        self.Arrival_Time = Arrival_Time
        self.Due_Dates = Due_Dates
        self.Breakdowns = Breakdowns if Breakdowns else []
        self.gp_tree = gp_tree

        if self.gp_tree is None:
            raise ValueError("GPSimulator cần một cây gp_tree để chạy!")

        # Khởi tạo Job
        self.jobs = []
        for k_id, v in self.J.items():
            self.jobs.append({
                'id': k_id, 'total_ops': v, 'current_op': 0,
                'ready_time': self.Arrival_Time[k_id - 1],
                'due_date': self.Due_Dates[k_id - 1],
                'is_done': False, 'finish_time': 0
            })

        # Khởi tạo Máy
        self.machines = []
        for i in range(self.M_num):
            m_breakdowns = [b for b in self.Breakdowns if b['machine'] == i]
            self.machines.append({'id': i, 'free_time': 0, 'history': [], 'breakdowns': m_breakdowns})
            for b in m_breakdowns:
                self.machines[i]['history'].append((b['start'], b['start'] + b['duration'], 'Break'))

    def run(self):
        t = 0

        # TỐI ƯU HÓA: Tạo mảng chứa riêng các Job chưa hoàn thành để không phải quét lại Job đã xong
        unfinished_jobs = [j for j in self.jobs]

        while unfinished_jobs:
            idle_machines = []
            for m in self.machines:
                is_broken = any(b['start'] <= t < b['start'] + b['duration'] for b in m['breakdowns'])
                if t >= m['free_time'] and not is_broken:
                    idle_machines.append(m)

            # TỐI ƯU HÓA: Chỉ lấy những job đã đến giờ và đưa vào danh sách chờ
            ready_jobs = [j for j in unfinished_jobs if j['ready_time'] <= t]

            job_assigned = False

            if idle_machines and ready_jobs:
                assignments = []
                for m in idle_machines:
                    for j in ready_jobs:
                        op_idx = j['current_op']
                        p_t = self.Processing_time[j['id'] - 1][op_idx][m['id']]

                        if p_t != 9999:
                            finish_t = t + p_t
                            overlap = any(
                                b['start'] < finish_t and (b['start'] + b['duration']) > t for b in m['breakdowns'])

                            if not overlap:
                                state = {
                                    'PT': p_t,
                                    'DD': j['due_date'],
                                    'T': t,
                                    'MFT': m['free_time'],
                                    'RO': j['total_ops'] - j['current_op']
                                }
                                priority_index = self.gp_tree.evaluate(state)
                                assignments.append({'job': j, 'machine': m, 'p_t': p_t, 'index': priority_index})

                if assignments:
                    assignments.sort(key=lambda x: x['index'], reverse=True)
                    best = assignments[0]

                    best['machine']['history'].append((t, t + best['p_t'], best['job']['id']))
                    best['machine']['free_time'] = t + best['p_t']
                    best['job']['current_op'] += 1

                    if best['job']['current_op'] >= best['job']['total_ops']:
                        best['job']['is_done'] = True
                        best['job']['finish_time'] = t + best['p_t']
                        # TỐI ƯU HÓA: Xóa thẳng Job đã xong khỏi mảng để vòng lặp sau nhẹ hơn
                        unfinished_jobs.remove(best['job'])
                    else:
                        best['job']['ready_time'] = t + best['p_t']

                    job_assigned = True

            # TỐI ƯU HÓA BƯỚC NHẢY THỜI GIAN
            if job_assigned:
                continue  # Nếu vừa xếp được việc, kiểm tra xem máy khác có nhận thêm việc được không ngay tại thời điểm t

            # Nếu không xếp được việc nào, nhảy vọt thời gian đến sự kiện gần nhất
            next_events = [j['ready_time'] for j in unfinished_jobs if j['ready_time'] > t]
            next_events += [m['free_time'] for m in self.machines if m['free_time'] > t]
            for m in self.machines:
                for b in m['breakdowns']:
                    if b['start'] > t: next_events.append(b['start'])
                    if b['start'] + b['duration'] > t: next_events.append(b['start'] + b['duration'])

            # Cập nhật thời gian t
            if next_events:
                t = min(next_events)
            else:
                t += 1

        cmax = max(j['finish_time'] for j in self.jobs)
        tardiness = sum(max(0, j['finish_time'] - j['due_date']) for j in self.jobs)
        return cmax, tardiness


def Draw_Gantt_GP(machines, cmax, tardiness, title="GP Rule Gantt"):
    colors = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
              'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua']
    plt.figure(figsize=(12, 6))
    for m in machines:
        for start, end, task in m['history']:
            if task == 'Break':
                plt.barh(m['id'], width=end - start, left=start, color='black', hatch='//')
            else:
                plt.barh(m['id'], width=end - start, left=start, color=colors[(task - 1) % len(colors)],
                         edgecolor='black')
                plt.text(start + (end - start) / 2, m['id'], str(task), color='black', fontweight='bold', ha='center',
                         va='center', fontsize=8)

    plt.yticks(range(len(machines)), range(1, len(machines) + 1))
    plt.title(f'{title} | Cmax: {cmax} | Total Tardiness: {tardiness}')
    plt.xlabel('Time (min)')
    plt.ylabel('Machine')
    plt.tight_layout()
    plt.show()
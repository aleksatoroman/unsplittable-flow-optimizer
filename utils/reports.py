import os
import csv

from models.flow_result import FlowResult


def write_report_to_csv(file_path, algorithm_name, params, elapsed_time, flow_result: FlowResult):
    write_header = not os.path.exists(file_path)

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        if write_header:
            header = ['Algorithm', 'Parameters', 'Elapsed Time (s)', 'Feasible', 'Max Flow-to-Capacity Ratio', 'Overflow']
            writer.writerow(header)

        feasible = flow_result.is_feasible()
        max_ratio = flow_result.calculate_max_flow_to_capacity_ratio()
        overflow = flow_result.calculate_overflow()

        row = [
            algorithm_name,
            str(params),
            f"{elapsed_time:.4f}",
            feasible,
            f"{max_ratio:.4f}",
            f"{overflow:.4f}"
        ]

        writer.writerow(row)

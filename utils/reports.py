import os
import csv

from models.flow_result import FlowResult


def write_report_to_csv(file_path, algorithm_name, params, elapsed_time, flow_result: FlowResult):
    write_header = not os.path.exists(file_path)

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        if write_header:
            header = ['Algorithm', 'Parameters', 'Elapsed Time (s)', 'Feasible', 'Max Flow-to-Capacity Ratio', 'Overflow', 'Score', 'Max Time In Seconds', 'No Improvement Threshold', 'Stopping Reason']
            writer.writerow(header)

        feasible = flow_result.is_feasible()
        max_ratio = flow_result.calculate_max_flow_to_capacity_ratio()
        overflow = flow_result.calculate_overflow()
        score = flow_result.calculate_score()
        max_time = params.get('max_time', None)
        no_improvement_threshold = params.get('no_improvement_threshold', None)

        row = [
            algorithm_name,
            str(params),
            f"{elapsed_time:.4f}",
            feasible,
            f"{max_ratio:.4f}",
            f"{overflow:.4f}",
            f"{score:.4f}",
            max_time,
            no_improvement_threshold,
            flow_result.stopping_reason
        ]

        writer.writerow(row)

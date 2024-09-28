import os
import pandas as pd
import matplotlib.pyplot as plt


class Statistics:
    def __init__(self, root_folder: str):
        self.root_folder = root_folder
        self.reports_df = self.load_reports()

    def load_reports(self):
        all_reports = []
        for root, dirs, files in os.walk(self.root_folder):
            for file in files:
                if file == 'report.csv':
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path)
                    df['Instance'] = os.path.basename(root)
                    all_reports.append(df)
        return pd.concat(all_reports, ignore_index=True)

    def best_parameters_per_algorithm(self):
        grouped = self.reports_df.groupby(['Algorithm', 'Parameters']).agg({
            'Score': 'mean'
        }).reset_index()

        best_params_per_algorithm = grouped.loc[grouped.groupby('Algorithm')['Score'].idxmax()]

        print("Best Parameters by Algorithm (Globally):")
        print(best_params_per_algorithm[['Algorithm', 'Parameters', 'Score']])
        return best_params_per_algorithm

    def compare_best_models(self):
        best_params = self.best_parameters_per_algorithm()

        best_params.plot(kind='bar', x='Algorithm', y='Score', legend=False, color='lightgreen')
        plt.ylabel('Best Score (Higher is Better)')
        plt.title('Best Algorithm Comparison Across All Instances')
        plt.show()
        
        for index, row in best_params.iterrows():
            print(f"Algorithm: {row['Algorithm']}")
            print(f"Best Parameters: {row['Parameters']}")
            print(f"Score: {row['Score']:.2f}")
            print('*' * 50)

    def run_best_of_best_analysis(self):
        self.compare_best_models()


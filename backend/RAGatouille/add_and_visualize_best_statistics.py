import json
import matplotlib
matplotlib.use("pdf")#'TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import os
import shutil

def copy_files(source_dir, destination_dir):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    else:
        # If the destination directory exists, delete all its contents
        for file in os.listdir(destination_dir):
            file_path = os.path.join(destination_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

    # Copy all files from source directory to destination directory
    for file_name in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file_name)
        destination_file = os.path.join(destination_dir, file_name)
        shutil.copy2(source_file, destination_file)
        print(f"Copied {source_file} to {destination_file}")

def main(args):
    best_checkpoint_path_German_DPR, best_checkpoint_path_XQA, best_checkpoint_path_HP = args.best_checkpoint_paths
    _, _, DPR_epoch, DPR_part = best_checkpoint_path_German_DPR.split("/")[-4:]
    _, _, XQA_epoch, XQA_part = best_checkpoint_path_XQA.split("/")[-4:]
    base_model_name, train_data, epoch, part = best_checkpoint_path_HP.split("/")[-4:]

    # append best checkpoint stats to best statistics
    df_stat = pd.read_csv(args.statistics_path)
    filtered_df_stat = df_stat[df_stat.iloc[:, 0] == f"{base_model_name}-{train_data}-{epoch}-{part}"]
    print(f"{base_model_name}-{train_data}-{epoch}-{part}")    
    print(filtered_df_stat)
    name = f"{train_data}-DPR{DPR_epoch}{DPR_part}-XQA{XQA_epoch}{XQA_part}-HP{epoch}{part}".replace("part", "p").replace("epoch", "e")
    filtered_df_stat.iloc[:, 0] = name
    print(filtered_df_stat)
    if os.path.exists(args.best_statistics_path): 
        df_best_stat = pd.read_csv(args.best_statistics_path)
        df_best_stat = pd.concat([df_best_stat, filtered_df_stat], axis=0)
    else:
        df_best_stat = filtered_df_stat
    print("df_best_stat", df_best_stat)
    # visualize best_statistics
    for _, row in df_best_stat.iterrows():
        y_values = list(row.iloc[1:len(Ks)+1])
        plt.plot(Ks, y_values, label=name)
    
    plt.xlabel('k')
    plt.ylabel('Recall@k')
    plt.legend(fontsize=6)
    plot_name = f"Best Checkpoints"
    plt.title(plot_name, loc='center', wrap=True)
    plt.savefig(args.save_img)
    plt.close()

    # save best checkpoint 
    df_best_stat.to_csv(args.best_statistics_path, index=False)
    copy_files(best_checkpoint_path_HP, f"{args.save_best_checkpoint}/{name}/checkpoint")
    copy_files(best_checkpoint_path_HP.replace("checkpoints", "indexes"), f"{args.save_best_checkpoint}/{name}/index")

Ks = [1,2,3,4,5,6,8,10,20,50,100]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--best_checkpoint_paths", metavar="N", type=str, nargs="+",
                        help="List of paths separated by spaces")
    parser.add_argument('--statistics_path', type=str, default="backend/data/statistics/statistics.csv", help="")
    parser.add_argument('--best_statistics_path', type=str, default="backend/data/statistics/best_statistics.csv" , help="")
    parser.add_argument('--save_img', type=str, default="backend/data/statistics/best_checkpoints.pdf", help="")
    parser.add_argument('--save_best_checkpoint', type=str, default="backend/data/colbert/best", help="")
    args = parser.parse_args()

    main(args)

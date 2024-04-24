conda create -y -n RAG_env_conda ; 
conda activate RAG_env_conda ; 
conda install -y -c conda-forge python=3.10 ; 
conda install -y pip ; 
/home/flml293c/.conda/envs/RAG_env_conda/bin/pip install ragatouille==0.0.7.post9 ; 
/home/flml293c/.conda/envs/RAG_env_conda/bin/pip uninstall -y faiss-cpu ; 
/home/flml293c/.conda/envs/RAG_env_conda/bin/pip uninstall -y faiss ; 
conda install -y -c conda-forge faiss-gpu ; 
conda install -y ninja matplotlib ; 
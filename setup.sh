# RUN POSTGRES
docker container run --name postgres_index_advisor -e POSTGRES_PASSWORD=adv -e POSTGRES_USER=adv -e POSTGRES_DB=adv -p 5432:5432 postgres:14 -d postgres_index_advisor

# INSTALL HYPOPG
sudo apt install curl ca-certificates gnupg
curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg >/dev/null
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
sudo apt install postgresql-14-hypopg -y

# INSTALL TOOLS
sudo apt install flex bison -y
sudo apt install unzip -y
sudo apt install net-tools -y
sudo apt install build-essential -y

# INSTALL CONDA ENVIRONMENT
conda config --set restore_free_channel true
conda env create -f environment.yaml python=3.6
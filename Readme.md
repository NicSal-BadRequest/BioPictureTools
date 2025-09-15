Entorno en PC:

readlink -f $(which java)

nano ~/.bashrc  # For bash users
# OR
nano ~/.zshrc   # For zsh users

export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

source ~/.bashrc

pip install python-bioformats
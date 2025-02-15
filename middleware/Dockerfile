# Utiliser Python comme base
FROM python:3.13

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers
COPY . /app

# Install Rust and Cargo before installing Python dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && export PATH="$HOME/.cargo/bin:$PATH"

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port du middleware
EXPOSE 5000

# Lancer le middleware
CMD ["python", "middleware.py"]

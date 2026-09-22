# =============================================================================
# Starter kit: Ollama backend
# =============================================================================
# Downloads the official Ollama linux tarball and extracts it with Python --
# deliberately NOT the official install.sh: on Codabench workers apt is
# unusable (the container lacks setuid/setgid capabilities and the Ubuntu 20.04
# repos are EOL), and install.sh needs apt-installed tools (zstd) to extract.
# Everything here relies only on pip packages and /tmp, which are known to work.
#
# The model is pulled straight from the HF Hub: ollama supports
# `hf.co/<user>/<repo>` ids for GGUF repos, with an optional quant tag.
# Edit the CONFIG block, then submit this file together with requirements.txt.
# =============================================================================
import os
import time
import shutil
import tarfile
import subprocess
import urllib.request

import ollama

# ---- CONFIG -----------------------------------------------------------------
# For Ollama, point at a GGUF repo. `hf.co/<user>/<repo>` pulls from HF Hub.
# You can also append a quant tag, e.g. "hf.co/user/repo:Q4_K_M".
OLLAMA_MODEL = "hf.co/bartowski/SmolLM2-135M-Instruct-GGUF:Q4_K_M"
HF_TOKEN = ""                 # only for PRIVATE / gated GGUF repos
SYSTEM_PROMPT = "You are a helpful assistant. Answer concisely."
TEMPERATURE = 0.7
TOP_P = 0.9
MAX_NEW_TOKENS = 128
# -----------------------------------------------------------------------------

# The tarball extracts to bin/ollama + lib/ollama (same tree install.sh uses).
OLLAMA_TARBALL = "https://ollama.com/download/ollama-linux-amd64.tar.zst"
INSTALL_DIR = "/tmp/ollama_dist"
# ollama writes keys to $HOME/.ollama and weights to $OLLAMA_MODELS; both are
# pointed at /tmp because it is the only location guaranteed writable.
DATA_DIR = "/tmp/ollama_home"
SERVER_LOG = "/tmp/ollama_serve.log"


class Submission:

    backend = "ollama"
    model_name = OLLAMA_MODEL.split("/")[-1]

    def _install_ollama(self):
        """Return a path to the ollama binary, downloading it if needed."""
        existing = shutil.which("ollama")
        if existing:
            return existing

        binary = os.path.join(INSTALL_DIR, "bin", "ollama")
        if not os.path.exists(binary):
            # zstandard comes from requirements.txt (pip works on the worker,
            # apt does not -- see the header comment).
            import zstandard

            os.makedirs(INSTALL_DIR, exist_ok=True)
            tarball = os.path.join(INSTALL_DIR, "ollama.tar.zst")
            print(f"[ollama] downloading {OLLAMA_TARBALL} (~1.4 GB) ...")
            urllib.request.urlretrieve(OLLAMA_TARBALL, tarball)

            print("[ollama] extracting ...")
            with open(tarball, "rb") as fh:
                dctx = zstandard.ZstdDecompressor()
                with dctx.stream_reader(fh) as reader:
                    with tarfile.open(fileobj=reader, mode="r|") as tar:
                        tar.extractall(INSTALL_DIR)
            os.remove(tarball)  # free ~1.4 GB of disk before pulling the model

            if not os.path.exists(binary):
                raise RuntimeError(
                    f"Extracted tarball but {binary} is missing - the tarball "
                    f"layout changed. Inspect {INSTALL_DIR}."
                )
        os.chmod(binary, 0o755)
        return binary

    def setup(self):
        if HF_TOKEN:
            os.environ["HF_TOKEN"] = HF_TOKEN
        binary = self._install_ollama()

        env = dict(os.environ)
        env["HOME"] = DATA_DIR
        env["OLLAMA_MODELS"] = os.path.join(DATA_DIR, "models")
        os.makedirs(env["OLLAMA_MODELS"], exist_ok=True)

        print(f"[ollama] starting server ({binary}) ...")
        self.server_log = open(SERVER_LOG, "w")
        self.server = subprocess.Popen(
            [binary, "serve"],
            env=env, stdout=self.server_log, stderr=subprocess.STDOUT,
        )
        # Wait for the server to accept connections before pulling.
        for _ in range(60):
            if self.server.poll() is not None:
                raise RuntimeError(
                    "`ollama serve` exited immediately. Server log:\n"
                    + open(SERVER_LOG).read()[-2000:]
                )
            try:
                ollama.list()
                break
            except Exception:
                time.sleep(1)
        else:
            raise RuntimeError(
                "ollama server did not become ready within 60s. Server log:\n"
                + open(SERVER_LOG).read()[-2000:]
            )

        print(f"[ollama] pulling {OLLAMA_MODEL} ...")
        ollama.pull(OLLAMA_MODEL)

    def generate(self, prompt):
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=(
                ([{"role": "system", "content": SYSTEM_PROMPT}] if SYSTEM_PROMPT else [])
                + [{"role": "user", "content": prompt}]
            ),
            options={
                "temperature": TEMPERATURE,
                "top_p": TOP_P,
                "num_predict": MAX_NEW_TOKENS,
            },
        )
        return response["message"]["content"].strip()

    def teardown(self):
        if getattr(self, "server", None):
            self.server.terminate()
        if getattr(self, "server_log", None):
            self.server_log.close()


# HackAsembler2binary

A **web-based Hack Assembler compiler** that combines the power of **Clojure for logic** and **Python (FastAPI)** for a web interface. It compiles Hack assembly language (from the [Nand2Tetris course](https://www.nand2tetris.org/)) into binary machine code.

---

## 🌐 Demo

Once the project is running, visit:

```
http://127.0.0.1:8000
```
---

## 🚀 Features

* ✅ Compile Hack assembly code to binary
* 🧠 Uses **Clojure** for the compiler logic
* 🔗 Uses **JPype** to connect Python with Clojure (via the JVM)
* 🌐 Simple web interface with **FastAPI** and **Jinja2**

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/jero98772/HackAsembler2binary.git
cd HackAsembler2binary
```

### 2. Build the Clojure JAR

Make sure you have [Leiningen](https://leiningen.org/) installed.

```bash
lein uberjar
```

This generates the JAR file at:

```
target/uberjar/clojure_hackassembler_web-0.1.0-SNAPSHOT-standalone.jar
```

### 3. Create Python virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the FastAPI server

```bash
python app/main.py
```

Now open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧠 How It Works

* The **assembler logic** (parsing Hack instructions and producing binary) is implemented in **Clojure**.
* The Clojure code is compiled into a standalone JAR.
* **JPype** launches the JVM and imports the Clojure classes in Python.
* **FastAPI** serves a web UI to input Hack code and displays the binary output.

---

## 📝 Example

Enter this Hack assembly:

```asm
@2
D=A
@3
D=D+A
@0
M=D
```

And get this output:

```
0000000000000010
1110110000010000
0000000000000011
1110000010010000
0000000000000000
1110001100001000
```

---

## 🧰 Dependencies

### Python

* `fastapi`
* `uvicorn`
* `jpype1`
* `jinja2`

### Clojure

* Standard Clojure compiler
* Core logic in `assembler.clj`

---

## 🧪 Development Tips

* If JPype fails to start JVM, ensure that `JAVA_HOME` is correctly set.
* Any changes in the Clojure code require rebuilding the JAR via `lein uberjar`.
* You can customize the `index.html` in `templates/` to improve the UI.


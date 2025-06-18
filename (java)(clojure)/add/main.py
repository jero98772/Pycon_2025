#python main.py
import jpype
import jpype.imports
from jpype.types import *
jpype.startJVM(classpath=["target/uberjar/add-0.1.0-SNAPSHOT-standalone.jar"])
Add = jpype.JClass("add.core")
clojure = jpype.JPackage("clojure")
sum_fn = clojure.java.api.Clojure.var("add.core", "sum")
result = sum_fn.invoke(5, 7)
print(f"The result is: {result}")
jpype.shutdownJVM()

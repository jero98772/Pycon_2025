#python main.py
import jpype
jpype.startJVM(classpath=["."])
Add = jpype.JClass("Add")
adder = Add()
result = adder.sum(5, 7)
print(f"The result is: {result}")
jpype.shutdownJVM()

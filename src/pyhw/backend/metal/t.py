import ctypes


mylib = ctypes.CDLL('./metalGPULib.dylib')
mylib.my_func.restype = ctypes.c_char_p

# Call the function
device_name = mylib.my_func()

# Print the result
print(f"Device Name: {device_name.decode('utf-8')}")
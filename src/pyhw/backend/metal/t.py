import ctypes


mylib = ctypes.CDLL('./metalGPULib.dylib')

mylib.backend_init.argtypes = []
mylib.backend_init.restype = None

mylib.get_default_device_name.argtypes = []
mylib.get_default_device_name.restype = ctypes.c_char_p


# Call the function
mylib.backend_init()
device_name = mylib.get_default_device_name()

# Print the result
print(f"Device Name: {device_name.decode('utf-8')}")


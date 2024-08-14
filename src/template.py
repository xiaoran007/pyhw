import os
import platform

# ASCII Art
ascii_art = """
                    'c.          
                 ,xNMM.          
               .OMMMMo           
               OMMM0,            
     .;loddo:' loolloddol;.      
   cKMMMMMMMMMMNWMMMMMMMMMM0:    
 .KMMMMMMMMMMMMMMMMMMMMMMMWd.    
 XMMMMMMMMMMMMMMMMMMMMMMMX.      
;MMMMMMMMMMMMMMMMMMMMMMMM:       
:MMMMMMMMMMMMMMMMMMMMMMMM:       
.MMMMMMMMMMMMMMMMMMMMMMMMX.      
 kMMMMMMMMMMMMMMMMMMMMMMMMWd.    
 .XMMMMMMMMMMMMMMMMMMMMMMMMMMk   
  .XMMMMMMMMMMMMMMMMMMMMMMMMK.   
    kMMMMMMMMMMMMMMMMMMMMMMd     
     ;KMMMMMMMWXXWMMMMMMMk.      
       .cooc,.    .,coo:.        
"""

# System Information
system_info = {
    "User": os.getlogin(),
    "Hostname": platform.node(),
    "OS": f"{platform.system()} {platform.release()} {platform.machine()}",
    "Kernel": platform.version(),
    "Uptime": f"{10} seconds",
    "Packages": "208 (brew)",  # This is a placeholder, customize as needed
    "Shell": os.getenv('SHELL'),
    "Resolution": "1440x900",  # Placeholder, customize if needed
    "DE": "Aqua",
    "WM": "Quartz Compositor",
    "WM Theme": "Blue (Dark)",
    "Terminal": os.getenv('TERM'),
    "Terminal Font": "SFMono-Regular",
    "CPU": platform.processor(),
    "GPU": "Apple M1",  # Placeholder, adjust according to your machine
    "Memory": f"{100000 // (1024 * 1024)}MiB / {1000000 // (1024 * 1024)}MiB"
}

# Prepare formatted system info
sys_info_str = f"""
{system_info['User']}@{system_info['Hostname']}
----------------------------------------
OS: {system_info['OS']}
Kernel: {system_info['Kernel']}
Uptime: {system_info['Uptime']}
Packages: {system_info['Packages']}
Shell: {system_info['Shell']}
Resolution: {system_info['Resolution']}
DE: {system_info['DE']}
WM: {system_info['WM']}
WM Theme: {system_info['WM Theme']}
Terminal: {system_info['Terminal']}
Terminal Font: {system_info['Terminal Font']}
CPU: {system_info['CPU']}
GPU: {system_info['GPU']}
Memory: {system_info['Memory']}
"""

# Split both ascii art and system info into lines
ascii_lines = ascii_art.strip().split('\n')
sys_info_lines = sys_info_str.strip().split('\n')

# Combine the lines side by side
combined_lines = []
max_len_ascii = max(len(line) for line in ascii_lines)
for ascii_line, sys_info_line in zip(ascii_lines, sys_info_lines):
    combined_line = ascii_line.ljust(max_len_ascii) + "    " + sys_info_line
    combined_lines.append(combined_line)

# If there are more ascii lines, add them
for ascii_line in ascii_lines[len(sys_info_lines):]:
    combined_lines.append(ascii_line)

# If there are more sys info lines, add them
for sys_info_line in sys_info_lines[len(ascii_lines):]:
    combined_lines.append(" " * max_len_ascii + "    " + sys_info_line)

# Print the result
print("\n".join(combined_lines))
